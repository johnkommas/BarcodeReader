

def event(user_info):
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
                                                "text": "ΑΣ ΞΕΚΙΝΗΣΟΥΜΕ",
                                                "emoji": True
                                            },
                                            "style": "primary",
                                            "value": "value_barcode_generator",
                                            "action_id": "action_id_barcode_generator"
                                        },

                                    ]
                                }

    if user_info['user'].get('is_admin'):
        return {
                "type": "home",
                "blocks": [basic_user_info, divider, barcode_generator_section, barcode_generator_action, divider]
           }
    else:
        print("User is app user", user_info['user'])
        return {
            "type": "home",
            "blocks": [basic_user_info, divider, access_denied]
        }


