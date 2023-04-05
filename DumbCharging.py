from datetime import datetime
from datetime import timedelta
import time
import pandas as pd
import utils
import functions


def algo(start_charging_time, departure_time, charging_minutes, data):

    b = time.strptime(start_charging_time, '%Y-%m-%d %H:%M')
    finish_charging_time = (datetime.fromtimestamp(time.mktime(b)) + timedelta(minutes=charging_minutes)).strftime(
        "%Y-%m-%d %H:%M")
    carbon_emission = functions.get_the_total_forecasts(start_charging_time, data, charging_minutes)
    time_slot = start_charging_time + " ~ " + finish_charging_time
    return time_slot,carbon_emission

