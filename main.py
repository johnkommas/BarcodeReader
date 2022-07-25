import time
from datetime import datetime

import pandas as pd
import uvicorn
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from private import credentials, sql_connect
from app import slack_home_page, barcode_generator, slack_getters, slack_modal
from fastapi import FastAPI, Request
from private import credentials
import warnings
warnings.simplefilter("ignore", UserWarning)

app = App(signing_secret=credentials.c['slack_credentials'].get('slack_secret'),
          token=credentials.c['slack_credentials'].get('slack_token'), )
app_handler = SlackRequestHandler(app)


@app.event("app_home_opened")
def publish_home_view(client, event, logger):
    user_info = slack_getters.get_user_details(event, client)
    # logger.error(f"User {user_info['user']['profile'].get('display_name')} clicked:  [Home Page]")
    try:
        client.views_publish(
            user_id=event["user"],
            view=slack_home_page.event(user_info))
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


@app.view("modal_button_triggered_barcode_generator")
def handle_submission(ack, body, client, view, logger,):
    ack()
    number = 'ΕΣΦΑΛΜΕΝΗ ΤΙΜΗ'
    try:
        # get user name
        user_info = slack_getters.get_modal_user_details(body, client)
        print(f"🟢 Button Triggered on Home Page: Barcode Generator 💭 || By: {user_info['user']['profile'].get('display_name')} || TimeStamp: {datetime.now().strftime('%d/%m/%y %H:%M:%S')}")

        logger.info(body)
        #get keys from modal
        key = view['state'].get('values').keys()
        key = list(key)

        # get values from inputs
        type = view['state']['values'][key[0]]['pick_type_static_select_action']['selected_option'].get('value')
        number = int(view['state']['values'][key[1]]['pda_number_plain_text_input_action'].get('value'))

        # run app
        barcode_generator.run(number, type)

    except Exception as e:
        logger.error(f"Error responding to 'first_button' button click: {e}")
        print(f"⭕️ Error on Home Page: Barcode Generator Button 💭")


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

