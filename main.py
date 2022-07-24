import time
import uvicorn
from slack_bolt import App
from slack_bolt.adapter.fastapi import SlackRequestHandler
from private import credentials, sql_connect
from app import slack_home_page, barcode_generator
from fastapi import FastAPI, Request
from private import credentials

app = App(signing_secret=credentials.c['slack_credentials'].get('slack_secret'),
          token=credentials.c['slack_credentials'].get('slack_token'), )
app_handler = SlackRequestHandler(app)


@app.event("app_home_opened")
def publish_home_view(client, event, logger):
    """
    The Home tab is a persistent, yet dynamic interface for apps.
    The user can reach the App Home from the conversation list
    within Slack or by clicking on the app's name in messages.
    Note: you *must* enable Home Tab (App Home > Show Tabs Section)
    to receive this event.
    Please see the 'Event Subscriptions' and 'OAuth & Permissions'
    sections of your app's configuration to add the following:
    Event subscription(s):  app_home_opened
    Required scope(s):      none
    Further Information & Resources
    https://slack.dev/bolt-python/concepts#app-home
    https://api.slack.com/surfaces/tabs
    """
    # admin_users = [ΚΟΜΜΑΣ , ΛΟΓΙΣΤΗΡΙΟ]
    admin_users = credentials.slack_admin_users
    if event["user"] in admin_users:
        print(f'Admin User {event["user"]}')
        try:
            client.views_publish(
                user_id=event["user"],
                view=slack_home_page.admin_event(event))
        except Exception as e:
            logger.error(f"Error publishing view to Home Tab: {e}")
    else:
        print(f'Single User {event["user"]}')
        try:
            client.views_publish(
                user_id=event["user"],
                view=slack_home_page.no_auth(event))
        except Exception as e:
            logger.error(f"Error publishing view to Home Tab: {e}")


@app.event("message")
def handle_message_events(body, logger, say):
    logger.info(body)

@app.action("action_id_barcode_generator")
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)
    try:
        barcode_generator.delete_all_files_inside_folder()
        barcode_generator.app(['2234567891234', '22345678'])
    except Exception as e:
        logger.error(f"Error on Barcode Generator: {e}")

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

