print("Checking for updates...")

import requests
import time
import json
import webbrowser

print("                                                                                                                  ")
print("                                                                                                                  ")
print("     OOOOOOOOO        SSSSSSSSSSSSSSS                                                                             ")
print("   OO:::::::::OO    SS:::::::::::::::S                                                                            ")
print(" OO:::::::::::::OO S:::::SSSSSS::::::S                                                                            ")
print("O:::::::OOO:::::::OS:::::S     SSSSSSS                                                                            ")
print("O::::::O   O::::::OS:::::S           rrrrr   rrrrrrrrr       eeeeeeeeeeee    ppppp   ppppppppp      ooooooooooo   ")
print("O:::::O     O:::::OS:::::S           r::::rrr:::::::::r    ee::::::::::::ee  p::::ppp:::::::::p   oo:::::::::::oo ")
print("O:::::O     O:::::O S::::SSSS        r:::::::::::::::::r  e::::::eeeee:::::eep:::::::::::::::::p o:::::::::::::::o")
print("O:::::O     O:::::O  SS::::::SSSSS   rr::::::rrrrr::::::re::::::e     e:::::epp::::::ppppp::::::po:::::ooooo:::::o")
print("O:::::O     O:::::O    SSS::::::::SS  r:::::r     r:::::re:::::::eeeee::::::e p:::::p     p:::::po::::o     o::::o")
print("O:::::O     O:::::O       SSSSSS::::S r:::::r     rrrrrrre:::::::::::::::::e  p:::::p     p:::::po::::o     o::::o")
print("O:::::O     O:::::O            S:::::Sr:::::r            e::::::eeeeeeeeeee   p:::::p     p:::::po::::o     o::::o")
print("O::::::O   O::::::O            S:::::Sr:::::r            e:::::::e            p:::::p    p::::::po::::o     o::::o")
print("O:::::::OOO:::::::OSSSSSSS     S:::::Sr:::::r            e::::::::e           p:::::ppppp:::::::po:::::ooooo:::::o")
print(" OO:::::::::::::OO S::::::SSSSSS:::::Sr:::::r             e::::::::eeeeeeee   p::::::::::::::::p o:::::::::::::::o")
print("   OO:::::::::OO   S:::::::::::::::SS r:::::r              ee:::::::::::::e   p::::::::::::::pp   oo:::::::::::oo ")
print("     OOOOOOOOO      SSSSSSSSSSSSSSS   rrrrrrr                eeeeeeeeeeeeee   p::::::pppppppp       ooooooooooo   ")
print("                                                                              p:::::p                             ")
print("                                                                              p:::::p                             ")
print("                                                                             p:::::::p                            ")
print("                                                                             p:::::::p                            ")
print("                                                                             p:::::::p                            ")
print("                                                                             ppppppppp                            ")
print("                                                                                                                  ")



print("WELCOME TO THE BIGGEST REPO OF OPERATING SYSTEMS!")
print("HERE, YOU WILL FIND A GREAT SELECTION OF OPERATING SYSTEMS, ALL HAND PICKED!")
print("This is a dumb project, made by the priceless efforts of FreeTurk")
print("")

print("Throughout this script, you will be presented with a series of options.")
print("Select accordingly, you have to know the category if you want the OS.")
print("")

print("Now, please select the type of your OS from the options of (case sensitive)")
print("*nix")
print("WindowsNT")
print("WindowsDOS")
print("Apple")
print("Legendary")
os_type = input()

if os_type == "*nix":
    print("Select from below options")
    print("Linux")
    print("Unix")
    print("BSD")
    nix_type = input()
    if nix_type == "Linux":
        print("A list of operating systems will come up, this may/should lag...")
        time.sleep(2)
        with open('linuxmain.json', 'r') as f:
            linux_dict = json.load(f)

        for linux_distro in linux_dict:
            print(linux_distro['Name'])

        linux_input = input("What OS do you want?")

        for linux_distro in linux_dict:
            print(linux_distro[linux_input + " Versions"])

        linux_ver_input = input("What version..?")

        for linux_distro in linux_dict:
            webbrowser.open(linux_distro[linux_input + " " + linux_ver_input])