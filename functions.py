import requests
from datetime import datetime
from datetime import timedelta
import time
import json
import pandas as pd
import utils
import numpy as np


def get_next48h_intensity(iso_date):
    headers = {
        'Accept': 'application/json'
    }
    url = 'https://api.carbonintensity.org.uk/intensity/' + iso_date + '/fw48h'
    r = requests.get(url, params={}, headers=headers)
    return json.loads(r.text).get("data")


def get_dataframe(data):
    from_dates = []
    from_times = []
    end_dates = []
    end_times = []
    forecasts = []

    for i in range(len(data)):
        from_dates.append(utils.formatTime_date(data[i].get("from")))
        from_times.append(utils.formatTime_time(data[i].get("from")))
        end_dates.append(utils.formatTime_date(data[i].get("to")))
        end_times.append(utils.formatTime_time(data[i].get("to")))
        forecasts.append(data[i].get("intensity").get("forecast"))

    carbon_intensity_48h = {
        'from_date': from_dates,
        'from_time': from_times,
        'end_date': end_dates,
        'end_time': end_times,
        'forecast': forecasts
    }

    df = pd.DataFrame(carbon_intensity_48h)
    return df


def get_carbon_intensity_by_time(date_t, data, minutes):
    b = time.strptime(date_t, '%Y-%m-%d %H:%M')
    x_time = (datetime.fromtimestamp(time.mktime(b)) - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
    finish_time = (datetime.fromtimestamp(time.mktime(b)) + timedelta(minutes=minutes + 30)).strftime("%Y-%m-%d %H:%M")
    f = data.loc[(data["from_date"] + " " + data["from_time"] > x_time)
                 & (data["end_date"] + " " + data["end_time"] < finish_time)]
    return f


def get_carbon_intensity_by_time_2(df, start_charging_time, finish_time):
    a = time.strptime(start_charging_time, '%Y-%m-%d %H:%M')
    b = time.strptime(finish_time, '%Y-%m-%d %H:%M')
    x_time = (datetime.fromtimestamp(time.mktime(a)) - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
    finish_time = (datetime.fromtimestamp(time.mktime(b)) + timedelta(minutes=0)).strftime("%Y-%m-%d %H:%M")
    f = df.loc[(df["from_date"] + " " + df["from_time"] > x_time)
               & (df["end_date"] + " " + df["end_time"] <= finish_time)]
    return f


def get_carbon_intensity_by_time_3(df, start_charging_time, finish_time):
    a = time.strptime(start_charging_time, '%Y-%m-%d %H:%M')
    b = time.strptime(finish_time, '%Y-%m-%d %H:%M')
    x_time = (datetime.fromtimestamp(time.mktime(a)) - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
    finish_time = (datetime.fromtimestamp(time.mktime(b)) + timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M")
    f = df.loc[(df["from_date"] + " " + df["from_time"] > x_time)
               & (df["end_date"] + " " + df["end_time"] <= finish_time)]
    return f


def get_the_minutes_list(a_time, b_time):
    start_times = []
    d1 = time.strptime(a_time, '%Y-%m-%d %H:%M')
    d1 = datetime.fromtimestamp(time.mktime(d1))
    d2 = time.strptime(b_time, '%Y-%m-%d %H:%M')
    d2 = datetime.fromtimestamp(time.mktime(d2))

    # 获取时间间隔
    delta = d2 - d1
    #     print(delta.total_seconds())

    # 遍历获得每一个时间点
    for i in range(int(delta.total_seconds() / 60) + 1):
        time_point_minute = (d1 + timedelta(minutes=i)).strftime("%Y-%m-%d %H:%M")
        start_times.append(time_point_minute)
    return start_times


# 得到整个充电过程的碳强度预测
# 输入：充电开始时间，请求回来的数据，充电时间（分钟）
def get_the_total_forecasts(start_time, data, minutes):
    b = time.strptime(start_time, '%Y-%m-%d %H:%M')
    finish_time = (datetime.fromtimestamp(time.mktime(b)) + timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M")
    df = get_dataframe(data)
    f = get_carbon_intensity_by_time(start_time, df, minutes)
    first_end_time = f.iloc[0]["end_date"] + " " + f.iloc[0]["end_time"]
    last_from_time = f.iloc[-1]["from_date"] + " " + f.iloc[-1]["from_time"]
    forecast_list = f["forecast"].tolist()

    if len(forecast_list) > 1:
        first_forecast = forecast_list[0]
        last_forecast = forecast_list[-1]
        total_cost = utils.get_part_mintues(start_time, first_end_time) * first_forecast / 60 + sum(
            forecast_list[1:-1]) / 60 * 30 + utils.get_part_mintues(last_from_time, finish_time) * last_forecast / 60
    else:
        total_cost = minutes * forecast_list[0] / 60
    return total_cost


def get_all_possible_forecasts(now_time, last_charging_time, charging_time, data):
    forecast_lists = []
    time_points = get_the_minutes_list(now_time, last_charging_time)
    for start_time_point in time_points:
        forecast_lists.append(get_the_total_forecasts(start_time_point, data, charging_time))
    return forecast_lists





def calculate_total_carbon_better(start_charging_time, departure_time, minutes, df):
    # print(start_charging_time, departure_time, minutes)
    df_ = get_carbon_intensity_by_time_3(df, start_charging_time, departure_time)
    df_ = df_.copy()
    df_ = df_.sort_values(by=["from_date", "from_time"], ascending=True)
    df_.loc[len(df_) - 1, 'end_time'] = utils.formatTime_time_2(departure_time)
    df_['from'] = df_['from_date'] + " " + df_['from_time']
    df_['end'] = df_['end_date'] + " " + df_['end_time']
    df_['valid_charging_minute'] = df_.apply(
        lambda row: utils.get_part_mintues(row['from'], row['end']), axis=1)
    slot_count = minutes // 30
    if minutes % 30 == 0:
        pass
    else:
        slot_count += 1
    f = df_.sort_values(by=["from_date", "from_time"], ascending=True)
    f = f.sort_values(by=["forecast"], ascending=True)

    f = f.head(slot_count)
    from_list = (f["from_date"] + " " + f["from_time"]).tolist()
    earliest_time = from_list[0]
    if (sum(f["valid_charging_minute"]) < minutes) & (earliest_time >= start_charging_time):
        slot_count += 1
        f = df_.sort_values(by=["from_date", "from_time"], ascending=True)
        f = f.sort_values(by=["forecast"], ascending=True)
        f = f.head(slot_count)
    delay = utils.get_part_mintues(earliest_time, start_charging_time)
    if (earliest_time < start_charging_time) & (minutes > delay):

        if sum(f["valid_charging_minute"]) - delay < minutes:
            slot_count += 1
            f = df_.sort_values(by=["from_date", "from_time"], ascending=True)
            f = f.sort_values(by=["forecast"], ascending=True)
            f = f.head(slot_count)

    valid_charging_minutes = f["valid_charging_minute"].tolist()
    valid_charging_minutes[-1] = minutes - sum(valid_charging_minutes[0:-1])
    from_ls = f["from"].tolist()
    valid_minutes_dict = dict(zip(from_ls, valid_charging_minutes))
    forecasts = f["forecast"].tolist()
    print("valid_charging_minutes:", valid_charging_minutes)
    print("slot_count:", slot_count)
    print("forecast", forecasts)
    # print(valid_minutes_dict)
    for i in range(len(forecasts)):
        forecasts[i] = forecasts[i] / 60
    total_emission = sum(np.multiply(forecasts, valid_charging_minutes))
    f = f.sort_values(by=["from_date", "from_time"], ascending=True)

    slots = []
    for start_time in list(f["from"]):
        valid_minute = valid_minutes_dict[start_time]
        if valid_minute == 0:
            continue
        cut_time = utils.time_plus_minutes(start_time, valid_minute)
        time_slot = start_time + " ~ " + cut_time
        slots.append(time_slot)
    print("slots", slots)
    print("total_emission", total_emission)
    return slots, total_emission


def calculate_total_carbon(start_charging_time, departure_time, minutes, df):
    print(start_charging_time, departure_time, minutes)
    df_ = get_carbon_intensity_by_time_2(df, start_charging_time, departure_time)
    print(df_)
    slot_count = minutes // 30
    if minutes % 30 == 0:
        pass
    else:
        slot_count += 1
    f = df_.sort_values(by=["from_date", "from_time"], ascending=True)
    f = f.sort_values(by=["forecast"], ascending=True)

    f = f.head(slot_count)

    f = f.sort_values(by=["from_date", "from_time"], ascending=True)
    earliest_time = (f["from_date"] + " " + f["from_time"]).tolist()[0]
    latest_start_time = (f["from_date"] + " " + f["from_time"]).tolist()[-1]
    # last_time = utils.get_part_mintues(latest_start_time, departure_time)
    # last_delay = 30 - last_time

    if earliest_time < start_charging_time:

        delay = utils.get_part_mintues(earliest_time, start_charging_time)

        if slot_count * 30 - delay < minutes:
            slot_count += 1
            f = df_.sort_values(by=["from_date", "from_time"], ascending=True)
            f = f.sort_values(by=["forecast"], ascending=True)
            f = f.head(slot_count)
            f = f.sort_values(by=["from_date", "from_time"], ascending=True)

    print(f)
    print("slot_count:", slot_count)
    ss = f["forecast"].tolist()
    print("forecast]", ss)
    for i in range(len(ss)):
        ss[i] = ss[i] / 2
    ss[-1] = ss[-1] * (minutes % 30) / 30
    total_emission = sum(ss)
    slot_dict = pd.Series(f.forecast.values, index=f.from_date + " " + f.from_time).to_dict()

    if ((list(slot_dict.keys())[0] < start_charging_time) & (
            utils.get_part_mintues(list(slot_dict.keys())[0], start_charging_time) < 30)):
        b = time.strptime(start_charging_time, '%Y-%m-%d %H:%M')

        if b.tm_min >= 30:
            m = abs(60 - b.tm_min)
        else:
            m = abs(30 - b.tm_min)


        minutes_ = minutes - m
        slot_count = minutes_ // 30

        if (minutes_ % 30 == 0) or (minutes < m):
            pass
        else:
            slot_count += 1
            f = df_.head(slot_count + 1).sort_values(by=["from_date", "from_time"], ascending=True)
            slot_dict = pd.Series(f.forecast.values, index=f.from_date + " " + f.from_time).to_dict()
            m2 = minutes_ - (slot_count - 1) * 30
            ss = list(slot_dict.values())
            total_emission = ss[0] * m / 60 + sum(ss[1:-1]) * 30 / 60 + ss[-1] * m2 / 60
    print("total_emission", total_emission)
    return slot_dict, total_emission


def calculate_avg_priority_emission(emissions, minutes, journey_number):
    minutes_ = minutes
    total_minutes = sum(minutes)
    for i in range(len(minutes)):
        minutes[i] = minutes[i] / total_minutes
    avg_priority_emission = 0
    for i, emission in enumerate(emissions):
        avg_priority_emission = avg_priority_emission + emission * minutes_[i]
    return avg_priority_emission / journey_number


def get_future_journeys(df, current_time, hours):
    b = time.strptime(current_time, '%Y-%m-%d %H:%M')
    d_time = (datetime.fromtimestamp(time.mktime(b)) + timedelta(minutes=hours*60)).strftime("%Y-%m-%d %H:%M")
    current_time = utils.formatTimeToCsv(current_time)
    d_time = utils.formatTimeToCsv(d_time)
    f = df.loc[(df["plug_in_date"] + " " + df["plug_in_time"] >= current_time)
                 & (df["departure_date"] + " " + df["departure_date"] < d_time)]
    return f