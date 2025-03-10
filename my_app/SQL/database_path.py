#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

import pathlib


def run():
    parent_path = pathlib.Path(__file__).parent.resolve()
    database = f"{parent_path}/Business.db"
    return database