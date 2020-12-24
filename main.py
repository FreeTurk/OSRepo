"""all_oss = []
class OSobj:
    def __init__(self , name , repo_item, group) :
        self.repo_item = repo_item
        self.name = name
        self.group = group
        #if group != None:
        #    self.link = repo[group][name]["link"]
        #else:
        #    self.link = repo[name]["link"]
def createosobject(name, group=None):
    if group == None :
        path = repo[name]
        for os in path:
            if os!="TYPE":
                print("  os:", os)
    if group != None :
        path = repo[group][name]
        for os in path:
            if os!="TYPE" and name!="TYPE":
                print("  ", name, ">",os)
    for os in path:
        if os != "TYPE" and name != "TYPE" :
            current_obj = OSobj(os, group, name)
            all_oss.append(current_obj)
import yaml
with open("osrepo.yaml", "r") as stream:
    loaded_data = yaml.safe_load(stream)
repo = loaded_data["os"]
for index in repo:
    repo_item = repo[index]
    print(index)
    type = repo_item["TYPE"]
    if type == "os_list":
         createosobject(index)
    elif type == "os_group":
        os_list = repo_item
        for name in os_list:
            createosobject(name, index)
for x in all_oss:
    if x.repo_item != None:
        print(x.repo_item, ">", x.group, ">", x.name)
    else:
        print(x.name)"""

import yaml
from os import system
import requests
from time import sleep as delay
import os
if not os.path.isfile(".\osrepo.yaml"):
    file = open("osrepo.yaml" , 'w+')
r = requests.get("https://raw.githubusercontent.com/FreeTurk/OSRepo/stable/osrepo.yaml", allow_redirects=True)
open('.\osrepo.yaml', 'wb').write(r.content)
with open("osrepo.yaml", "r") as stream:
    loaded_data = yaml.safe_load(stream)
repo = loaded_data["os"]
def link(link):
    print(link)
def walk(current_dir):
    items= []
    for item in current_dir:
        items.append(item)
        print(item)
    bruh = input("\n>>")
    if bruh in items:
        system("cls")
        walk(current_dir[bruh])
    elif bruh.lower() == "main" or "back":
        system("cls")
        walk(repo)
walk(repo)