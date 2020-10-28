import webbrowser
import json

with open('apple.json', 'r') as wut:
    apple_dict = json.load(wut)

print(apple_dict["apple"]["Names"])

input = input("What OS do you want?")

webbrowser.open(apple_dict["apple"][input]["link"])