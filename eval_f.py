import SmartCharging
import functions
import utils


def check_demand(total_demand, ev, journey_number):
    if total_demand >= ev["max_electricity"]:
        print("Do not meet the charging requirement")

        total_demand = ev["max_electricity"]
        return False
    # compare the current electricity with total total_demand
    if journey_number * ev["current_electricity"] >= total_demand:
        print("Do not need to charge now")
        return False
    else:
        # print("total_demand:", total_demand - journey_number * ev["current_electricity"], "kw·h", journey_number)
        return True


def get_charging_duration(total_demand, ev, plug_in_time, departure_time, journey_number):
    charging_duration = int((total_demand - journey_number * ev["current_electricity"]) / ev["charging_speed"] * 60) + 1
    # compare the finished time with the first departure time
    charging_time_limit = utils.get_part_mintues(departure_time, plug_in_time)
    if charging_duration > charging_time_limit:
        print("can not meet the charging requirement")
        charging_duration = charging_time_limit
    print("charging_duration:", charging_duration, "minutes")
    return charging_duration


def algo1_1(journey, ev):
    ls = [1]
    journey_number = 2
    emissions = []
    minutes = []
    for i in ls:
        journey_ids = journey["journey_ids"]
        print("journey_id:", journey_ids)
        unanticipated_demand = 0
        required_electricity = journey["required_electricity"]
        print("required_distance:", sum(required_electricity[0:i + 1]), "km")
        journeys_demand = sum(required_electricity[0:i + 1]) * ev["per_100km_electricity"] / 100 * 2

        total_demand = journeys_demand + unanticipated_demand
        if not check_demand(total_demand, ev, journey_number):
            continue
        plug_in_times = journey["plug_in_times"]
        departure_times = journey["departure_times"]
        charging_duration = get_charging_duration(total_demand, ev, plug_in_times[0],
                                                  departure_times[0], journey_number)
        if i != len(ls):
            start_charging_time = journey["plug_in_times"][i]
            print("plug_in_time: ", start_charging_time)
            departure_time = journey["departure_times"][i]
        else:
            start_charging_time = journey["plug_in_times"][0]
            print("plug_in_time: ", start_charging_time)
            departure_time = journey["departure_times"][0]
        data = functions.get_next48h_intensity(utils.str2iso(start_charging_time))
        time_slot, carbon_emission = SmartCharging.algo1(start_charging_time, departure_time, charging_duration, data)
        print("algo1 time slot : ", time_slot)
        print("algo1 carbon_emission :", carbon_emission)
        print("algo1 avg carbon emission : ", carbon_emission / charging_duration, "/ minute")
        emissions.append(carbon_emission)
        minutes.append(charging_duration)
        print("================" * 5)
    avg_priority_emission = functions.calculate_avg_priority_emission(emissions, minutes, journey_number)
    print('\033[0;36mavg_priority_emission is ' + str(avg_priority_emission) + '\033[0m')


def algo1_11(journey, ev):
    ls = [0, 1]
    journey_number = 1
    emissions = []
    minutes = []
    for i in ls:
        journey_ids = journey["journey_ids"]
        journey_id = journey_ids[i]
        print("journey_id:", journey_id)
        unanticipated_demand = 0
        required_electricity = journey["required_electricity"]
        print("required_distance:", sum(required_electricity[i:i + 1]), "km")
        journeys_demand = sum(required_electricity[i:i + 1]) * ev["per_100km_electricity"] / 100 * 2
        total_demand = journeys_demand + unanticipated_demand
        if not check_demand(total_demand, ev, journey_number):
            continue
        plug_in_times = journey["plug_in_times"]
        departure_times = journey["departure_times"]
        charging_duration = get_charging_duration(total_demand, ev, plug_in_times[0],
                                                  departure_times[0], journey_number)
        if i != len(ls):
            start_charging_time = journey["plug_in_times"][i]
            print("plug_in_time: ", start_charging_time)
            departure_time = journey["departure_times"][i]
        else:
            start_charging_time = journey["plug_in_times"][0]
            print("plug_in_time: ", start_charging_time)
            departure_time = journey["departure_times"][0]
        data = functions.get_next48h_intensity(utils.str2iso(start_charging_time))
        time_slot, carbon_emission = SmartCharging.algo1(start_charging_time, departure_time, charging_duration, data)
        print("algo1 time slot : ", time_slot)
        print("algo1 carbon_emission :", carbon_emission)
        print("algo1 avg carbon emission : ", carbon_emission / charging_duration, "/ minute")
        emissions.append(carbon_emission)
        minutes.append(charging_duration)
        print("================" * 5)
    avg_priority_emission = functions.calculate_avg_priority_emission(emissions, minutes, journey_number)
    print('\033[0;36mavg_priority_emission is ' + str(avg_priority_emission) + '\033[0m')
    return journey_id,


def algo2_22(journey, ev):
    ls = [0, 1]
    journey_number = 1
    emissions = []
    minutes = []
    for i in ls:
        unanticipated_demand = 0
        journey_ids = journey["journey_ids"]
        journey_id = journey_ids[i]
        print("journey_id:", journey_id)
        required_electricity = journey["required_electricity"]
        print("required_distance:", sum(required_electricity[i:i + 1]), "km")
        journeys_demand = sum(required_electricity[i:i + 1]) * ev["per_100km_electricity"] / 100 * 2
        total_demand = journeys_demand + unanticipated_demand
        if not check_demand(total_demand, ev, journey_number):
            continue
        plug_in_times = journey["plug_in_times"]
        departure_times = journey["departure_times"]
        charging_duration = get_charging_duration(total_demand, ev, plug_in_times[0],
                                                  departure_times[0], journey_number)
        if i != len(ls):
            start_charging_time = journey["plug_in_times"][i]
            print("plug_in_time: ", start_charging_time)
            departure_time = journey["departure_times"][i]
        else:
            start_charging_time = journey["plug_in_times"][0]
            print("plug_in_time: ", start_charging_time)
            departure_time = journey["departure_times"][0]
        data = functions.get_next48h_intensity(utils.str2iso(start_charging_time))
        time_slot, carbon_emission = SmartCharging.algo2(start_charging_time, departure_time, charging_duration, data)
        print("algo2 time slot :", utils.merge_slots(time_slot, [], 0, 0))
        print("algo2 carbon_emission :", carbon_emission)
        print("algo2 avg carbon emission : ", carbon_emission / charging_duration, "/ minute")
        emissions.append(carbon_emission)
        minutes.append(charging_duration)
        print("================" * 5)
    avg_priority_emission = functions.calculate_avg_priority_emission(emissions, minutes, journey_number)
    print('\033[0;36mavg_priority_emission is ' + str(avg_priority_emission) + '\033[0m')


def algo2_2(journey, ev):
    ls = [1]
    journey_number = 2
    emissions = []
    minutes = []
    for i in ls:
        # journey_ids = journey["journey_ids"]
        # print("journey_ids:", journey_ids)
        unanticipated_demand = 0
        required_electricity = journey["required_electricity"]
        print("required_distance:", sum(required_electricity[0:i + 1]), "km")
        journeys_demand = sum(required_electricity[0:i + 1]) * ev["per_100km_electricity"] / 100 * 2
        total_demand = journeys_demand + unanticipated_demand
        if not check_demand(total_demand, ev, journey_number):
            continue
        plug_in_times = journey["plug_in_times"]
        departure_times = journey["departure_times"]
        charging_duration = get_charging_duration(total_demand, ev, plug_in_times[0],
                                                  departure_times[0], journey_number)
        if i != len(ls):
            start_charging_time = journey["plug_in_times"][i]
            print("plug_in_time: ", start_charging_time)
            departure_time = journey["departure_times"][i]
        else:
            start_charging_time = journey["plug_in_times"][0]
            print("plug_in_time: ", start_charging_time)
            departure_time = journey["departure_times"][0]

        data = functions.get_next48h_intensity(utils.str2iso(start_charging_time))
        time_slot, carbon_emission = SmartCharging.algo2(start_charging_time, departure_time, charging_duration, data)
        print("algo2 time slot :", utils.merge_slots(time_slot, [], 0, 0))
        print("algo2 carbon_emission :", carbon_emission)
        print("algo2 avg carbon emission : ", carbon_emission / charging_duration, "/ minute")
        emissions.append(carbon_emission)
        minutes.append(charging_duration)
        print("================" * 5)
    avg_priority_emission = functions.calculate_avg_priority_emission(emissions, minutes, journey_number)
    print('\033[0;36mavg_priority_emission : ' + str(avg_priority_emission) + '\033[0m')
