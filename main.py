from tkinter import Tk
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from os import system
from difflib import SequenceMatcher as matcher
import yaml , requests , os , webbrowser , string , re , tempfile , shutil , time , sys ,platform

# back end

generate_temp_yaml = lambda path : shutil.copy2(path , os.path.join(tempfile.gettempdir() , "osrepo.tmp.yaml"))
request_download = lambda filename , path : open(filename , 'wb').write(requests.get(path , allow_redirects=True).content)

def initialize() :
    # generate VARIABLES (if non-existent) and request file
    request_download("VARIABLES" , "https://raw.githubusercontent.com/FreeTurk/OSRepo/stable/VARIABLES")
    # parse VARIABLES
    with open("VARIABLES" , "r") as f :
        var = yaml.safe_load(f)

    # generate osrepo.yaml (if non-existent) and request file
    request_download(var["yaml_filename"] , var["yaml_link"])
    # parse osrepo.yaml
    with open(var["yaml_filename"] , "r") as stream :
        loaded_data = yaml.safe_load(stream)

    repo = loaded_data["os"]
    meta = loaded_data["meta"]
    return var , repo , meta

def download(link) :
    confirm = input("Do you want to download this OS? (y/n): ")
    if confirm.upper() == "Y" :
        webbrowser.open(link)
    elif confirm.upper() == "N" :
        print("download cancelled.")

def index(dictionary , key='link') :
    if key in dictionary :
        yield ""
    for k , v in dictionary.items() :
        if isinstance(v , dict) :
            for s in index(v , key) :
                yield f" > {k}{s}"

def walk(repo , current_dir) :
    items = []
    for item in current_dir :
        items.append(item)
        if item == "link" :
            download(current_dir["link"])
        else :
            print(item)
    bruh = input("\n>>")
    if bruh in items :
        walk(current_dir[bruh])
    elif bruh.lower() == "main" or bruh.lower() == "back" :
        walk(repo)
    else :
        print("invaild.")
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
    if len(out) != 0 :
        info , success = str("{} results found in {} seconds".format(str(len(out)) , str(round(float(time.time() - start_time) , 3)))) , True
    else :
        info , success = "No search results found" , False
    return success , out , info

def remove_prefix(text , prefixstr) :
    if text.startswith(prefixstr) :
        return text[len(prefixstr) :]
    return text

# gui

app = QApplication([])

def rgb(r , g , b) : return f"rgb({r},{g},{b})" , (r , g , b)

def font(os):
    if os == "windows": return "Segoe UI"
    elif os == "linux": return "Ubuntu Sans" # uses ubuntu sans if available, uses fallback font if its a distro other than ubuntu
    elif os == "darwin": return "Helvetica"
    # uses default font as fallback if font not available

class ui :
    winx , winy = 300 , 380
    margin = 16
    font , fontsize = font(platform.system().lower()) , 14
    quitbuttonsize = 32

    class style :
        # colors
        class colors :
            # window
            win_border = rgb(24 , 24 , 30)
            background = rgb(18 , 18 , 18)
            text = rgb(160 , 160 , 177)
            accent = rgb(60 , 172 , 210)
            # box
            box = rgb(30 , 30 , 32)
            box_hover = rgb(40 , 40 , 42)
            box_active = rgb(86 , 92 , 100)
            border = rgb(30 , 30 , 30)

        # stylesheets

        button_modern = """
            QPushButton{{
                border-top-right-radius:6px;
                background: {box} ;
                border-width: 1px; border-style: solid; border-color: {border}; border-radius: 5px;}}
            QPushButton:hover{{
                border-width: 1px; border-style: solid; border-color: {accent}; border-radius: 5px;
                background: {active} ;}}
            QPushButton:hover:!pressed{{
                border-width: 1px; border-style: solid; border-color: {border}; border-radius: 5px;
                background: {hover} ;}}
        """.format(box=colors.box[0] , accent=colors.accent[0] , hover=colors.box_hover[0] , border=colors.border[0] , active=colors.box_active[0])
        searchbutton = """
            QPushButton{{
                border-width: 1px; border-style: solid; border-color: {border};
                border-bottom-right-radius: 12px; border-bottom-left-radius: 2px; border-top-right-radius: 12px; border-top-left-radius: 2px;
                background: {box} ;}}
            QPushButton:hover{{
                border-width: 1px; border-style: solid; border-color: {accent};
                border-bottom-right-radius: 12px; border-bottom-left-radius: 2px; border-top-right-radius: 12px; border-top-left-radius: 2px;
                background:{active};}}
            QPushButton:hover:!pressed{{
                border-width: 1px; border-style: solid; border-color:{border};
                border-bottom-right-radius: 12px; border-bottom-left-radius: 2px; border-top-right-radius: 12px; border-top-left-radius: 2px;
                background:{hover};}}
        """.format(box=colors.box[0] , accent=colors.accent[0] , hover=colors.box_hover[0] , border=colors.border[0] , active=colors.box_active[0])
        button_close = """
            QPushButton{{
                background: {box} ;
                border-radius: 1px;
                border-style: none;}}
            QPushButton:hover{{
                background:rgb(100,10,30);}}
            QPushButton:hover:!pressed{{
                background:rgb(200,20,40);}}
        """.format(box=colors.box[0])
        searchbar = """
            QLineEdit{{
                background-color: {box};
                border-width: 1px; border-style: solid; border-color: {border};
                border-bottom-right-radius: 2px; border-bottom-left-radius: 12px; border-top-right-radius: 2px; border-top-left-radius: 12px;}}
        """.format(box=colors.box[0] , border=colors.border[0])

tk = Tk()
style = ui.style

# Dark Mode by Default
app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window , QColor(*style.colors.background[1]))
palette.setColor(QPalette.WindowText , QColor(*style.colors.text[1]))
palette.setColor(QPalette.Base , QColor(*style.colors.box[1]))
palette.setColor(QPalette.AlternateBase , QColor(*style.colors.box[1]))
palette.setColor(QPalette.ToolTipBase , Qt.white)
palette.setColor(QPalette.ToolTipText , Qt.white)
palette.setColor(QPalette.Text , Qt.white)
palette.setColor(QPalette.Button , QColor(*style.colors.box[1]))
palette.setColor(QPalette.ButtonText , Qt.white)
palette.setColor(QPalette.BrightText , Qt.yellow)
palette.setColor(QPalette.Link , QColor(*style.colors.accent[1]))
palette.setColor(QPalette.Highlight , QColor(*style.colors.accent[1]))
palette.setColor(QPalette.HighlightedText , Qt.black)

app.setPalette(palette)
app.setApplicationName("OSRepo")

def winpos(dispx , dispy , winx=ui.winx , winy=ui.winy) :
    if winx % 2 != 0 : winx += 1
    if winy % 2 != 0 : winy += 1
    return int((dispx / 2) - (winx / 2)) , int((dispy / 2) - (winy / 2))

def label(window , content="label" , geometry=((0 , 0) , (20 , 20)) , qss=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    posxpercent , posypercent = int((posx * ui.winx) / 100) , int((posy * ui.winy) / 100)
    sizexpercent , sizeypercent = int((sizex * ui.winx) / 100) , int((sizey * ui.winy) / 100)
    label = QLabel(window)
    label.setText(content)
    label.setGeometry(posxpercent , posypercent , sizexpercent , sizeypercent)
    if qss != None : label.setStyleSheet(qss)
    return label

def flex_button(item , content="Button" , geometry=((0 , 0) , (20 , 20)) , onclick=None , tooltip=None , margin=(ui.margin , ui.margin) , qss=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    marginx , marginy = margin
    posxpercent , posypercent = round(int((posx * ui.winx) / 100) + marginx) , round(int((posy * ui.winy) / 100) + marginy)
    sizexpercent , sizeypercent = round(int((sizex * ui.winx) / 100) - (marginx * 2)) , round(int((sizey * ui.winy) / 100) - (marginy * 2))
    buttonobject = QPushButton(content , item)
    buttonobject.setGeometry(posxpercent , posypercent , sizexpercent , sizeypercent)
    if qss != None : buttonobject.setStyleSheet(qss)
    if tooltip != None : buttonobject.setToolTip(tooltip)
    if onclick != None : buttonobject.clicked.connect(onclick)
    return buttonobject

def button(item , content="Button" , geometry=((0 , 0) , (20 , 20)) , onclick=None , tooltip=None , qss=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    buttonobject = QPushButton(content , item)
    buttonobject.setGeometry(round(posx) , round(posy) , round(sizex) , round(sizey))
    if qss != None : buttonobject.setStyleSheet(qss)
    if tooltip != None : buttonobject.setToolTip(tooltip)
    if onclick != None : buttonobject.clicked.connect(onclick)
    return buttonobject

def searchbar(item , content="search" , geometry=((0 , 0) , (20 , 20)) , margin=(ui.margin , ui.margin) , qss=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    marginx , marginy = margin
    posxpercent , posypercent = int((posx * ui.winx) / 100) + marginx , int((posy * ui.winy) / 100) + marginy
    sizexpercent , sizeypercent = int((sizex * ui.winx) / 100) - (marginx * 2) , int((sizey * ui.winy) / 100) - (marginy * 2)
    inputobject = QLineEdit(item)
    inputobject.setPlaceholderText(content)
    inputobject.setGeometry(posxpercent , posypercent , sizexpercent , sizeypercent)
    if qss != None : inputobject.setStyleSheet(qss)
    return inputobject

def quitbutton(obj) : return button(obj , "X" , ((ui.winx - (ui.quitbuttonsize + ui.margin / 2) - 14 , (ui.margin / 2) + 2) , (ui.quitbuttonsize + 12 , ui.quitbuttonsize)) , lambda self : QCoreApplication.exit(0) , qss=style.button_close)

class MainMenu(QWidget) :

    def __init__(self , parent=None) :
        QWidget.__init__(self , parent=parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0 , 0 , 0 , 0)
        self.layout.addStretch(-1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.setWindowTitle("OSRepo")
        self.setGeometry(*winpos(tk.winfo_screenwidth() , tk.winfo_screenheight()) , ui.winx , ui.winy)
        self.setFixedSize(ui.winx , ui.winy)
        self.setStyleSheet(
            """
            font-family: {font};
            font-size: {fontsize}px;
            border: 1px solid {border};
            """.format(font=ui.font , fontsize=str(ui.fontsize) , border=style.colors.win_border[0]))
        # header
        # quit button TODO: add an ubuntu-style quit button for linux only
        quitbutton(self)
        # search bar
        searchbar(self , " search" , ((0 , 0) , (74 , 14)) , qss=style.searchbar , margin=(10 , 10))
        flex_button(self , ">" , ((68 , 0) , (15 , 14)) , self.search , qss=style.searchbutton , margin=(10 , 10))

        # info label
        label(self , f"{'138'} OSs found\nLast updated: {'17-1-2021'}" , ((0 , 40) , (100 , 15)) , qss="qproperty-alignment: AlignCenter;border-style:none;")  # TODO: assign variables to get last update from meta and number of OSs from index()
        label(self , r'<img src=.\icons\app\text.svg>' , ((33 , 16) , (35 , 20)) , qss="border-style:none;")
        label(self , f"{'v1.12.0'}" , ((0 , 32) , (100 , 4)) , qss="qproperty-alignment: AlignCenter;border-style:none;")  # TODO: assign 'version' variable here

        # buttons
        # main buttons
        flex_button(self , "See All OSs" , ((0 + (ui.margin / 8) , 55) , (50 , 30)) , self.func , qss=style.button_modern)
        flex_button(self , "Download\nan OS" , ((50 - (ui.margin / 8) , 55) , (50 , 30)) , self.func , qss=style.button_modern)
        # footer
        flex_button(self , "More..." , ((0 , 90 - ui.margin / 4) , (82 , 10)) , self.func , margin=((ui.margin * 1.5) , 0) , qss=style.button_modern)
        flex_button(self , "?" , ((82 - (ui.margin / 4) , 90 - ui.margin / 4) , (18 , 10)) , self.func , "Help" , margin=(ui.margin / 2 , 0) , qss=style.button_modern)
        self.show()

    def func(self) :
        print("function called!")

    def search(self) :
        print("search")

class MorePage(QWidget) :

    def __init__(self , parent=None) :
        QWidget.__init__(self , parent=parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0 , 0 , 0 , 0)
        self.layout.addStretch(-1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.setWindowTitle("OSRepo")
        self.setGeometry(*winpos(tk.winfo_screenwidth() , tk.winfo_screenheight()) , ui.winx , ui.winy)
        self.setFixedSize(ui.winx , ui.winy)
        self.setStyleSheet(
            """
            font-family: {font};
            font-size: {fontsize}px;
            border: 1px solid {border};
            """.format(font=ui.font , fontsize=str(ui.fontsize) , border=style.colors.win_border[0]))

        # header
        flex_button(self , "<back" , ((0 , 0) , (25 , 12)) , self.back , qss=style.button_modern , margin=(ui.margin / 2 , ui.margin / 2))
        quitbutton(self)

        # main
        flex_button(self , "OSR on GitHub" , ((20 , 20) , (60 , 25)) , lambda self : webbrowser.open("www.github.com/freeturk/osrepo") , qss=style.button_modern)
        flex_button(self , "Open Repo in\nText Editor" , ((20 , 40) , (60 , 25)) , lambda self : system(f"start {shutil.copy2('osrepo.yaml' , os.path.join(tempfile.gettempdir() , 'osrepo.tmp.yaml'))}") , qss=style.button_modern)

        # footer
        label(self , "made with \u2665 by \n@baris-inandi and @FreeTurk" , ((0 , 70) , (100 , 25)) , qss="border-style:none;qproperty-alignment: AlignCenter;")

        self.show()

    def back(self) :
        print("back")

class Window(QMainWindow) :

    def __init__(self) :
        mainmenu = MainMenu()
        morepage = MorePage()
        self.Stack = mainmenu

def quit() : QCoreApplication.quit()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
