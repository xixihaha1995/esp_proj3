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

'''
Train df,
Test df
'''
test_portion = int(test_portion_factor * len(df.values))
df_train = df.iloc[:-test_portion]
df_test = df.iloc[-test_portion:]
# Scaling the input data
sc = MinMaxScaler()
label_sc = MinMaxScaler()
data_train = sc.fit_transform(df_train.values)
data_test = sc.transform(df_test.values)
# Obtaining the Scale for the labels(usage data) so that output can be re-scaled to actual value during evaluation
label_sc.fit(df_train.iloc[:, -1].values.reshape(-1, 1))
label_scalers[case_arr_abs] = label_sc

# Use lookback period to split inputs/labels
inputs_train = np.zeros((len(data_train) - lookback, lookback, df_train.shape[1]))
labels_train = np.zeros(len(data_train) - lookback)

for i in range(lookback, len(data_train)):
    inputs_train[i - lookback] = data_train[i - lookback:i]
    labels_train[i - lookback] = data_train[i, 0]
inputs_train = inputs_train.reshape(-1, lookback, df_train.shape[1])
labels_train = labels_train.reshape(-1, 1)


inputs_test = np.zeros((len(data_test) , lookback, df_test.shape[1]))
labels_test = np.zeros(len(data_test) )
scaled_tain_test_df = np.concatenate((data_train,data_test))
for i in range(data_train.shape[0] , len(scaled_tain_test_df)):
    inputs_test[i - data_train.shape[0]] = scaled_tain_test_df[i - lookback:i]
    labels_test[i - data_train.shape[0]] = scaled_tain_test_df[i, 0]
inputs_test = inputs_test.reshape(-1, lookback, df_test.shape[1])
labels_test = labels_test.reshape(-1, 1)
# Split data into train/test portions and combining all data from different files into a single array
if len(train_x) == 0:
    train_x = inputs_train[:]
    train_y = labels_train[:]
else:
    train_x = np.concatenate((train_x, inputs_train[:]))
    train_y = np.concatenate((train_y, labels_train[:]))

test_x[case_arr_abs] = (inputs_test[:])
test_y[case_arr_abs] = (labels_test[:])
pass