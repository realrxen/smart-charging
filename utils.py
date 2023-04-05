import random

import requests
from datetime import datetime
from datetime import timedelta
import time
import uuid
import json
import pandas as pd


def formatTimeFromCsv(s):
    timeArray = time.strptime(s, "%Y/%m/%d %H:%M")
    return time.strftime("%Y-%m-%d %H:%M", timeArray)


def formatTimeToCsv(s):
    timeArray = time.strptime(s, "%Y-%m-%d %H:%M")
    return time.strftime("%Y/%m/%d %H:%M", timeArray)


def splitTimeCsv(s):
    timeArray = time.strptime(s, "%Y/%m/%d %H:%M")
    d = time.strftime("%Y/%m/%d", timeArray)
    t = time.strftime("%H:%M", timeArray)
    return d, t


def get_part_mintues(a_time, b_time):
    d1 = time.strptime(a_time, '%Y-%m-%d %H:%M')
    d1 = datetime.fromtimestamp(time.mktime(d1))
    d2 = time.strptime(b_time, '%Y-%m-%d %H:%M')
    d2 = datetime.fromtimestamp(time.mktime(d2))
    delta = abs(d2 - d1)
    return int(delta.seconds / 60)


def str2iso(time_str):
    b = time.strptime(time_str, '%Y-%m-%d %H:%M')
    return (datetime.fromtimestamp(time.mktime(b))).isoformat()


def formatTime_date(x):
    t = time.strptime(x, '%Y-%m-%dT%H:%MZ')
    d = datetime.fromtimestamp(time.mktime(t))
    date_time_str = d.strftime("%Y-%m-%d")
    return date_time_str


def formatTime_time(x):
    t = time.strptime(x, '%Y-%m-%dT%H:%MZ')
    d = datetime.fromtimestamp(time.mktime(t))
    time_time_str = d.strftime("%H:%M")
    return time_time_str


def formatTime_time_2(x):
    t = time.strptime(x, '%Y-%m-%d %H:%M')
    d = datetime.fromtimestamp(time.mktime(t))
    time_time_str = d.strftime("%H:%M")
    return time_time_str


# 给充电开始时间和充电时长
def outputSlot1(start_time, charging_minutes):
    a = time.strptime(start_time, '%Y-%m-%d %H:%M')
    charging_end_time = (datetime.fromtimestamp(time.mktime(a)) + timedelta(minutes=charging_minutes)).strftime(
        "%Y-%m-%d %H:%M")
    return start_time + " ~ " + charging_end_time


def outputSlot3():
    pass


def outputSlot2(charging_dict, start_charging_time, charging_minutes):
    outputs = []
    slots = list(charging_dict.keys())
    if start_charging_time > slots[0]:
        delay = abs(get_part_mintues(slots[0], start_charging_time) - 30)
        # print("delay:", delay)
        # delay = 20
        slots[0] = start_charging_time
        if delay >= charging_minutes:
            outputs.append(outputSlot1(slots[0], charging_minutes))
            return outputs
        else:
            outputs.append(outputSlot1(slots[0], delay))
        for t in slots[1:-1]:
            outputs.append(outputSlot1(t, 30))
        outputs.append(outputSlot1(slots[-1], charging_minutes - delay - (len(slots) - 2) * 30))
    else:
        for t in slots[0:-1]:
            outputs.append(outputSlot1(t, 30))
        outputs.append(outputSlot1(slots[-1], charging_minutes - (len(slots) - 1) * 30))
    return outputs


def time_plus_minutes(current_time, minutes):
    a = time.strptime(current_time, '%Y-%m-%d %H:%M')
    target_time = (datetime.fromtimestamp(time.mktime(a)) + timedelta(minutes=minutes)).strftime("%Y-%m-%d %H:%M")
    return target_time


# n去试探前面的，m留下已经成功的
def merge_slots(slots, merged_slots=[], m=0, n=0):
    # m = 0 第一个时间段
    if n == 0:
        slot = slots[m]
        # 将第一个时间段加入到融合slot里面
        merged_slots.append(slot)
    # 已有的merged slots的时间段
    slot_split = merged_slots[m].split(" ~ ")
    # 如果没有下一个时间段，就这样了
    if n + 1 == len(slots):
        return merged_slots
    # 获取下一个时间段
    slot_ = slots[n + 1]
    slot_split_ = slot_.split(" ~ ")
    if slot_split[1] == slot_split_[0]:
        # slots[n] = slot_split[0] + "~" + slot_split[1]
        # 修改第一个时间段的结束时间
        merged_slots[m] = slot_split[0] + " ~ " + slot_split_[1]
        # print(slot_split_[1], n)
        merged_slots = merge_slots(slots, merged_slots, m, n + 1)
    else:
        # 加入下一个时间段，只有以它为开头来合并
        merged_slots.append(slot_)
        merged_slots = merge_slots(slots, merged_slots, m + 1, n + 1)
    return merged_slots


def get_unique_id():
    uni_id = ''.join(str(uuid.uuid4()).split('-'))
    return uni_id


if __name__ == '__main__':
    # print(merge_slots(
    #     ["2022-08-16 18:30~2022-08-16 19:00", "2022-08-16 19:00~2022-08-16 19:30",
    #      "2022-08-16 19:30~2022-08-16 20:00"]))

    # print(merge_slots(
    #     ["2022-08-16 18:30~2022-08-16 19:00", "2022-08-16 20:00~2022-08-16 20:30",
    #      "2022-08-16 20:30~2022-08-16 21:00","2022-08-16 21:00~2022-08-16 21:30","2022-08-16 22:30~2022-08-16 23:00","2022-08-16 23:00~2022-08-16 23:30"]))
    # 时间跨度

    a = ['2022-08-16 13:00 ~ 2022-08-16 13:30', '2022-08-16 13:30 ~ 2022-08-16 14:00',
         '2022-08-16 14:00 ~ 2022-08-16 14:30', '2022-08-16 14:30 ~ 2022-08-16 14:42']
    b = ['2022-08-16 13:00 ~ 2022-08-16 13:30', '2022-08-16 14:00 ~ 2022-08-16 14:30',
         '2022-08-16 14:30 ~ 2022-08-16 14:33']
    c = ['2022-08-17 11:30 ~ 2022-08-17 12:00', '2022-08-17 13:00 ~ 2022-08-17 13:10']
    # print(merge_slots(c))
    print(get_unique_id())


def get_charging_start_time(time_slot):
    slot_split = time_slot.split(" ~ ")
    return slot_split[0]


def get_charging_finish_time(time_slot):
    slot_split = time_slot.split(" ~ ")
    return slot_split[1]


def get_charging_delay(time_slots, plug_in_time):
    time_slots = time_slots[0:-1].split(",")
    delays = []
    for time_slot in time_slots:
        charging_start_time = get_charging_start_time(time_slot)
        charging_finish_time = get_charging_finish_time(time_slot)
        charging_middle_time = time_plus_minutes(charging_start_time,
                                                 get_part_mintues(charging_start_time, charging_finish_time))
        delay = get_part_mintues(plug_in_time, charging_middle_time)
        delays.append(delay)
    return sum(delays)


def get_time_zone(charging_time, n):
    a = time.strptime(charging_time, '%Y-%m-%d %H:%M')
    time_index = int(a.tm_hour // (24 / n)) + 1
    return (datetime.fromtimestamp(time.mktime(a)) - timedelta(
        minutes=(a.tm_hour * 60 + a.tm_min)) + timedelta(
        minutes=((time_index - 1) * 24 / n * 60))).strftime("%H:%M") + "~" + (
                       datetime.fromtimestamp(time.mktime(a)) - timedelta(
                   minutes=(a.tm_hour * 60 + a.tm_min)) + timedelta(
                   minutes=(time_index * 24 / n * 60))).strftime("%H:%M")


def get_time_zone_more_journeys(time_slot, n):
    time_slots = time_slot[0:-1].split(",")
    a = ''
    for t in time_slots:
        start_time = get_charging_start_time(t)
        time_zone = get_time_zone(start_time,n)
        a = a + time_zone+","
    return a[0:-1]