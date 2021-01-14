import yaml, requests, os, webbrowser, string, re, platform, tempfile, shutil, time
from os import system
from time import sleep as delay
from difflib import SequenceMatcher as matcher

generate_temp_yaml = lambda path : shutil.copy2(path , os.path.join(tempfile.gettempdir() , "osrepo.tmp.yaml"))
request_download = lambda filename,path : open(filename , 'wb').write(requests.get(path ,allow_redirects=True).content)

def initialize() :
    # generate VARIABLES (if non-existent) and request file
    request_download("VARIABLES", "https://raw.githubusercontent.com/FreeTurk/OSRepo/stable/VARIABLES")
    # parse VARIABLES
    with open("VARIABLES" , "r") as f :
        var = yaml.safe_load(f)

    # generate osrepo.yaml (if non-existent) and request file
    request_download(var["yaml_filename"], var["yaml_link"])
    # parse osrepo.yaml
    with open(var["yaml_filename"] , "r") as stream :
        loaded_data = yaml.safe_load(stream)

    repo = loaded_data["os"]
    meta = loaded_data["meta"]
    return var , repo , meta

def download(link) :
    clear()
    confirm = input("Do you want to download this OS? (y/n): ")
    if confirm.upper() == "Y" : webbrowser.open(link)
    elif confirm.upper() == "N" :
        clear()
        print("download cancelled.")
        delay(.75)
        walk(repo)
    else :
        clear()
        print("invalid")
        delay(.5)
        clear()
        download(link)
    clear()

def index(dictionary , key='link') :
    if key in dictionary :
        yield ""
    for k , v in dictionary.items() :
        if isinstance(v , dict) :
            for s in index(v , key) :
                yield f" > {k}{s}"

def walk(current_dir) :
    items = []
    for item in current_dir :
        items.append(item)
        if item == "link" :
            download(current_dir["link"])
        else :
            print(item)
    bruh = input("\n>>")
    if bruh in items :
        clear()
        walk(current_dir[bruh])
    elif bruh.lower() == "main" or bruh.lower() == "back" :
        clear()
        walk(repo)
    else :
        clear()
        print("invaild.")
        delay(.5)
        clear()
        walk(current_dir)

def removeduplicate(list) :
    new = []
    for i in list :
        if i not in new :
            new.append(i)
    return new

def search(os_list , keywords_input , success_treshold=0.67) :
    start_time = time.time()
    # initial definitions
    filtered_input = []
    passed_filter = []

    # filter the input
    keywords = keywords_input[len("search ".lower()) :].split(",")
    for keyword in keywords :
        proper_keyword = keyword.strip("\'").strip("\"").strip(" ")
        filtered_input.append(proper_keyword)
    # print(filtered_input, "\n\n")

    # filter the OSes
    for path in os_list :
        # print("os path in operation: \t", path)
        filtered = list(filter(None , re.split(' > ' , path)))
        filtered_word_sensitive = re.sub('[' + string.punctuation + ']' , '> ' , path).split()
        while ">" in filtered :
            filtered == filtered.remove(">")
        while ">" in filtered_word_sensitive :
            filtered_word_sensitive == filtered_word_sensitive.remove(">")
        # print("keywords:\t\t ", filtered)
        # print("word sensitive:\t\t ", filtered_word_sensitive)
        # print("inputed keywords:\t ", filtered_input)

        # compare the values
        all_filtered = removeduplicate(filtered_word_sensitive + filtered)
        # print("----------------------------------------------")
        # print("success_treshold = " , success_treshold)
        for item in all_filtered :
            for keyword in filtered_input :
                matchval = round(matcher(None , keyword.lower() , item.lower()).ratio() , 3)
                # if matchval!=0:print(keyword , "to" , item, "\t--->", round(matchval*100, 3),"%")
                # else:print(keyword, "to", item, "\tNO MATCH")
                if matchval >= success_treshold : passed_filter.append(path)
        # print("\n\n")

    # finalize
    out = list(removeduplicate(passed_filter))
    if len(out) != 0 :info , success = str("{} results found in {} seconds".format(str(len(out)) , str(round(float(time.time() - start_time) , 3)))) , True
    else :info , success = "No search results found" , False
    return success , out , info

def clear() :
    if platform.system() == "Linux" : system("clear")
    if platform.system() == "Windows" : system("cls")

def interface() :
    print("""
OSRepo:

The only repo you'll need to download any kind of OSes.
Type 'help' to see a list of commands

Enter a command to continue:
""")

def help() :
    print("""
list
  //lists all OSes currently in the repo
  
download
  //where you can download the OSes
  
search <args>
  //you can search for any OS or group here!
    search <args> (multiple args can be used)  
help
  //a list of commands available
  
open
  //allows the user to read the repo in yaml formal
  
meta
  //goes to meta menu where you can see more info about the current repo
  
update (windows only)
  //installs the latest version of OSR if a new version is available
  
uninstall (windows only)
  //uninstall OSR
    """)

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def get_command(user) :
    if user.startswith("search ") :
        if remove_prefix(user, search).replace(" ", ""):
            success, search_result, info = search(all_oses_list, user)
    elif user == "list" :
        i = 0
        for os in all_oses_list :
            i += 1
            print("({}){}".format(i,os))
    elif user == "download" :
        clear()
        walk(repo)
    elif user == "help" :
        clear()
        help()
    elif user == "open" :
        clear()
        system("start " + generate_temp_yaml("osrepo.yaml"))
        main()

def main() :
    clear()
    interface()
    get_command(input("> ").lower())

if __name__ == "__main__" :
    clear()
    var, repo , meta = initialize()
    all_oses_list = index(repo)
    main()
