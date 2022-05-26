import sys, os, json
sys.path.insert(0, 'C:\EnergyPlusV22-1-0')

from pyenergyplus.api import EnergyPlusAPI
one_time = True
outdoor_temp_sensor = 0
outdoor_dew_point_actuator = 0
zone_cool = []
def time_step_handler(state):
    global one_time , outdoor_temp_sensor , outdoor_dew_point_sensor , outdoor_dew_point_actuator,zoon_cool_sensor
    if one_time:
        if not api.exchange.api_data_fully_ready(state):
            return
        outdoor_temp_sensor = api.exchange.get_variable_handle(
            state, u"SITE OUTDOOR AIR DRYBULB TEMPERATURE", u"ENVIRONMENT")
        zoon_cool_sensor = api.exchange.get_variable_handle(
            state, u"Zone Air System Sensible Cooling Rate", u"SPACE1-1")
        outdoor_dew_point_actuator = api.exchange.get_actuator_handle(
            state, "Weather Data", "Outdoor Dry Bulb", "Environment")
        one_time = False
    oa_temp = api.exchange.get_variable_value(state, outdoor_temp_sensor)
    zone_cool_rate = api.exchange.get_variable_value(state, zoon_cool_sensor)
    zone_cool.append(zone_cool_rate)
    api.exchange.set_actuator_value(state, outdoor_dew_point_actuator, -5)

def saveJSON(data, name):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    with open(os.path.join(script_dir, 'pyep_outputs',name + '.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def loadJSONFromOutputs(name):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    with open(os.path.join(script_dir, 'pyep_outputs',name + '.json'), 'r') as f:
        testDict = json.loads(f.read())
    return testDict

api = EnergyPlusAPI()
state = api.state_manager.new_state()
api.runtime.callback_end_zone_timestep_after_zone_reporting(state, time_step_handler)
api.exchange.request_variable(state, "SITE OUTDOOR AIR DRYBULB TEMPERATURE", "ENVIRONMENT")
api.runtime.run_energyplus(state, sys.argv[1:])
# result = loadJSONFromOutputs('pyep_results')
# result["changed"] = zone_cool
# saveJSON(result, "pyep_results")

