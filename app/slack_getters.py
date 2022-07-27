#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

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