import utils
import random
from pandas import DataFrame


# 50km/h 50/60
def get_random_time(plug_in_time_, hours, diff):
    diff_plug_in = random.randint(0, diff + 1)
    diff_departure = random.randint(0, diff + 1)
    # random factor to distance
    diff_d = round(random.uniform(0.8, 1.2), 2)
    distance = diff_departure * 60 / 60
    distance = int(distance * diff_d) + 1

    p_time = utils.formatTimeToCsv(utils.time_plus_minutes(plug_in_time_, diff_plug_in))

    departure_time_ = utils.time_plus_minutes(plug_in_time_, hours * 60)
    d_time = utils.formatTimeToCsv(utils.time_plus_minutes(departure_time_, diff_departure * -1))
    return p_time, d_time, distance


def create_data_new(plug_in_time, user_type, days, user_ids,hours):
    plug_in_times = []
    for i in range(days):

        plug_in_times.append(utils.time_plus_minutes(plug_in_time, i * 24 * 60))
    journey_list = []
    for plug_in_time_ in plug_in_times:
        for user_id in user_ids:

            p_time, d_time, distance = get_random_time(plug_in_time_, hours, 60)
            p_d, p_t = utils.splitTimeCsv(p_time)
            d_d, d_t = utils.splitTimeCsv(d_time)

            x_time_ = utils.time_plus_minutes(utils.formatTimeFromCsv(p_time), random.randint(2, 4)*60)
            p_time_, d_time_, distance_ = get_random_time(x_time_, random.randint(2, 4), 30)
            p_d_, p_t_ = utils.splitTimeCsv(utils.formatTimeToCsv(x_time_))
            d_d_, d_t_ = utils.splitTimeCsv(d_time_)
            journey_list.append(
                [str(user_id) + "_" + user_type, utils.get_unique_id(), p_d, p_t, p_d_, p_t_, distance_, user_type])
            journey_list.append(
                [str(user_id) + "_" + user_type, utils.get_unique_id(), d_d_, d_t_, d_d, d_t, distance, user_type])
    journey_df = DataFrame(journey_list,
                           columns=['user_id', 'journey_id', 'plug_in_date', 'plug_in_time', 'departure_date',
                                    'departure_time',
                                    'distance', 'user_type'])
    return journey_df


if __name__ == '__main__':
    journey_df_9_5 = create_data_new("2022-08-08 17:00", "9_5", 7, list(range(1,21)),16)
    journey_df_5_9 = create_data_new("2022-08-08 05:00", "5_9", 7, list(range(1,21)),16)
    journey_df_nurse_day_1 = create_data_new("2022-08-08 09:00", "nurse", 4, list(range(1,11)),16)
    journey_df_nurse_night_1 = create_data_new("2022-08-08 17:00", "nurse", 4, list(range(11,21)),16)
    journey_df_nurse_day_2 = create_data_new("2022-08-12 21:00", "nurse", 3, list(range(11,21)),16)
    journey_df_nurse_night_2 = create_data_new("2022-08-12 17:00", "nurse", 3, list(range(1,11)),16)
    total_df = journey_df_9_5.append(
        [journey_df_nurse_day_1, journey_df_nurse_night_1, journey_df_nurse_day_2, journey_df_nurse_night_2,
         journey_df_5_9])
    total_df.to_csv("./journey_final2.csv", index=False)

