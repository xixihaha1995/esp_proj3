import _0_util as util, pandas as pd, os, numpy as np, datetime
from pathlib import Path

result = util.loadJSONFromOutputs('pyep_results')

drop_warmup = 8 * 24*4
x_date_start = 1483228800
x_date = []
for time_step in range(np.array(result['oat'][drop_warmup:]).shape[0]):
    datetime_time = datetime.datetime.fromtimestamp(x_date_start)
    x_date.append(x_date_start)
    x_date_start = x_date_start + 15*60

dataset = pd.DataFrame({'oat[C]': result['oat'][drop_warmup:],
                        'elec_hvac[J]': result['elec_hvac'][drop_warmup:],
                        'solar[W/m2]': result['solar'][drop_warmup:],
                        'zone_load_rate[W]': result['zone_load'][drop_warmup:],
                        'timestamp': np.array(x_date)})
saved_cols = ['timestamp','oat[C]','elec_hvac[J]','solar[W/m2]','zone_load_rate[W]']
dataset = dataset[saved_cols]
filepath = Path('../toy_2_py_ep_outputs/pyep_results.csv')
dataset.to_csv(filepath, index=False)
