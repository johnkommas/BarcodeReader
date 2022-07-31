#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

def event(user_info, sql_status, activity):
    profile = user_info['user']['profile']

    divider = {
        "type": "divider"
    }

    basic_user_info = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f"<@{user_info['user'].get('id')}> \n"
                    f"{profile.get('title')}  \n"
                    f"{profile.get('status_emoji')} _{profile.get('status_text')}_ \n"

        },
        "accessory": {
            "type": "image",
            "image_url": f"{profile.get('image_original')}",
            "alt_text": "apple"
        },
    }

    access_denied = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": " Έχετε περιορισμένη πρόσβαση σε αυτήν την σελίδα. \n"
                    " Για παραχώρηση δικαιωμάτων, παρακαλώ επικοινωνήστε με τον διαχειριστή \n"

        },

    }

    barcode_generator_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Barcode Generator*\n"
                    "_work in progress_"
        },

    }

    barcode_generator_action = {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "ΚΑΝΟΝΙΚΕΣ ΤΙΜΕΣ",
                    "emoji": True
                },
                "style": "primary",
                "value": "value_barcode_generator",
                "action_id": "action_id_barcode_generator"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "ΠΡΟΣΦΟΡΕΣ",
                    "emoji": True
                },
                "style": "primary",
                "value": "value_special_price_list",
                "action_id": "action_id_special_price_list"
            },

        ]
    }

    entersoft_sql_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": "*Setup Entersoft SQL Server and VPN*\n"
                    "_work in progress_"
        },

    }

    entersoft_sql_action = {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "SQL & VPN SETUP",
                    "emoji": True
                },
                "style": "primary",
                "value": "value_entersoft_sql",
                "action_id": "action_id_entersoft_sql"
            },

        ]
    }

    activity_section = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": f'{activity.pivot("USER", "CHANNEL", "TIMES")}'
        },

    }

    if user_info['user'].get('is_admin'):
        if sql_status:
            blocks = [basic_user_info, divider, entersoft_sql_section, entersoft_sql_action, divider]
        else:
            blocks = [basic_user_info, divider, barcode_generator_section, barcode_generator_action, divider, activity_section]
        return {
            "type": "home",
            "blocks": blocks
        }
    else:
        print("User is app user", user_info['user'])
        return {
            "type": "home",
            "blocks": [basic_user_info, divider, access_denied]
        }
