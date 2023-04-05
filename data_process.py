import pandas as pd

import eval_f
import functions
import utils


def load_data():
    journeys = pd.read_csv("./journeys_v2_nurse.csv", encoding="utf-8")
    # journeys = pd.read_excel('./journeys_v2.csv', sheet_name='Sheet1')
    journey, ev = process_journeys(journeys)
    return journey, ev


# todo get journey(s) in the next 48h
def process_journeys(journeys):
    journeys = journeys.copy()
    journeys['departure'] = journeys.apply(
        lambda row: utils.formatTimeFromCsv(row['departure_date'] + " " + row['departure_time']), axis=1)
    journeys = journeys.copy()
    journeys['plug_in'] = journeys.apply(
        lambda row: utils.formatTimeFromCsv(row['plug_in_date'] + " " + row['plug_in_time']), axis=1)

    journeys = journeys.sort_values(by=["plug_in"], ascending=True)
    first_plug_in_time = journeys["plug_in"].tolist()[0]
    time_48h = utils.time_plus_minutes(first_plug_in_time, 48 * 60)
    journey_48h = journeys.loc[journeys["departure"] <= time_48h]
    journey_ids = journey_48h["journey_id"].tolist()
    plug_in_times = journey_48h["plug_in"].tolist()
    departure_times = journey_48h["departure"].tolist()
    required_electricity = journey_48h["distance"].tolist()
    user_type = journey_48h["user_type"].tolist()[0]
    user_id = journey_48h["user_id"].tolist()[0]

    journey = {
        "plug_in_times": plug_in_times,
        "departure_times": departure_times,
        "required_electricity": required_electricity,
        "journey_ids": journey_ids,
        "user_type": user_type,
        "user_id": user_id
    }

    ev = {
        "current_electricity": 5,
        "per_100km_electricity": 15,
        "max_electricity": 150,
        "charging_speed": 20
    }

    return journey, ev


file_path = "./journey_example.csv"


def get_journeys_by_user_id(journeys, user_id):
    return journeys[journeys.user_id == user_id]


def load_data_2(journeys):
    journey, ev = process_journeys(journeys)
    return journey, ev


def cut_df_avg(df, n):
    df = df.sort_values(by=["user_id", "plug_in_date", "plug_in_time"], ascending=True)
    df_list = []
    for i in range(0, len(df), n):
        df_list.append(df[i:i + n])
    return df_list


if __name__ == '__main__':
    journeys = pd.read_csv("./journey_example_test1.csv", encoding="utf-8")
    journeys = journeys.sort_values(by=["user_id", "plug_in_date", "plug_in_time"], ascending=True)
    print(journeys)
