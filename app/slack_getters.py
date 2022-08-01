#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved
from asyncio.log import logger

from private import sql3_conn
from app import slack_home_page


def get_user_details(event, client):
    user_id = event["user"]
    try:
        result = client.users_info(user=user_id)
        return result
        # EXAMPLES
        # profile = result['user']['profile']
        # profile.get['display_name'],
        # profile.get('title'),
        # profile.get['image_original'],
        # profile.get('status_text'),
        # profile.get('status_emoji')
    except Exception as e:
        print(e)


def get_modal_user_details(body, client):
    user_id = body['user'].get('id')
    try:
        result = client.users_info(user=user_id)
        return result
        # EXAMPLES
        # profile = result['user']['profile']
        # profile.get['display_name'],
        # profile.get('title'),
        # profile.get['image_original'],
        # profile.get('status_text'),
        # profile.get('status_emoji')
    except Exception as e:
        print(e)


def refresh_home_page(client, user):
    # refresh home page
    entersoft_id = sql3_conn.main()
    try:
        client.views_publish(
            user_id=user["user"].get('id'),
            view=slack_home_page.event(user, entersoft_id, sql3_conn.read_activity()))
    except Exception as e:
        logger.error(f"Error publishing view to Home Tab: {e}")