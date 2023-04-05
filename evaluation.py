import pandas as pd
import utils
import functions
import SmartCharging
import eval_f
import data_process

journey,ev = data_process.load_data()

# evaluation_1_2.py
# eval_f.algo1_1(journey,ev)
# eval_f.algo2_2(journey,ev)
# # evaluation_11_1.py
# eval_f.algo1_11(journey,ev)
# eval_f.algo1_1(journey,ev)
# # evaluation_11_2.py
# eval_f.algo1_11(journey,ev)
# eval_f.algo2_2(journey,ev)
# # evaluation_11_22.py
# eval_f.algo1_11(journey,ev)
# eval_f.algo2_22(journey,ev)
# # evaluation_22_1.py
# eval_f.algo2_22(journey,ev)
# eval_f.algo1_1(journey,ev)
# # evaluation_22_2.py
# eval_f.algo2_22(journey,ev)
# eval_f.algo2_2(journey,ev)

if __name__ == '__main__':
    eval_f.algo1_11(journey, ev)
    # eval_f.algo2_2(journey, ev)