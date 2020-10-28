import time
import webbrowser
import json

with open('winntmain.json', 'r') as dict:
    winnt_dict = json.load(dict)

print(winnt_dict["winnt"]["Names"])


input = input("What OS do you want")

webbrowser.open(winnt_dict["winnt"][input]["link"])

