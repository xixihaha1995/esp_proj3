import sys, _0_util as util
sys.path.insert(0, 'C:\EnergyPlusV22-1-0')

from pyenergyplus.api import EnergyPlusAPI
one_time = True
outdoor_temp_sensor = 0
outdoor_dew_point_actuator = 0
oat_lst = []
ele_hvac_lst = []
solar_lst = []
zone_cool_lst = []
def time_step_handler(state):
    global one_time , oat_handle,  elec_hvac_handle, solar_handle, zoon_cool_handle
    if one_time:
        if not api.exchange.api_data_fully_ready(state):
            return
        oat_handle = api.exchange.get_variable_handle(
            state, u"SITE OUTDOOR AIR DRYBULB TEMPERATURE", u"ENVIRONMENT")
        elec_hvac_handle = api.exchange.get_meter_handle(state, "Electricity:HVAC")
        solar_handle = api.exchange.get_variable_handle(
            state, u"Site Direct Solar Radiation Rate per Area", u"ENVIRONMENT")
        zoon_cool_handle = api.exchange.get_variable_handle(
            state, u"Zone List Sensible Cooling Energy", u"EntireBuilding")
        one_time = False
    oat_val = api.exchange.get_variable_value(state, oat_handle)
    elec_hvac_value = api.exchange.get_meter_value(state, elec_hvac_handle)
    solar_val = api.exchange.get_variable_value(state, solar_handle)
    zone_cool_val = api.exchange.get_variable_value(state, zoon_cool_handle)
    oat_lst.append(oat_val)
    ele_hvac_lst.append(elec_hvac_value)
    solar_lst.append(solar_val)
    zone_cool_lst.append(zone_cool_val)
api = EnergyPlusAPI()
state = api.state_manager.new_state()
api.runtime.callback_end_zone_timestep_after_zone_reporting(state, time_step_handler)
api.exchange.request_variable(state, "Zone List Sensible Cooling Energy", "EntireBuilding")
api.runtime.run_energyplus(state, sys.argv[1:])
result = util.loadJSONFromOutputs('pyep_results')
result["oat"] = oat_lst
result["elec_hvac"] = ele_hvac_lst
result["solar"] = solar_lst
result["zone_cool"] = zone_cool_lst
print(zone_cool_lst)
util.saveJSON(result, "pyep_results")

