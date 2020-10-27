import time
import webbrowser
import json


print("A list of operating systems will come up, this may/should lag...")

time.sleep(2)
with open('linuxmain.json', 'r') as f:
    linux_dict = json.load(f)

print(linux_dict["linux"]["Names"])

linux_input = input("What OS do you want?")

print(linux_dict["linux"][linux_input]["versions"])

linux_ver_input = input("What version..?")

webbrowser.open(linux_dict["linux"][linux_input][linux_ver_input])