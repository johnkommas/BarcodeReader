#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved
def action(text, value, action_id):
    return {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": text,
                    "emoji": True
                },
                "style": "primary",
                "value": value,
                "action_id": action_id
            },

        ]
    }


def double_action(text, value, action_id, text_2, value_2, action_id_2):
    return {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": text,
                    "emoji": True
                },
                "style": "primary",
                "value": value,
                "action_id": action_id
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": text_2,
                    "emoji": True
                },
                "style": "primary",
                "value": value_2,
                "action_id": action_id_2
            },
        ]
    }


def section(text, image_url):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        },
        "accessory": {
            "type": "image",
            "image_url": image_url,
            "alt_text": "apple"
        },

    }


def simple_section(text):
    return {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": text
        },

    }


def event(user_info, sql_status, activity):
    activity = activity.pivot("USER", "CHANNEL", "TIMES")
    activity = activity.fillna(0)

    profile = user_info['user']['profile']

    divider = {
        "type": "divider"
    }

    basic_user_info = section(
        text=f"<@{user_info['user'].get('id')}>\n{profile.get('title')} \n{profile.get('status_emoji')} _{profile.get('status_text')}_ \n",
        image_url=f"{profile.get('image_original')}")
    barcode_generator_section = simple_section(text="*Barcode Generator*\n_work in progress_")
    barcode_generator_action = double_action(text="ΚΑΝΟΝΙΚΕΣ ΤΙΜΕΣ", value="value_barcode_generator",
                                             action_id="action_id_barcode_generator",
                                             text_2="ΠΡΟΣΦΟΡΕΣ", value_2="value_special_price_list",
                                             action_id_2="action_id_special_price_list")
    entersoft_sql_section = simple_section(text="*Setup Entersoft SQL Server and VPN*\n_work in progress_")
    entersoft_sql_action = action(text="SQL & VPN SETUP", value="value_entersoft_sql",
                                  action_id="action_id_entersoft_sql")
    activity_section = simple_section(text=f"> *USER ACTIVITY ANALYTICS* \n{activity}")

    basic_block = [basic_user_info, divider, barcode_generator_section, barcode_generator_action, divider,
                   activity_section, divider]
    if user_info['user'].get('is_admin'):
        if sql_status:
            blocks = [basic_user_info, divider, entersoft_sql_section, entersoft_sql_action, divider]
        else:
            blocks = basic_block
        return {
            "type": "home",
            "blocks": blocks
        }
    else:
        # print("User is my_app user", user_info['user'])
        return {
            "type": "home",
            "blocks": basic_block
        }
