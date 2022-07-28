#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

from datetime import datetime

import pandas as pd
import uvicorn
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from private import sql_connect
from app import slack_home_page, barcode_generator, slack_getters, slack_modal, create_final_image
from fastapi import FastAPI, Request
from private import credentials
import warnings
import time
from tqdm import tqdm
from private import sql3_conn
from private import pass_manager

warnings.simplefilter("ignore", UserWarning)

sql3_conn.main()
df =sql3_conn.read_token_for_slack()
app = App(signing_secret=pass_manager.decrypt(df['fernet'].values[0], df['secrete'].values[0]),
          token=df['token'].values[0])
app_handler = SlackRequestHandler(app)



@app.event("app_home_opened")
def publish_home_view(client, event, logger):
    entersoft_id = sql3_conn.main()
    user_info = slack_getters.get_user_details(event, client)
    # logger.error(f"User {user_info['user']['profile'].get('display_name')} clicked:  [Home Page]")
    try:
        client.views_publish(
            user_id=event["user"],
            view=slack_home_page.event(user_info, entersoft_id))
    except Exception as e:
        logger.error(f"Error publishing view to Home Tab: {e}")


@app.event("message")
def handle_message_events(body, logger, say):
    logger.info(body)


@app.action("action_id_barcode_generator")
def action_button_click(body, ack, say, logger, client):
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


@app.view("modal_button_triggered_barcode_generator")
def handle_submission(ack, body, client, view, logger, ):
    ack()
    try:
        # get user name
        user_info = slack_getters.get_modal_user_details(body, client)
        start_process_time_modal_button_triggered_barcode_generator = time.process_time()
        start_performance_time_modal_button_triggered_barcode_generator = time.perf_counter()
        print(
            f"🟢 Button Triggered on Home Page: Barcode Generator 💭 || By: {user_info['user']['profile'].get('display_name')} || TimeStamp: {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
        logger.info(body)
        # get keys from modal
        key = view['state'].get('values').keys()
        key = list(key)

        # get values from inputs
        type = view['state']['values'][key[0]]['pick_type_static_select_action']['selected_option'].get('value')
        number = int(view['state']['values'][key[1]]['pda_number_plain_text_input_action'].get('value'))
        store = str(view['state']['values'][key[2]]['pick_type_static_select_store']['selected_option'].get('value'))
        special_color = str(
            view['state']['values'][key[3]]['pick_type_static_select_paper_type']['selected_option'].get('value'))

        stores = ['EM', 'L1', 'L2']
        special_colors = ['WHITE', 'YELLOW']
        bg_colors = ['#61D839', '#6FBCF0']
        prices = ['RetailPrice', 'LATO 01', 'LATO 02']
        file_names = ['Elounda Market White.png', 'Elounda Market Yellow.png', 'Lato White.png', 'Lato Yellow.png']

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
        elif store == stores[1]:
            price = prices[1]
            bg_color = bg_colors[1]
            if special_color == special_colors[0]:
                file_name = file_names[2]
            elif special_color == special_colors[1]:
                file_name = file_names[3]
        elif store == stores[2]:
            price = prices[2]
            bg_color = bg_colors[1]
            if special_color == special_colors[0]:
                file_name = file_names[2]
            elif special_color == special_colors[1]:
                file_name = file_names[3]

        # run app
        df = barcode_generator.run(number, type, bg_color)
        for i in tqdm(df.BarCode.unique(), desc='Barcode Generator: Creating Final Images:'):
            create_final_image.run(df[df['BarCode'] == i], file_name, price)

    except Exception as e:
        logger.error(f"Error responding to 'first_button' button click: {e}")
        print(f"⭕️ Error on Home Page: Barcode Generator Button 💭")
    finally:
        stop_process_time_modal_button_triggered_barcode_generator = time.process_time()
        stop_performance_time_modal_button_triggered_barcode_generator = time.perf_counter()
        final_process_time_modal_button_triggered_barcode_generator = stop_process_time_modal_button_triggered_barcode_generator - start_process_time_modal_button_triggered_barcode_generator
        final_performance_time_modal_button_triggered_barcode_generator = stop_performance_time_modal_button_triggered_barcode_generator - start_performance_time_modal_button_triggered_barcode_generator
        print(
            f"🎉 END OF: Barcode Generator 💭 || By: {user_info['user']['profile'].get('display_name')} || TimeStamp: {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
        print(
            f"⌛️ Performance Time: {round(final_performance_time_modal_button_triggered_barcode_generator, 2)} sec || Process Time: {round(final_process_time_modal_button_triggered_barcode_generator, 2)}")


@app.view("modal_button_triggered_initialize_sql_settings")
def handle_submission(ack, body, client, view, logger, ):
    ack()
    try:
        # get user name
        user_info_initialize_sql = slack_getters.get_modal_user_details(body, client)
        start_process_time_modal_button_triggered_initialize_sql = time.process_time()
        start_performance_time_modal_button_triggered_initialize_sql = time.perf_counter()
        print(
            f"🟢 Button Triggered on Home Page: Initialize SQL Settings 💭 || By: {user_info_initialize_sql['user']['profile'].get('display_name')} || TimeStamp: {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
        logger.info(body)

        # get keys from modal
        key = view['state'].get('values').keys()
        key = list(key)

        sql_server_ip = str(view['state']['values'][key[0]]['sql_server_ip'].get('value'))
        sql_server_uid = str(view['state']['values'][key[1]]['sql_server_uid'].get('value'))
        f_sql_key, sql_server_password = pass_manager.encrypt(str(view['state']['values'][key[2]]['sql_server_password'].get('value')))
        sql_server_Database =str(view['state']['values'][key[3]]['sql_server_Database'].get('value'))
        sql_server_TrustServerCertificate =str(view['state']['values'][key[4]]['sql_server_TrustServerCertificate']['selected_option'].get('value'))

        vpn_name =str(view['state']['values'][key[5]]['vpn_name'].get('value'))
        f_vpn_key, vpn_secret = pass_manager.encrypt(str(view['state']['values'][key[6]]['vpn_secret'].get('value')))

        sql_data = (1, sql_server_ip,  sql_server_uid, sql_server_password, sql_server_Database, sql_server_TrustServerCertificate, f_sql_key)
        vpn_data = (1, vpn_name, vpn_secret, f_vpn_key )

        sql3_conn.insertVaribleIntoSqlTable(sql_data)
        sql3_conn.insertVaribleIntoVpnTable(vpn_data)

        #Store Data To database
        #TODO

    except Exception as e:
        logger.error(f"Error responding to 'first_button' button click: {e}")
        print(f"⭕️ Error on Home Page: Barcode Generator Button 💭")
    finally:
        stop_process_time_modal_button_triggered_initialize_sql = time.process_time()
        stop_performance_time_modal_button_triggered_initialize_sql = time.perf_counter()
        final_process_time_modal_button_triggered_initialize_sql = stop_process_time_modal_button_triggered_initialize_sql - start_process_time_modal_button_triggered_initialize_sql
        final_performance_time_modal_button_triggered_initialize_sql = stop_performance_time_modal_button_triggered_initialize_sql - start_performance_time_modal_button_triggered_initialize_sql
        print(
            f"🎉 END OF: Initialize SQL Settings 💭 || By: {user_info_initialize_sql['user']['profile'].get('display_name')} || TimeStamp: {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")
        print(
            f"⌛️ Performance Time: {round(final_performance_time_modal_button_triggered_initialize_sql, 2)} sec || Process Time: {round(final_process_time_modal_button_triggered_initialize_sql, 2)}")


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

    uvicorn.run("main:api", host=my_ip, port=3000, log_level="info", reload=True)
