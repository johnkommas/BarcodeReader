#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved
import pathlib
import uvicorn
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from my_app.SLACK import slack_getters, slack_home_page, slack_modal, slack_channels
from my_app.SELF_LABEL import barcode_generator, create_final_image
from fastapi import FastAPI, Request
import warnings
from tqdm import tqdm
from my_app.SQL import sql3_conn, sql_connect, pass_manager
import logging

path = pathlib.Path(__file__).parent.resolve()
log_path = f'{path}/_std.log'
logging.basicConfig(filename=log_path, filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')
logger=logging.getLogger()
logger.setLevel(logging.INFO)

warnings.simplefilter("ignore", UserWarning)

sql3_conn.main()
df = sql3_conn.read_token_for_slack()
app = App(signing_secret=pass_manager.decrypt(df['KeyOnSave'].values[0], df['SlackSecret'].values[0]),
          token=df['SlackToken'].values[0])
app_handler = SlackRequestHandler(app)


@app.event("app_home_opened")
def publish_home_view(client, event, logger):
    entersoft_id = sql3_conn.main()
    user_info = slack_getters.get_user_details(event, client)
    # logger.error(f"User {user_info['user']['profile'].get('display_name')} clicked:  [Home Page]")
    try:
        client.views_publish(
            user_id=event["user"],
            view=slack_home_page.event(user_info, entersoft_id, sql3_conn.read_activity()))
    except Exception as e:
        logger.error(f"Error publishing view to Home Tab: {e}")


@app.event("message")
def handle_message_events(body, logger):
    logger.info(body)


@app.action("action_id_barcode_generator")
def action_button_click(body, ack, say, logger, client):
    logger.info(body)
    # print(body)
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient
    client.views_open(
        trigger_id=body["trigger_id"],
        view=slack_modal.modal_view()
    )


@app.action("action_id_entersoft_sql")
def action_button_click(body, ack, say, logger, client):
    # print(body)
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient
    client.views_open(
        trigger_id=body["trigger_id"],
        view=slack_modal.sql_modal_view()
    )


@app.action("action_id_special_price_list")
def action_button_click(body, ack, say, logger, client):
    # print(body)
    # Acknowledge the shortcut request
    ack()
    # Call the views_open method using the built-in WebClient
    client.views_open(
        trigger_id=body["trigger_id"],
        view=slack_modal.special_offer_modal()
    )


@app.view("modal_button_triggered_barcode_generator")
def handle_submission(ack, body, client, view, logger, ):
    ack()
    try:
    # get username
        user_info = slack_getters.get_modal_user_details(body, client)
        logger.info(body)
        # get keys from modal
        key = view['state'].get('values').keys()
        key = list(key)
        # get values from inputs
        for i in key:
            x = list(view['state']['values'][i].keys())[0]
            if x == 'a_pick_type_static_select_action':
                type = str(view['state']['values'][i][x]['selected_option'].get('value'))
            elif x == 'b_pda_number_plain_text_input_action':
                number = int(view['state']['values'][i][x].get('value'))
            elif x == 'c_pick_type_static_select_store':
                store = str(view['state']['values'][i][x]['selected_option'].get('value'))
            elif x == 'd_pick_type_static_select_color':
                special_color = str(view['state']['values'][i][x]['selected_option'].get('value'))
            elif x == 'e_pick_type_static_select_tags':
                tags = str((view['state']['values'][i][x]['selected_option'].get('value')))
            elif x == 'normal_price_pick_label_size':
                is_big = int((view['state']['values'][i][x]['selected_option'].get('value')))
            elif x == 'normal_price_printer_name':
                printer_name = str((view['state']['values'][i][x]['selected_option'].get('value')))

        stores = ['EM', 'L1', 'L2']
        special_colors = ['WHITE', 'YELLOW', 'RED']
        bg_colors = ['#61D839', '#6FBCF0']
        prices = ['RetailPrice', 'LATO 01', 'LATO 02']
        file_names = ['Elounda Market White.png', 'Elounda Market Yellow.png', 'Lato White.png', 'Lato Yellow.png', 'Elounda Market RED.png']

        bg_color = bg_colors[0]
        file_name = file_names[0]
        price = prices[0]

        if store == stores[0]:
            price = prices[0]
            bg_color = bg_colors[0]
            if special_color == special_colors[0]:
                file_name = file_names[0]
            elif special_color == special_colors[1]:
                file_name = file_names[1]
            elif special_color == special_colors[2]:
                file_name = file_names[4]
        elif store == stores[1]:
            price = prices[1]
            bg_color = bg_colors[1]
            if special_color == special_colors[0]:
                file_name = file_names[2]
            elif special_color == special_colors[1]:
                file_name = file_names[3]
            elif special_color == special_colors[2]:
                file_name = file_names[4]
        elif store == stores[2]:
            price = prices[2]
            bg_color = bg_colors[1]
            if special_color == special_colors[0]:
                file_name = file_names[2]
            elif special_color == special_colors[1]:
                file_name = file_names[3]
            elif special_color == special_colors[2]:
                file_name = file_names[4]

        # run my_app
        df = barcode_generator.run(number, type, bg_color)
        for i in tqdm(df.BarCode.unique(), desc='Barcode Generator: Creating Final Images:'):
            create_final_image.run(df[df['BarCode'] == i], file_name, price, tags)

        # Create A4 Pages Ready To Print
        create_final_image.split_labels_to_fit_a4(is_big)

        # Εκτύπωση των ετικετών
        create_final_image.export_to_printer(printer_name)

    except Exception as e:
        logger.error(f"Error responding to 'first_button' button click: {e}")
        print(f"⭕️ Error on Home Page: Barcode Generator Button 💭")
    finally:
        print("END")
        # insert sql data, refresh home page,  update channel image
        # slack_channels.update_users_activity(user_info, 'NORMAL PRICES')


@app.view("modal_button_triggered_initialize_sql_settings")
def handle_submission(ack, body, client, view, logger, ):
    ack()
    try:
        # get user_name
        user_info_initialize_sql = slack_getters.get_modal_user_details(body, client)
        logger.info(body)

        # get keys from modal
        key = view['state'].get('values').keys()
        key = list(key)

        sql_server_ip = str(view['state']['values'][key[0]]['sql_server_ip'].get('value'))
        sql_server_uid = str(view['state']['values'][key[1]]['sql_server_uid'].get('value'))
        f_sql_key, sql_server_password = pass_manager.encrypt(
            str(view['state']['values'][key[2]]['sql_server_password'].get('value')))
        sql_server_Database = str(view['state']['values'][key[3]]['sql_server_Database'].get('value'))
        sql_server_TrustServerCertificate = str(
            view['state']['values'][key[4]]['sql_server_TrustServerCertificate']['selected_option'].get('value'))

        vpn_name = str(view['state']['values'][key[5]]['vpn_name'].get('value'))
        f_vpn_key, vpn_secret = pass_manager.encrypt(str(view['state']['values'][key[6]]['vpn_secret'].get('value')))

        sql_data = (
            sql_server_ip, sql_server_uid, sql_server_password, sql_server_Database,
            sql_server_TrustServerCertificate,
            f_sql_key)
        vpn_data = (vpn_name, vpn_secret, f_vpn_key)

        sql3_conn.insertVariableIntoSqlTable(sql_data)
        sql3_conn.insertVariableIntoVpnTable(vpn_data)

    except Exception as e:
        logger.error(f"Error responding to 'first_button' button click: {e}")
        print(f"⭕️ Error on Home Page: Initialize SQL Settings 💭")
    finally:
        # refresh home page
        slack_getters.refresh_home_page(client, user_info_initialize_sql)


@app.view("modal_button_triggered_special_offer")
def handle_submission(ack, body, client, view, logger, ):
    ack()
    try:
        # get user_name
        user_info_special_offer = slack_getters.get_modal_user_details(body, client)
        logger.info(body)

        # get keys from modal
        key = view['state'].get('values').keys()
        key = list(key)

        for i in key:
            x = list(view['state']['values'][i].keys())[0]
            if x == 'special_offer_datepicker_action_from':
                from_date = (view['state']['values'][i][x].get('selected_date'))
            elif x == 'special_offer_pick_type_static_select_store':
                store = str(view['state']['values'][i][x]['selected_option'].get('value'))
            elif x == 'special_offer_pick_label_size':
                is_big = int(view['state']['values'][i][x]['selected_option'].get('value'))
            elif x == 'special_offer_pick_printer_name':
                printer_name = str(view['state']['values'][i][x]['selected_option'].get('value'))

        stores = ['EM', 'L1', 'L2']
        prices = ['RetailPrice', 'LATO 01', 'LATO 02']
        file_names = ['Elounda Market RED.png', 'Lato Yellow.png']
        tags = ["special_offer", 'none']

        if store == stores[0]:
            price = prices[0]
            file_name = file_names[0]
        elif store == stores[1]:
            price = prices[1]
            file_name = file_names[0]
        else:
            price = prices[2]
            file_name = file_names[0]

        df = barcode_generator.special_offer_get_data(from_date)
        print(df)
        for i in tqdm(df['ΚΩΔΙΚΟΣ'].unique(), desc='Barcode Generator: Creating Final Images:'):
            create_final_image.special_price(df[df['ΚΩΔΙΚΟΣ'] == i], file_name, price, tags[-1])

        # Create A4 Pages Ready To Print
        create_final_image.split_labels_to_fit_a4(is_big)

        # Εκτύπωση των ετικετών
        create_final_image.export_to_printer(printer_name)


    except Exception as e:
        logger.error(f"Error responding to 'first_button' button click: {e}")
        print(f"⭕️ Error on Home Page: Special Offer 💭 {e}")
    finally:
        print("END")
        # insert sql data, refresh home page,  update channel image
        # slack_channels.update_users_activity(user_info_special_offer, 'SPECIAL OFFER')


api = FastAPI()


@api.post("/slack/events")
async def endpoint(req: Request):
    return await app_handler.handle(req)


@api.get("/")
async def root():
    x = {'print': 'Hello World'}
    return x


if __name__ == "__main__":
    my_ip = sql_connect.get_ip_address()

    uvicorn.run("main:api", host=my_ip, port=3001, log_level="info", reload=False)
