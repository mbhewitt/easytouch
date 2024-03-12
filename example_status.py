from easytouch import ask_easytouch
import time
import asyncio

for sublocation in ('kitchen','bedroom'):
  status=asyncio.run(ask_easytouch(sublocation,"status","85"))
  tag={'location':location,'subLocation':sublocation,'SN':status['SN']}
  values={ 'autoHeat_sp': float(status['autoHeat_sp']),
           'autoCool_sp': float(status['autoCool_sp']), 
           'cool_sp':  float(status['cool_sp']), 
           'heat_sp':  float(status['heat_sp']), 
           'dry_sp':  float(status['dry_sp']), 
           'fan_mode_num': status['fan_mode_num'], 
           'cool_mode_num': status['cool_mode_num'], 
           'mode_num': status['mode_num'], 
           'heat_mode_num': status['heat_mode_num'], 
           'facePlateTemperature': float(status['facePlateTemperature']), 
           'current_mode_num': status['current_mode_num']} #0=off #3=cool_on
  print($tags,$values)
