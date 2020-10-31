import webbrowser
import json

with open('others.json', 'r') as enough:
    others_dict = json.load(enough)

print(others_dict["others"]["Names"])

input = input("What OS do you want?")

webbrowser.open(others_dict["others"][input]["link"])