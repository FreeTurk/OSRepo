import webbrowser
import json

with open('bsd.json', 'r') as wut:
    apple_dict = json.load(wut)

print(apple_dict["bsd"]["Names"])

input = input("What OS do you want?")

webbrowser.open(apple_dict["bsd"][input]["link"])