import yaml
from os import system
import requests
from time import sleep as delay
import os
import webbrowser
import re
import string
from difflib import SequenceMatcher as matcher
import re

def initialize():
    if not os.path.isfile(".\osrepo.yaml") :
        open("osrepo.yaml" , 'w+')
    r = requests.get("https://raw.githubusercontent.com/FreeTurk/OSRepo/stable/osrepo.yaml" ,allow_redirects=True)
    open('.\osrepo.yaml' , 'wb').write(r.content)
    with open("osrepo.yaml" , "r") as stream :
        loaded_data = yaml.safe_load(stream)
    repo = loaded_data["os"]
    return repo
def download(link):
    system("cls")
    confirm = input("Do you want to download this OS? (y/n): ")
    if confirm.upper() == "Y":
        webbrowser.open(link)
    elif confirm.upper() == "N":
        system("cls")
        print("download cancelled.")
        delay(.75)
        #                                               TODO: go to main menu here
    else:
        system("cls")
        print("invalid")
        delay(.5)
        system("cls")
        download(link)
    system("cls")

def index(dct, key='link'):
    if key in dct:
        yield ""
    for k, v in dct.items():
        if isinstance(v, dict):
            for s in index(v, key):
                yield f" > {k}{s}"

def walk(current_dir):
    items= []
    for item in current_dir:
        items.append(item)
        if item == "link":
            download(current_dir["link"])
        else:
            print(item)
    bruh = input("\n>>")
    if bruh in items:
        system("cls")
        walk(current_dir[bruh])
    elif bruh.lower() == "main" or bruh.lower() == "back":
        system("cls")
        walk(repo)
    else:
        system("cls")
        print("invaild.")
        delay(.5)
        system("cls")
        walk(current_dir)
class OSobj:
    def __init__(self , name, path) :
        self.name = name
        self.path = path

def removeduplicate(list):
    new=[]
    for i in list:
        if i not in new:
            new.append(i)
    return new

def search(os_list, keywords_input, success_treshold = 0.67, try_count=0):
    #initial definitions
    filtered_input = []
    passed_filter = []

    #filter the input
    keywords = keywords_input[len("search ".lower()):].split(",")
    for keyword in keywords:
        proper_keyword = keyword.strip("\'").strip("\"").strip(" ")
        filtered_input.append(proper_keyword)
    #print(filtered_input, "\n\n")

    #filter the OSes
    for path in os_list:
        #print("os path in operation: \t", path)
        filtered = list(filter(None, re.split(' > ' , path)))
        filtered_word_sensitive = re.sub('[' + string.punctuation + ']' , '> ' , path).split()
        while ">" in filtered:
            filtered == filtered.remove(">")
        while ">" in filtered_word_sensitive:
            filtered_word_sensitive == filtered_word_sensitive.remove(">")
        #print("keywords:\t\t ", filtered)
        #print("word sensitive:\t\t ", filtered_word_sensitive)
        #print("inputed keywords:\t ", filtered_input)

        #compare the values
        all_filtered = removeduplicate(filtered_word_sensitive + filtered)
        #print("----------------------------------------------")
        #print("success_treshold = " , success_treshold)
        for item in all_filtered:
            for keyword in filtered_input:
                matchval = round(matcher(None , keyword.lower() , item.lower()).ratio(), 3)
                #if matchval!=0:
                    #print(keyword , "to" , item, "\t--->", round(matchval*100, 3),"%")
                #else:
                    #print(keyword, "to", item, "\tNO MATCH")
                if matchval >= success_treshold:
                    passed_filter.append(path)
        #print("\n\n")

    return list(removeduplicate(passed_filter))

if __name__ == "__main__":
    bruhh = input(">> ")
    import time
    start_time = time.time()
    repo = initialize()
    all_oses_list = index(repo)
    print()
    result = search(all_oses_list , bruhh)
    print(len(result), "search result(s):")
    for i in result:
        print(i)
    print("\nprocess completed in:\n--- %s seconds ---" % round((time.time() - start_time),2))