import asyncio
import json
import time
import sys
import BLE_GATT
easytouch_devices={"kitchen":"XX:XX:XX:XX:XX:XX", #enter your bluetooth mac address here
                   "bedroom":"XX:XX:XX:XX:XX:XX",
                  }
MODEL_NBR_UUID = "2A24"
UUIDS = {
        "service":    '000000FF-0000-1000-8000-00805F9B34FB', #ro
        "jsonReturn": '0000FF01-0000-1000-8000-00805F9B34FB',
        "jsonCmd":    '0000EE01-0000-1000-8000-00805F9B34FB', #rw
        "strangeCmd": '0000DD01-0000-1000-8000-00805F9B34FB', #rw
        "unknown":    '00002a05-0000-1000-8000-00805f9b34fb',
}

async def ask_easytouch(location,command,arg):
    chars={}
    address=easytouch_devices[location]
    ubit= BLE_GATT.Central(address)
    ubit.connect()
    ubit.char_write(UUIDS["strangeCmd"], b'Cdw9@fL@6Gp7TXw')
    status=get_status(ubit)
    if command=="off":
      power(ubit,0)
    if command=="cool":
      cool_temp_set(ubit,status,int(arg))
    status=get_status(ubit)
    status['location']=location
    return status

def get_status(ubit):
    message=json.dumps({"Type":"Get Status","Zone":0,"EM":"dircery@gmail.com","TM":int(time.time())})
    ubit.char_write(UUIDS["jsonCmd"], bytes(message.encode('utf_8')))
   
    status=decript(bytes(ubit.char_read(UUIDS["jsonReturn"])).decode())
    return status
def power(ubit,mode): # mode 0=off, 1=on
    message=json.dumps({"Type": "Change", "Changes": {"zone": 0, "power": mode}})
    ubit.char_write(UUIDS["jsonCmd"], bytes(message.encode('utf_8')))
def cool_temp_set(ubit,status,temp): # mode 0=off, 1=on
    message=json.dumps({"Type": "Change", "Changes": {
       "zone": 0,
       "power":1,
       "mode":2,
       "cool_sp":temp,
#       "heat_sp":status["heat_sp"],
#       "dry_sp":status["dry_sp"],
#       "auto Cool_sp":status["autoCool_sp"],
#       "auto Heat_sp":status["sutoHeat_sp"],
       "coolFan":128, #set to Auto

    }})
    ubit.char_write(UUIDS["jsonCmd"], bytes(message.encode('utf_8')))
"""
"cool_sp":80
"heat_sp":72
"dry_sp":72
"auto Heat_sp":68
"auto Cool_sp":72
"coolFan":128


"mode":1

"fanOnly":1
"fanOnly":2
"fanOnly":0

"mode":4
"mode":2

"""


def decript(data):
#  print(data)
#  if len(data)<5:
#     return data.decode()
  status=json.loads(data)
  info=status['Z_sts']['0']
  param=status['PRM']
  modes={0:"off",3:"cool_on",4:"heat",2:"cool",1:"fan",11:"auto"}
  fan_modes={0:"off",1:"manuelL",2:"manuellH",65:"cycledL",66:"cycledH",128:"full auto",}
  hr_status={}
  hr_status['SN']=status['SN']
  hr_status['autoHeat_sp']=info[0]
  hr_status['autoCool_sp']=info[1]
  hr_status['cool_sp']=info[2]
  hr_status['heat_sp']=info[3]
  hr_status['dry_sp']=info[4]
  hr_status['u5']=info[5]
  hr_status['fan_mode_num']=info[6]
  hr_status['cool_mode_num']=info[7]
  hr_status['u8']=info[8]
  hr_status['u9']=info[9]
  hr_status['mode_num']=info[10]
  hr_status['heat_mode_num']=info[11]
  hr_status['facePlateTemperature']=info[12]
  hr_status['u13']=info[13]
  hr_status['u14']=info[14]
  hr_status['current_mode_num']=info[15]
  hr_status['ALL']=status
  if 7 in param:
    hr_status['off']=True
  if 15 in param:
    hr_status['on']=True
  
  if  hr_status['current_mode_num'] in modes:
     hr_status['current_mode']=modes[hr_status['current_mode_num']]
  if  hr_status['mode_num'] in modes:
     hr_status['mode']=modes[hr_status['mode_num']]
  if  hr_status['fan_mode_num'] in fan_modes:
     hr_status['fan_mode']=fan_modes[hr_status['fan_mode_num']]
  if  hr_status['cool_mode_num'] in fan_modes:
     hr_status['cool_mode']=fan_modes[hr_status['cool_mode_num']]
  if  hr_status['heat_mode_num'] in fan_modes:
     hr_status['heat_mode']=fan_modes[hr_status['heat_mode_num']]
  return hr_status
def main():
    if len(sys.argv)>2: 
      print(sys.argv)
      print(asyncio.run(ask_easytouch(sys.argv[1],sys.argv[2],sys.argv[3])))
    else:
      print("Usage: python3 easytouch.py [kitchen|bedroom] [off|cool|status] [temp]")


if __name__ == '__main__':
    main()


"""
[NEW] Primary Service (Handle 0x0000)
        /org/bluez/hci0/dev_C4_DE_E2_D3_83_92/service0001
        00001801-0000-1000-8000-00805f9b34fb
        Generic Attribute Profile
[NEW] Characteristic (Handle 0x0000)
        /org/bluez/hci0/dev_C4_DE_E2_D3_83_92/service0001/char0002
        00002a05-0000-1000-8000-00805f9b34fb
        Service Changed
[NEW] Descriptor (Handle 0x0000)
        /org/bluez/hci0/dev_C4_DE_E2_D3_83_92/service0001/char0002/desc0004
        00002902-0000-1000-8000-00805f9b34fb
        Client Characteristic Configuration
[NEW] Primary Service (Handle 0x0000)
        /org/bluez/hci0/dev_C4_DE_E2_D3_83_92/service0028
        000000ff-0000-1000-8000-00805f9b34fb
        Unknown
[NEW] Characteristic (Handle 0x0000)
        /org/bluez/hci0/dev_C4_DE_E2_D3_83_92/service0028/char0029
        0000ee01-0000-1000-8000-00805f9b34fb
        Unknown
[NEW] Characteristic (Handle 0x0000)
        /org/bluez/hci0/dev_C4_DE_E2_D3_83_92/service0028/char002b
        0000ff01-0000-1000-8000-00805f9b34fb
        Unknown
[NEW] Characteristic (Handle 0x0000)
        /org/bluez/hci0/dev_C4_DE_E2_D3_83_92/service0028/char002d
        0000dd01-0000-1000-8000-00805f9b34fb
        Unknown
"""
