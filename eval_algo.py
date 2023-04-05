import json
import pandas as pd
from pandas import DataFrame

import DumbCharging
import SmartCharging
import data_process
import functions
import utils
import eval_f


# Smart Charging Algorithm1 for one journey
def algo1_for_one_journey(journey, ev):
    user_id = journey["user_id"]
    journey_id = journey["journey_id"]
    print(journey_id)
    journey_type = journey["user_type"]
    distance = journey["distance"]
    total_demand = distance * ev["per_100km_electricity"] / 100 * 2
    # 充电的电量要求 旅程需要的电量-当前的电量
    if not eval_f.check_demand(total_demand, ev, 1):
        return []
    plug_in_time = utils.formatTimeFromCsv(journey["plug_in_date"] + " " + journey["plug_in_time"])
    print(plug_in_time)
    departure_time = utils.formatTimeFromCsv(journey["departure_date"] + " " + journey["departure_time"])
    print(departure_time)
    charging_duration = eval_f.get_charging_duration(total_demand, ev, plug_in_time,
                                                     departure_time, 1)
    data = functions.get_next48h_intensity(utils.str2iso(plug_in_time))
    time_slot, carbon_emission = SmartCharging.algo1(plug_in_time, departure_time, charging_duration, data)
    print("algo1 time slot : ", time_slot)
    # print("algo1 carbon_emission :", carbon_emission)
    # print("algo1 avg carbon emission : ", carbon_emission / charging_duration, "/ minute")
    avg_carbon_emission = carbon_emission / charging_duration
    return [user_id, journey_id, plug_in_time, departure_time, time_slot, carbon_emission, avg_carbon_emission,
            total_demand,
            charging_duration, journey_type]


def algo2_for_one_journey(journey, ev):
    user_id = journey["user_id"]
    journey_id = journey["journey_id"]
    # print(journey_id)
    user_type = journey["user_type"]
    distance = journey["distance"]
    total_demand = distance * ev["per_100km_electricity"] / 100 * 2
    # 充电的电量要求 旅程需要的电量-当前的电量
    if not eval_f.check_demand(total_demand, ev, 1):
        return []
    plug_in_time = utils.formatTimeFromCsv(journey["plug_in_date"] + " " + journey["plug_in_time"])
    # print(plug_in_time)
    departure_time = utils.formatTimeFromCsv(journey["departure_date"] + " " + journey["departure_time"])
    # print(departure_time)
    charging_duration = eval_f.get_charging_duration(total_demand, ev, plug_in_time,
                                                     departure_time, 1)
    data = functions.get_next48h_intensity(utils.str2iso(plug_in_time))
    time_slot, carbon_emission = SmartCharging.algo2(plug_in_time, departure_time, charging_duration, data)
    time_slot = utils.merge_slots(time_slot, [])
    time_slot_str = ""
    for slot in time_slot:
        time_slot_str = time_slot_str + slot + ","
    print("time_slot:", time_slot)
    avg_carbon_emission = carbon_emission / charging_duration
    print("=========" * 10)
    return [user_id, journey_id, plug_in_time, departure_time, time_slot_str, carbon_emission, avg_carbon_emission,
            total_demand,
            charging_duration, user_type]


def algo1_for_two_journey(journey, ev):
    emissions = []
    minutes = []
    user_id = journey["user_id"]
    journey_ids = journey["journey_ids"]
    user_type = journey["user_type"]
    print("journey_id:", journey_ids)
    journey_number = len(journey_ids)
    print(journey_number)
    required_electricity = journey["required_electricity"]
    print("required_distance:", sum(required_electricity), "km")
    journeys_demand = sum(required_electricity) * ev["per_100km_electricity"] / 100 * 2
    # 充电的电量要求 旅程需要的电量-当前的电量
    total_demand = journeys_demand
    if not eval_f.check_demand(total_demand, ev, journey_number):
        return []
    plug_in_times = journey["plug_in_times"]
    departure_times = journey["departure_times"]
    charging_duration = eval_f.get_charging_duration(total_demand, ev, plug_in_times[0],
                                                     departure_times[0], journey_number)
    plug_in_time = journey["plug_in_times"][0]
    print("plug_in_time: ", plug_in_time)
    departure_time = journey["departure_times"][0]
    data = functions.get_next48h_intensity(utils.str2iso(plug_in_time))
    time_slot, carbon_emission = SmartCharging.algo1(plug_in_time, departure_time, charging_duration, data)
    print("algo1 time slot : ", time_slot)
    print("algo1 carbon_emission :", carbon_emission)
    print("algo1 avg carbon emission : ", carbon_emission / charging_duration, "/ minute")
    emissions.append(carbon_emission)
    minutes.append(charging_duration)
    print("================" * 5)
    avg_priority_emission = functions.calculate_avg_priority_emission(emissions, minutes, journey_number)
    print('\033[0;36mavg_priority_emission is ' + str(avg_priority_emission) + '\033[0m')
    return [user_id,journey_ids, plug_in_time, departure_time, time_slot, carbon_emission, carbon_emission / charging_duration,
            avg_priority_emission,
            total_demand,
            charging_duration,user_type]


def algo2_for_two_journey(journey, ev):
    emissions = []
    minutes = []
    user_id = journey["user_id"]
    journey_ids = journey["journey_ids"]
    print("journey_id:", journey_ids)
    user_type = journey["user_type"]
    journey_number = len(journey_ids)
    print(journey_number)
    required_electricity = journey["required_electricity"]
    print("required_distance:", sum(required_electricity), "km")
    journeys_demand = sum(required_electricity) * ev["per_100km_electricity"] / 100 * 2

    total_demand = journeys_demand
    if not eval_f.check_demand(total_demand, ev, journey_number):
        return []
    plug_in_times = journey["plug_in_times"]
    departure_times = journey["departure_times"]
    charging_duration = eval_f.get_charging_duration(total_demand, ev, plug_in_times[0],
                                                     departure_times[0], journey_number)
    plug_in_time = journey["plug_in_times"][0]
    print("plug_in_time: ", plug_in_time)
    departure_time = journey["departure_times"][0]
    data = functions.get_next48h_intensity(utils.str2iso(plug_in_time))
    time_slot, carbon_emission = SmartCharging.algo2(plug_in_time, departure_time, charging_duration, data)
    print("merged algo2 time slot :", utils.merge_slots(time_slot, [], 0, 0))
    time_slot = utils.merge_slots(time_slot, [], 0, 0)
    time_slot_str = ""
    for slot in time_slot:
        time_slot_str = time_slot_str + slot + ","
    print("algo1 carbon_emission :", carbon_emission)
    print("algo1 avg carbon emission : ", carbon_emission / charging_duration, "/ minute")
    emissions.append(carbon_emission)
    minutes.append(charging_duration)
    print("================" * 5)
    avg_priority_emission = functions.calculate_avg_priority_emission(emissions, minutes, journey_number)
    print('\033[0;36mavg_priority_emission is ' + str(avg_priority_emission) + '\033[0m')
    return [user_id,journey_ids, plug_in_time, departure_time, time_slot_str, carbon_emission,
            carbon_emission / charging_duration,
            avg_priority_emission,
            total_demand,
            charging_duration, user_type]


def dumb_charging_for_one_journey(journey, ev):
    user_id = journey["user_id"]
    journey_id = journey["journey_id"]
    # print(journey_id)
    user_type = journey["user_type"]
    distance = journey["distance"]
    total_demand = distance * ev["per_100km_electricity"] / 100 * 2

    if not eval_f.check_demand(total_demand, ev, 1):
        return []
    plug_in_time = utils.formatTimeFromCsv(journey["plug_in_date"] + " " + journey["plug_in_time"])
    # print(plug_in_time)
    departure_time = utils.formatTimeFromCsv(journey["departure_date"] + " " + journey["departure_time"])
    # print(departure_time)
    charging_duration = eval_f.get_charging_duration(total_demand, ev, plug_in_time,
                                                     departure_time, 1)
    data = functions.get_next48h_intensity(utils.str2iso(plug_in_time))
    time_slot, carbon_emission = DumbCharging.algo(plug_in_time, departure_time, charging_duration, data)
    print("time_slot:", time_slot)
    print("carbon_emission", carbon_emission)
    avg_carbon_emission = carbon_emission / charging_duration
    return [user_id, journey_id, plug_in_time, departure_time, time_slot, carbon_emission, avg_carbon_emission,
            total_demand,
            charging_duration, user_type]


def dumb_charging_for_two_journey(journey, ev):
    emissions = []
    minutes = []
    user_id = journey["user_id"]
    journey_ids = journey["journey_ids"]
    user_type = journey["user_type"]
    journey_number = len(journey_ids)
    print("journey_id:", journey_ids)
    required_electricity = journey["required_electricity"]
    print("required_distance:", sum(required_electricity), "km")
    journeys_demand = sum(required_electricity) * ev["per_100km_electricity"] / 100 * 2

    total_demand = journeys_demand
    if not eval_f.check_demand(total_demand, ev, journey_number):
        return []
    plug_in_times = journey["plug_in_times"]
    departure_times = journey["departure_times"]
    charging_duration = eval_f.get_charging_duration(total_demand, ev, plug_in_times[0],
                                                     departure_times[0], journey_number)
    plug_in_time = journey["plug_in_times"][0]
    print("plug_in_time: ", plug_in_time)
    departure_time = journey["departure_times"][0]
    data = functions.get_next48h_intensity(utils.str2iso(plug_in_time))
    time_slot, carbon_emission = DumbCharging.algo(plug_in_time, departure_time, charging_duration, data)
    print("dumb algo carbon_emission :", carbon_emission)
    print("dumb algo avg carbon emission : ", carbon_emission / charging_duration, "/ minute")
    emissions.append(carbon_emission)
    minutes.append(charging_duration)
    print("================" * 5)
    avg_priority_emission = functions.calculate_avg_priority_emission(emissions, minutes, journey_number)
    print('\033[0;36mavg_priority_emission is ' + str(avg_priority_emission) + '\033[0m')
    return [user_id,journey_ids, plug_in_time, departure_time, time_slot, carbon_emission, carbon_emission / charging_duration,
            avg_priority_emission,
            total_demand,
            charging_duration,user_type]


if __name__ == '__main__':
    # file_path = "./journeys_v2_nurse.csv"
    data = pd.read_csv("./journey_example.csv", encoding="utf-8")

    # df_list = data_process.cut_df_avg(df_1_9_5, 1)
    df_list = data_process.cut_df_avg(data, 2)
    ev = {
        "current_electricity": 5,
        "per_100km_electricity": 15,
        "max_electricity": 150,
        "charging_speed": 20
    }
    output_list = []
    for journey in df_list:
        # journey = journey.to_json(orient='records')
        # journey_obj = json.loads(journey)[0]
        # algo1 for one journey
        # output = algo1_for_one_journey(journey_obj, ev)
        # algo2 for one journey
        # output = algo2_for_one_journey(journey_obj, ev)
        journey, ev = data_process.load_data_2(journey)
        # algo1 for two journey
        # output = algo1_for_two_journey(journey, ev)
        # algo2 for two journey
        output = algo2_for_two_journey(journey, ev)
        output_list.append(output)
    output_df = DataFrame(output_list,
                          columns=["journey_ids", "plug_in_time", "departure_time", "time_slot",
                                   "carbon_emission", "avg_carbon_emission",
                                   "avg_priority_carbon_emission", "total_demand", "charging_duration"])
    output_df.to_csv("./output_example_algo2_2journey.csv", index=False)
