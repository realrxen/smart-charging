from datetime import datetime
from datetime import timedelta
import time
import pandas as pd
import utils
import functions


# algo1 连续充电法
def algo1(start_charging_time, departure_time, charging_minutes, data):
    b = time.strptime(departure_time, '%Y-%m-%d %H:%M')
    last_charging_time = (datetime.fromtimestamp(time.mktime(b)) - timedelta(minutes=charging_minutes)).strftime(
        "%Y-%m-%d %H:%M")
    all_possible_forecasts = functions.get_all_possible_forecasts(start_charging_time, last_charging_time,
                                                                  charging_minutes, data)
    min_cost = min(all_possible_forecasts)
    min_index = all_possible_forecasts.index(min(all_possible_forecasts))
    time_slot = utils.outputSlot1(functions.get_the_minutes_list(start_charging_time, last_charging_time)[min_index],
                                  charging_minutes)
    return time_slot, min_cost



def algo2(start_charging_time, departure_time, charging_minutes, data):
    df = functions.get_dataframe(data)
    outputs, carbon_emission = functions.calculate_total_carbon_better(start_charging_time, departure_time,
                                                                       charging_minutes, df)
    return outputs, carbon_emission
