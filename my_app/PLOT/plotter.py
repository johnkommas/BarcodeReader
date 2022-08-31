#  Copyright (c) Ioannis E. Kommas 2022. All Rights Reserved

import pathlib
import matplotlib.pyplot as plt
import seaborn as sns


def plot_activity(df):
    # --------------------- Parent Folder  ---------------------
    parent_path = pathlib.Path(__file__).parent.resolve()

    # --------------------- Dataframe Pivot  ---------------------
    df = df.pivot("UserName", "CHANNEL", "TIMES")

    # --------------------- ΤΙΤΛΟΣ  ---------------------
    name = 'CLICK ACTIVITY'

    # --------------------- ΠΡΟΕΤΟΙΜΑΣΙΑ ΓΡΑΦΗΜΑΤΟΣ ΔΙΑΣΤΑΣΕΙΣ ΓΡΑΦΗΜΑΤΟΣ ---------------------
    f, ax = plt.subplots(figsize=(19, 9))

    # --------------------- ΧΡΩΜΑΤΑ  ---------------------
    cmap = 'Blues'
    # cmap = sns.diverging_palette(133, 10, as_cmap=True)

    # --------------------- ΓΡΑΦΗΜΑ ---------------------
    sns.heatmap(df, annot=True, fmt='.2f', linewidths=1, ax=ax, cmap=cmap).set(title=f'{name}')

    # --------------------- ΕΝΤΟΛΗ ΕΜΦΑΝΙΣΗΣ ΓΡΑΦΗΜΑΤΟΣ ---------------------
    plt.tight_layout()
    plt.savefig(f'{parent_path}/images/user_activity_graph.png', transparent=True)

    # --------------------- ΕΝΤΟΛΗ ΚΛΕΙΣΙΜΑΤΟΣ ΓΡΑΦΗΜΑΤΟΣ (ΑΠΕΛΕΥΘΕΡΩΣΗ ΧΩΡΟΥ) ---------------------
    plt.close()
