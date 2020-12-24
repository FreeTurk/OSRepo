all_oss = []
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
    if x.group != None:
        print(x.repo_item, ">", x.group, ">", x.name)
    else:
        print(x.name)