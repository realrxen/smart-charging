import json

import pandas as pd
from pandas import DataFrame

import data_process
import eval_algo
import utils


# algo1 for one journey
def test_algo1_for_one_journey(data, ev, journey_number):
    df_list = data_process.cut_df_avg(data, journey_number)
    output_list = []
    for journey in df_list:
        journey = journey.to_json(orient='records')
        journey_obj = json.loads(journey)[0]
        output = eval_algo.algo1_for_one_journey(journey_obj, ev)
        output_list.append(output)
    output_df = DataFrame(output_list,
                          columns=["user_id", "journey_id", "plug_in_time", "departure_time", "time_slot",
                                   "carbon_emission", "avg_carbon_emission", "total_demand", "charging_duration",
                                   "user_type"])
    output_df.to_csv("./output_algo1_" + str(journey_number) + "journey.csv", index=False)


def test_algo2_for_one_journey(data, ev, journey_number):
    df_list = data_process.cut_df_avg(data, journey_number)
    output_list = []
    for journey in df_list:
        journey = journey.to_json(orient='records')
        journey_obj = json.loads(journey)[0]
        output = eval_algo.algo2_for_one_journey(journey_obj, ev)
        output_list.append(output)
    output_df = DataFrame(output_list,
                          columns=["user_id", "journey_id", "plug_in_time", "departure_time", "time_slot",
                                   "carbon_emission", "avg_carbon_emission", "total_demand", "charging_duration",
                                   "user_type"])
    output_df.to_csv("./output_algo2_" + str(journey_number) + "journey.csv", index=False)


def test_algo1_for_two_journey(data, journey_number):
    user_ids = list(set(list(data["user_id"])))
    all_user_journeys = []
    for user_id in user_ids:
        user_journeys = data_process.get_journeys_by_user_id(data, user_id)
        all_user_journeys.append(user_journeys)
    final_df = DataFrame([], columns=["user_id", "journey_ids", "plug_in_time", "departure_time", "time_slot",
                                      "carbon_emission", "avg_carbon_emission",
                                      "avg_priority_carbon_emission", "total_demand", "charging_duration", "user_type"])

    for user_journeys in all_user_journeys:
        user_two_journeys_list = data_process.cut_df_avg(user_journeys, journey_number)
        output_list = []
        for two_journey in user_two_journeys_list:
            journey, ev = data_process.load_data_2(two_journey)
            output = eval_algo.algo1_for_two_journey(journey, ev)
            output_list.append(output)
        output_df = DataFrame(output_list,
                              columns=["user_id", "journey_ids", "plug_in_time", "departure_time", "time_slot",
                                       "carbon_emission", "avg_carbon_emission",
                                       "avg_priority_carbon_emission", "total_demand", "charging_duration",
                                       "user_type"])
        final_df = final_df.append(output_df)
    final_df.to_csv("./output_algo1_" + str(journey_number) + "journey.csv", index=False)


def test_algo2_for_two_journey(data, journey_number):
    user_ids = list(set(list(data["user_id"])))
    all_user_journeys = []
    for user_id in user_ids:
        user_journeys = data_process.get_journeys_by_user_id(data, user_id)
        all_user_journeys.append(user_journeys)
    final_df = DataFrame([], columns=["user_id", "journey_ids", "plug_in_time", "departure_time", "time_slot",
                                      "carbon_emission", "avg_carbon_emission",
                                      "avg_priority_carbon_emission", "total_demand", "charging_duration", "user_type"])
    for user_journeys in all_user_journeys:
        user_two_journeys_list = data_process.cut_df_avg(user_journeys, journey_number)
        output_list = []
        for two_journey in user_two_journeys_list:
            journey, ev = data_process.load_data_2(two_journey)
            output = eval_algo.algo2_for_two_journey(journey, ev)
            output_list.append(output)
        output_df = DataFrame(output_list,
                              columns=["user_id", "journey_ids", "plug_in_time", "departure_time", "time_slot",
                                       "carbon_emission", "avg_carbon_emission",
                                       "avg_priority_carbon_emission", "total_demand", "charging_duration",
                                       "user_type"])
        final_df = final_df.append(output_df)
    final_df.to_csv("./output_algo2_" + str(journey_number) + "journey.csv", index=False)


def test_dumb_charging_for_one_journey(data, ev, journey_number):
    df_list = data_process.cut_df_avg(data, journey_number)
    output_list = []
    for journey in df_list:
        journey = journey.to_json(orient='records')
        journey_obj = json.loads(journey)[0]
        output = eval_algo.dumb_charging_for_one_journey(journey_obj, ev)
        output_list.append(output)
    output_df = DataFrame(output_list,
                          columns=["user_id", "journey_id", "plug_in_time", "departure_time", "time_slot",
                                   "carbon_emission", "avg_carbon_emission", "total_demand", "charging_duration",
                                   "user_type"])
    output_df.to_csv("./output_dumb_charging_" + str(journey_number) + "journey.csv", index=False)


def test_dumb_charging_for_two_journey(data, journey_number):
    user_ids = list(set(list(data["user_id"])))
    all_user_journeys = []
    for user_id in user_ids:
        user_journeys = data_process.get_journeys_by_user_id(data, user_id)
        all_user_journeys.append(user_journeys)
    final_df = DataFrame([], columns=["user_id", "journey_ids", "plug_in_time", "departure_time", "time_slot",
                                      "carbon_emission", "avg_carbon_emission",
                                      "avg_priority_carbon_emission", "total_demand", "charging_duration", "user_type"])
    for user_journeys in all_user_journeys:
        user_two_journeys_list = data_process.cut_df_avg(user_journeys, journey_number)
        output_list = []
        for two_journey in user_two_journeys_list:
            journey, ev = data_process.load_data_2(two_journey)
            output = eval_algo.dumb_charging_for_two_journey(journey, ev)
            output_list.append(output)
        output_df = DataFrame(output_list,
                              columns=["user_id", "journey_ids", "plug_in_time", "departure_time", "time_slot",
                                       "carbon_emission", "avg_carbon_emission",
                                       "avg_priority_carbon_emission", "total_demand", "charging_duration",
                                       "user_type"])
        final_df = final_df.append(output_df)
    final_df.to_csv("./output_dumb_charging_" + str(journey_number) + "journey.csv", index=False)


if __name__ == '__main__':
    data = pd.read_csv("./journey_final2.csv", encoding="utf-8")

    ev = {
        "current_electricity": 5,
        "per_100km_electricity": 15,
        "max_electricity": 150,
        "charging_speed": 20
    }
    # test_algo1_for_one_journey(data, ev, 1)
    # test_algo2_for_one_journey(data, ev, 1)
    # test_dumb_charging_for_one_journey(data, ev, 1)

    # test_algo1_for_two_journey(data, 2)
    # test_algo2_for_two_journey(data, 2)
    # test_dumb_charging_for_two_journey(data, 2)

    # test_algo1_for_two_journey(data, 3)
    # test_algo2_for_two_journey(data, 3)
    # test_dumb_charging_for_two_journey(data, 3)
