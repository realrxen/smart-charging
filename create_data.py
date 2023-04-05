import utils
import random
from pandas import DataFrame


# 50km/h 50/60
def create_data(plug_in_time, user_type, days, user_ids):
    plug_in_times = []
    for i in range(days):
        plug_in_times.append(utils.time_plus_minutes(plug_in_time, i * 24 * 60))
    journey_list = []
    for plug_in_time_ in plug_in_times:
        for user_id in user_ids:
            diff_plug_in = random.randint(-30, 31)
            diff_departure = random.randint(-30, 31)
            diff_d = round(random.uniform(0.8, 1.2), 2)
            distance = (31 - diff_departure) * 60 / 60
            # random factor to distance
            distance = int(distance * diff_d) + 1
            p_time = utils.formatTimeToCsv(utils.time_plus_minutes(plug_in_time_, diff_plug_in))
            departure_time_ = utils.time_plus_minutes(plug_in_time_, 15 * 60)
            d_time = utils.formatTimeToCsv(utils.time_plus_minutes(departure_time_, diff_departure))
            p_d, p_t = utils.splitTimeCsv(p_time)
            d_d, d_t = utils.splitTimeCsv(d_time)
            journey_list.append(
                [str(user_id) + "_" + user_type, utils.get_unique_id(), p_d, p_t, d_d, d_t, distance, user_type])
    journey_df = DataFrame(journey_list,
                           columns=['user_id', 'journey_id', 'plug_in_date', 'plug_in_time', 'departure_date',
                                    'departure_time',
                                    'distance', 'user_type'])
    return journey_df


if __name__ == '__main__':
    journey_df_9_5 = create_data("2022-08-08 17:30", "9_5", 7, [1, 2, 3, 4, 5, 6])
    journey_df_nurse_day_1 = create_data("2022-08-08 08:30", "nurse", 4, [1, 2, 3])
    journey_df_nurse_night_1 = create_data("2022-08-08 17:30", "nurse", 4, [4, 5, 6])
    journey_df_nurse_day_2 = create_data("2022-08-15 08:30", "nurse", 3, [4, 5, 6])
    journey_df_nurse_night_2 = create_data("2022-08-15 17:30", "nurse", 3, [1, 2, 3])
    total_df = journey_df_9_5.append(
        [journey_df_nurse_day_1, journey_df_nurse_night_1, journey_df_nurse_day_2, journey_df_nurse_night_2])
    total_df.to_csv("./journey_example.csv", index=False)
