#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved


from datetime import datetime


def modal_view():
    return {
        "type": "modal",
        "callback_id": "modal_button_triggered_barcode_generator",
        "title": {
            "type": "plain_text",
            "text": "ΔΗΜΙΟΥΡΓΙΑ BARCODE",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Αποστολή",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Άκυρο",
            "emoji": True
        },
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "ΕΠΙΛΕΞΕ ΤΟΝ ΤΥΠΟ ΠΑΡΑΣΤΑΤΙΚΟΥ",
                        "emoji": True
                    },
                    "initial_option": {"text": {"type": "plain_text",
                                                "text": f"ΑΠ_ΜΟΒ: \t\t (ΔΕΛΤΙΟ ΑΠΟΓΡΑΦΗΣ)",
                                                "emoji": True
                                                },
                                       "value": f"ΑΠ_ΜΟΒ"},

                    "options": [{"text": {"type": "plain_text",
                                          "text": f"ΔΕΑ: \t\t\t\t (ΔΕΛΤΙΟ ΕΠΙΣΤΡΟΦΗΣ ΑΓΟΡΩΝ)",
                                          "emoji": True
                                          },
                                 "value": f"ΔΕΑ"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": f"ΠΠΡ: \t\t\t\t (ΠΑΡΑΓΓΕΛΙΑ ΑΓΟΡΑΣ)",
                                          "emoji": True
                                          },
                                 "value": f"ΠΠΡ"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": f"ΑΠ_ΜΟΒ: \t\t (ΔΕΛΤΙΟ ΑΠΟΓΡΑΦΗΣ)",
                                          "emoji": True
                                          },
                                 "value": f"ΑΠ_ΜΟΒ"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": f"ΔΕN: \t\t\t\t (ΔΕΛΤΙΟ ΕΝΔΟΔΙΑΚΙΝΗΣΗΣ)",
                                          "emoji": True
                                          },
                                 "value": f"ΔΕΝ"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": f"ΠΕΝ: \t\t\t\t (ΠΑΡΑΓΓΕΛΙΑ ΕΝΔΟΔΙΑΚΙΝΗΣΗΣ)",
                                          "emoji": True
                                          },
                                 "value": f"ΠΕΝ"
                                 },

                                {"text": {"type": "plain_text",
                                          "text": f"ΑΔΠ: \t\t\t\t (ΔΕΛΤΙΟ ΠΑΡΑΛΑΒΗΣ ΑΓΟΡΩΝ)",
                                          "emoji": True
                                          },
                                 "value": f"ΑΔΠ"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": f"ΑΤΔ: \t\t\t\t (ΤΙΜΟΛΟΓΙΟ ΔΕΛΤΙΟ ΠΑΡΑΛΑΒΗΣ)",
                                          "emoji": True
                                          },
                                 "value": f"ΑΤΔ"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": f"ΑΠΑΠ: \t\t\t (ΤΙΜΟΛΟΓΙΟ ΑΓΡΟΤΙΚΩΝ ΠΡΟΪΟΝΤΩΝ)",
                                          "emoji": True
                                          },
                                 "value": f"ΑΠΑΠ"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": f"ΑΧΔ: \t\t\t\t (ΔΕΛΤΙΟ ΠΑΡΑΛΑΒΗΣ ΧΩΡΙΣ ΧΡΕΩΣΗ)",
                                          "emoji": True
                                          },
                                 "value": f"ΑΧΔ"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": f"ΠΔΣ: \t\t\t\t (ΔΕΣΜΕΥΣΗ ΑΠΟΘΕΜΑΤΟΣ ΓΙΑ ΠΕΛΑΤΗ)",
                                          "emoji": True
                                          },
                                 "value": f"ΠΔΣ"
                                 },

                                ],

                    "action_id": "pick_type_static_select_action"
                },
                "label": {
                    "type": "plain_text",
                    "text": "ΕΠΙΛΕΞΕ ΤΟΝ ΤΥΠΟ ΤΟΥ ΠΑΡΑΣΤΑΤΙΚΟΥ:",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "pda_number_plain_text_input_action"
                },
                "label": {
                    "type": "plain_text",
                    "text": " ΠΛΗΚΤΡΟΛΟΓΗΣΕ ΤΟΝ ΑΡΙΘΜΟ ΤΟΥ ΠΑΡΑΣΤΑΤΙΚΟΥ:",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "ΕΠΙΛΕΞΕ ΥΠΟΚΑΤΑΣΤΗΜΑ",
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {"type": "plain_text",
                                 "text": "ELOUNDA MARKET",
                                 "emoji": True
                                 },
                        "value": "EM"
                    },
                    "options": [{"text": {"type": "plain_text",
                                          "text": "ELOUNDA MARKET",
                                          "emoji": True
                                          },
                                 "value": "EM"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": "LATO 01",
                                          "emoji": True
                                          },
                                 "value": "L1"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": "LATO 02",
                                          "emoji": True
                                          },
                                 "value": "L2"
                                 },
                                ],

                    "action_id": "pick_type_static_select_store"

                },
                "label": {
                    "type": "plain_text",
                    "text": "ΕΠΙΛΕΞΕ ΥΠΟΚΑΤΑΣΤΗΜΑ:",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "ΕΠΙΛΕΞΕ ΤΥΠΟ ΧΑΡΤΙΟΥ",
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {"type": "plain_text",
                                 "text": "ΛΕΥΚΟ",
                                 "emoji": True
                                 },
                        "value": "WHITE"

                    },
                    "options": [{"text": {"type": "plain_text",
                                          "text": "ΛΕΥΚΟ",
                                          "emoji": True
                                          },
                                 "value": "WHITE"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": "ΚΙΤΡΙΝΟ",
                                          "emoji": True
                                          },
                                 "value": "YELLOW"
                                 },

                                ],

                    "action_id": "pick_type_static_select_paper_type"
                },
                "label": {
                    "type": "plain_text",
                    "text": "ΕΠΙΛΕΞΕ ΤΥΠΟ ΧΑΡΤΙΟΥ:",
                    "emoji": True
                }
            },

        ]
    }


def sql_modal_view():
    return {
        "type": "modal",
        "callback_id": "modal_button_triggered_initialize_sql_settings",
        "title": {
            "type": "plain_text",
            "text": "INITIALIZE CREDENTIALS",
            "emoji": True
        },
        "submit": {
            "type": "plain_text",
            "text": "Αποστολή",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "Άκυρο",
            "emoji": True
        },
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sql_server_ip"
                },
                "label": {
                    "type": "plain_text",
                    "text": " SQL SERVER IP:",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "initial_value": "sa",
                    "action_id": "sql_server_uid"
                },
                "label": {
                    "type": "plain_text",
                    "text": " SQL SERVER UID:",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sql_server_password"
                },
                "label": {
                    "type": "plain_text",
                    "text": " SQL SERVER PASS:",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sql_server_Database"
                },
                "label": {
                    "type": "plain_text",
                    "text": " SQL SERVER DATABASE:",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "sql_server_TrustServerCertificate",
                        "emoji": True
                    },
                    "initial_option": {
                        "text": {"type": "plain_text",
                                 "text": "NO",
                                 "emoji": True
                                 },
                        "value": "no"

                    },
                    "options": [{"text": {"type": "plain_text",
                                          "text": "YEs",
                                          "emoji": True
                                          },
                                 "value": "yes"
                                 },
                                {"text": {"type": "plain_text",
                                          "text": "NO",
                                          "emoji": True
                                          },
                                 "value": "no"
                                 },

                                ],

                    "action_id": "sql_server_TrustServerCertificate"
                },
                "label": {
                    "type": "plain_text",
                    "text": "SQL SERVER TrustServerCertificate",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "vpn_name"
                },
                "label": {
                    "type": "plain_text",
                    "text": " VPN NAME:",
                    "emoji": True
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "vpn_secret"
                },
                "label": {
                    "type": "plain_text",
                    "text": " VPN SECRET:",
                    "emoji": True
                }
            },

        ]
    }


def special_offer_modal():
    set_today = datetime.now().strftime('%Y-%m-%d')
    return {
        "type": "modal",
        "callback_id": "modal_button_triggered_special_offer",
        "submit": {
            "type": "plain_text",
            "text": "GO!",
            "emoji": True
        },
        "close": {
            "type": "plain_text",
            "text": "ΆΚΥΡΟ",
            "emoji": True
        },
        "title": {
            "type": "plain_text",
            "text": "ΕΙΔΙΚΕΣ ΠΡΟΣΦΟΡΕΣ",
            "emoji": True
        },
        "blocks": [
            {
                "type": "input",
                "element": {
                    "type": "datepicker",
                    "initial_date": f"{set_today}",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a date",
                        "emoji": True
                    },
                    "action_id": "special_offer_datepicker_action_from"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Από Ημερομηνία:",
                    "emoji": True
                }
            },
        ]
    }
