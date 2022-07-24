from app import slack_face

def admin_event(event):
    user_id = event['user']
    face = slack_face.admin_photo(user_id)
    return {
        "type": "home",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Barcode Generator*"
                },
                "accessory": {
                    "type": "image",
                    "image_url": f"https://github.com/johnkommas/CodeCademy_Projects/blob/master/img/{face}?raw=true",
                    "alt_text": "apple"
                },
            },
                {
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
                },

            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": ":pushpin: Ο φάκελος *BPO_RESULTS* είναι σε κοινή χρήση με τον χρήστη: _*eloundamarket@outlook.com*_"

                },
                # "accessory": {
                #     "type": "image",
                #     "image_url": f"https://github.com/johnkommas/CodeCademy_Projects/blob/master/img/{face}?raw=true",
                #     "alt_text": "apple"
                # },
            },
            {
                "type": "divider"
            },

        ]
    }


def no_auth(event):
    return {
        "type": "home",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"""*Καλώς Ορίσατε, <@{event['user']}> :house:*
    Ζητούμε συγνώμη για την αναστάτωση αλλά δεν σας βρίσκουμε στην Βάση Δεδομένων μας.
    Παρακαλώ επικοινωνήστε με τον διαχειριστή. 
    """
                }
            }]}
