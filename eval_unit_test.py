import unittest
import pandas as pd
import data_process


class MyTestCase(unittest.TestCase):
    data = pd.read_csv("./journey_example.csv", encoding="utf-8")

    # df_list = data_process.cut_df_avg(df_1_9_5, 1)
    ev = {
        "current_electricity": 5,
        "per_100km_electricity": 15,
        "max_electricity": 150,
        "charging_speed": 20
    }


    # def test_algo1_for_one_journey(self):
    #     data = pd.read_csv("./journey_example.csv", encoding="utf-8")
    #     user_ids = list(set(list(data["user_id"])))
    #     all_user_journeys = []
    #     for user_id in user_ids:
    #         user_journeys = data_process.get_journeys_by_user_id(data, user_id)
    #         all_user_journeys.append(user_journeys)
    #     print(all_user_journeys)

    def test_algo2_for_one_journey(self):
        print(2)

    def test_algo1_for_two_journey(self):
        print(3)

    def test_algo2_for_two_journey(self):
        print(4)


if __name__ == '__main__':
    data = pd.read_csv("./journey_example.csv", encoding="utf-8")
    df_list = data_process.cut_df_avg(data, 2)
    for journey in df_list:
        print(journey)