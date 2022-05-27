import _0_util as util
result = util.loadJSONFromOutputs('pyep_results')

df = pd.read_csv(case_arr_abs)
df.Timestamp = pd.to_datetime(df.Timestamp)
df['minute'] = df.apply(lambda x: x['Timestamp'].minute, axis=1)
df['hour'] = df.apply(lambda x: x['Timestamp'].hour, axis=1)
df['dayofweek'] = df.apply(lambda x: x['Timestamp'].dayofweek, axis=1)
new_cols = ['dayofweek', 'hour', 'minute', 't_out', 't_slab1',
            't_cav', 'valve_ht', 'valve_cl', 'vfr_water', 'rc_y', 'y']

df = df.sort_values("Timestamp").drop("Timestamp", axis=1)
# new_cols = ['t_out','t_slab1','t_cav','valve_ht',
#             'valve_cl','vfr_water','rc_y','y']
df = df[new_cols]