import time
from datetime import datetime
import uvicorn
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from private import credentials, sql_connect
from app import slack_home_page, barcode_generator, slack_getters
from fastapi import FastAPI, Request
from private import credentials

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
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)
    logger.error(f"🟢 {datetime.now().strftime('%d/%m/%y, %H:%M:%S')} || Barcode Generator Start || ")
    time_start_action_id_barcode_generator = time.perf_counter()
    try:
        barcode_generator.delete_all_files_inside_folder()
        barcode_generator.app(['4234567891234', '42345678'])
    except Exception as e:
        logger.error(f"Error on Barcode Generator: {e}")
    time_end_action_id_barcode_generator = time.perf_counter()
    time_diff_action_id_barcode_generator = time_end_action_id_barcode_generator - time_start_action_id_barcode_generator
    logger.error(f"🟢 {datetime.now().strftime('%d/%m/%y, %H:%M:%S')} || Barcode Generator Ended || 🎉 TOTAL TIME: {round(time_diff_action_id_barcode_generator, 2)} sec")


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

