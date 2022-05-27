import _0_util as util, pandas as pd, os
result = util.loadJSONFromOutputs('pyep_results')

script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
case_arr_abs = os.path.join(script_dir, '../py_ep_outputs', 'pyep_results.csv')

df = pd.read_csv(case_arr_abs)
df.timestamp = pd.to_datetime(df.timestamp, unit='s')
df['minute'] = df.apply(lambda x: x['timestamp'].minute, axis=1)
df['hour'] = df.apply(lambda x: x['timestamp'].hour, axis=1)
df['dayofweek'] = df.apply(lambda x: x['timestamp'].dayofweek, axis=1)
df['dayofmonth'] = df.apply(lambda x: x['timestamp'].day, axis=1)
df['month'] = df.apply(lambda x: x['timestamp'].month, axis=1)
new_cols = ['month','dayofmonth','dayofweek', 'hour', 'minute',
            'oat[C]', 'elec_hvac[J]','solar[W/m2]', 'zone_load_rate[W]']

df = df.sort_values("timestamp").drop("timestamp", axis=1)
# new_cols = ['t_out','t_slab1','t_cav','valve_ht',
#             'valve_cl','vfr_water','rc_y','y']
df = df[new_cols]
pass