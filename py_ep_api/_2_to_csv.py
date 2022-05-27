import _0_util as util, pandas as pd, os, numpy as np
from sklearn.preprocessing import MinMaxScaler
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
'''Time for separate Scaling'''
lookback = 90
test_portion_factor = 0.3
label_scalers = {}
train_x = []
train_y = []
test_x = {}
test_y = {}
# Scaling the input data
sc = MinMaxScaler()
label_sc = MinMaxScaler()
data = sc.fit_transform(df.values)
# Obtaining the Scale for the labels(usage data) so that output can be re-scaled to actual value during evaluation
label_sc.fit(df.iloc[:, 0].values.reshape(-1, 1))
label_scalers[case_arr_abs] = label_sc

# Use lookback period to split inputs/labels
inputs = np.zeros((len(data) - lookback, lookback, df.shape[1]))
labels = np.zeros(len(data) - lookback)

for i in range(lookback, len(data)):
    inputs[i - lookback] = data[i - lookback:i]
    labels[i - lookback] = data[i, 0]
inputs = inputs.reshape(-1, lookback, df.shape[1])
labels = labels.reshape(-1, 1)

# Split data into train/test portions and combining all data from different files into a single array
test_portion = int(test_portion_factor * len(inputs))
if len(train_x) == 0:
    train_x = inputs[:-test_portion]
    train_y = labels[:-test_portion]
else:
    train_x = np.concatenate((train_x, inputs[:-test_portion]))
    train_y = np.concatenate((train_y, labels[:-test_portion]))
test_x[case_arr_abs] = (inputs[-test_portion:])
test_y[case_arr_abs] = (labels[-test_portion:])