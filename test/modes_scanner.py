import json

from pylgbst.hub import SmartHub

# logging.basicConfig(level=logging.DEBUG)

hub = SmartHub(address='86996732-BF5A-433D-AACE-5611D4C6271D')   # test hub
# hub = HandsetRemote(address='2BC6E69B-5F56-4716-AD8C-7B4D5CBC7BF8')  # test handset
# hub = RemoteHandset(address='5D319849-7D59-4EBB-A561-0C37C5EF8DCD')  # train handset

descr = {}
values = hub.peripherals.values()

print("@@@@ modes_scanner.py 15: ", values)

# for dev in values:
dev = hub.peripherals[1]
descr[str(dev)] = dev.describe_possible_modes()
# print("@@@@ modes_scanner.py 15: ", dev)
print("@@@@ modes_scanner.py 16: ", dev.describe_possible_modes())

print("@@@@ modes_scanner.py 24: ", descr )

with open("descr_color_sensor.json", "w") as fhd:
    json.dump(descr, fhd, indent=True)
