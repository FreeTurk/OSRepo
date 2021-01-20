from tkinter import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import yaml, requests, os, webbrowser, string, re, platform, tempfile, shutil, time, sys
from os import system
from time import sleep as delay
from difflib import SequenceMatcher as matcher

app = QApplication([])

def rgb(r,g,b):
    return "rgb({},{},{})".format(r,g,b), (r,g,b)

class ui :

    winx , winy = 300 , 380
    margin = 16
    # TODO: check OS, use Ubuntu, Segoe UI for linux and win respectively
    font, fontsize = "Segoe UI", 14
    quitbuttonsize = 32

    class style:

        # colors
        class colors:
            # window
            win_border =    rgb(24,24,30)
            background =    rgb(18,18,18)
            text =          rgb(160,160,177)
            accent =        rgb(60,172,210)
            # box
            box =           rgb(30,30,32)
            box_hover =     rgb(40,40,42)
            box_active =    rgb(86,92 ,100)
            border =        rgb(30,30,30)

        # stylesheets

        button_modern="""
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
        """.format(box=colors.box[0], accent=colors.accent[0], hover=colors.box_hover[0], border=colors.border[0], active=colors.box_active[0])
        searchbutton="""
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
        """.format(box=colors.box[0], accent=colors.accent[0], hover=colors.box_hover[0], border=colors.border[0], active=colors.box_active[0])
        button_close="""
            QPushButton{{
                background: {box} ;
                border-radius: 1px;
                border-style: none;}}
            QPushButton:hover{{
                background:rgb(100,10,30);}}
            QPushButton:hover:!pressed{{
                background:rgb(200,20,40);}}
        """.format(box=colors.box[0])
        searchbar="""
            QLineEdit{{
                background-color: {box};
                border-width: 1px; border-style: solid; border-color: {border};
                border-bottom-right-radius: 2px; border-bottom-left-radius: 12px; border-top-right-radius: 2px; border-top-left-radius: 12px;}}
        """.format(box=colors.box[0],border=colors.border[0])

tk = Tk()
style = ui.style

# Dark Mode
app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window ,              QColor(*style.colors.background[1]))
palette.setColor(QPalette.WindowText ,          QColor(*style.colors.text[1]))
palette.setColor(QPalette.Base ,                QColor(*style.colors.box[1]))
palette.setColor(QPalette.AlternateBase ,       QColor(*style.colors.box[1]))
palette.setColor(QPalette.ToolTipBase ,         Qt.white)
palette.setColor(QPalette.ToolTipText ,         Qt.white)
palette.setColor(QPalette.Text ,                Qt.white)
palette.setColor(QPalette.Button ,              QColor(*style.colors.box[1]))
palette.setColor(QPalette.ButtonText ,          Qt.white)
palette.setColor(QPalette.BrightText ,          Qt.yellow)
palette.setColor(QPalette.Link ,                QColor(*style.colors.accent[1]))
palette.setColor(QPalette.Highlight ,           QColor(*style.colors.accent[1]))
palette.setColor(QPalette.HighlightedText ,     Qt.black)

app.setPalette(palette)
app.setApplicationName("OSRepo")

def winpos(dispx , dispy , winx=ui.winx , winy=ui.winy) :
    if winx % 2 != 0 : winx += 1
    if winy % 2 != 0 : winy += 1
    return int((dispx / 2) - (winx / 2)) , int((dispy / 2) - (winy / 2))

def label(window , content="label" , geometry=((0 , 0) , (20 , 20)) , qss=None):
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    posxpercent , posypercent =     int((posx * ui.winx) / 100) ,       int((posy * ui.winy) / 100)
    sizexpercent , sizeypercent =   int((sizex * ui.winx) / 100) ,      int((sizey * ui.winy) / 100)
    label = QLabel(window)
    label.setText(content)
    label.setGeometry(posxpercent , posypercent , sizexpercent , sizeypercent)
    if qss != None : label.setStyleSheet(qss)
    return label

def flex_button(item , content="Button" , geometry=((0 , 0) , (20 , 20)) , onclick=None , tooltip=None , margin=(ui.margin, ui.margin), qss=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    marginx,marginy = margin
    posxpercent , posypercent =     round(int((posx * ui.winx) / 100) + marginx) ,             round(int((posy * ui.winy) / 100) + marginy)
    sizexpercent , sizeypercent =   round(int((sizex * ui.winx) / 100) - (marginx * 2)) ,      round(int((sizey * ui.winy) / 100) - (marginy * 2))
    buttonobject = QPushButton(content , item)
    buttonobject.setGeometry(posxpercent , posypercent , sizexpercent , sizeypercent)
    if qss!=None: buttonobject.setStyleSheet(qss)
    if tooltip != None : buttonobject.setToolTip(tooltip)
    if onclick != None : buttonobject.clicked.connect(onclick)
    return buttonobject

def button(item , content="Button" , geometry=((0,0),(20,20)) , onclick=None , tooltip=None , qss=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    buttonobject = QPushButton(content , item)
    buttonobject.setGeometry(round(posx) , round(posy) , round(sizex) , round(sizey))
    if qss!=None: buttonobject.setStyleSheet(qss)
    if tooltip != None : buttonobject.setToolTip(tooltip)
    if onclick != None : buttonobject.clicked.connect(onclick)
    return buttonobject

def searchbar(item , content="search" , geometry=((0 , 0) , (20 , 20)) ,  margin=(ui.margin, ui.margin), qss=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    marginx,marginy = margin
    posxpercent , posypercent =     int((posx * ui.winx) / 100) + marginx ,             int((posy * ui.winy) / 100) + marginy
    sizexpercent , sizeypercent =   int((sizex * ui.winx) / 100) - (marginx * 2) ,      int((sizey * ui.winy) / 100) - (marginy * 2)
    inputobject = QLineEdit(item)
    inputobject.setPlaceholderText(content)
    inputobject.setGeometry(posxpercent , posypercent , sizexpercent , sizeypercent)
    if qss!=None: inputobject.setStyleSheet(qss)
    return inputobject

class MainMenu(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.layout  = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
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
        """.format(font=ui.font, fontsize=str(ui.fontsize), border=style.colors.win_border[0]))
        # header
        # quit button TODO: add an ubuntu-style quit button for linux only
        button(self , "X" , ((ui.winx - (ui.quitbuttonsize + ui.margin / 2) - 14 , (ui.margin / 2) + 2) , (ui.quitbuttonsize + 12 , ui.quitbuttonsize)) , quit ,qss=style.button_close)
        # search bar
        searchbar(self , " search" , ((0 , 0) , (74 , 14)) , qss=style.searchbar , margin=(10 , 10))
        flex_button(self , ">" , ((68 , 0) , (15 , 14)) , self.search , qss=style.searchbutton , margin=(10 , 10))

        # info label
        label(self , f"{'138'} OSs found\nLast updated: {'17-1-2021'}" , ((0 , 40) , (100 , 15)) ,qss="qproperty-alignment: AlignCenter;border-style:none;")  # TODO: assign variables to get last update from meta and number of OSs from index()
        label(self , r'<img src=.\icons\app\text.svg>' , ((33 , 16) , (35 , 20)) , qss="border-style:none;")
        label(self , f"{'v1.12.0'}" , ((0 , 32) , (100 , 4)) ,qss="qproperty-alignment: AlignCenter;border-style:none;")  # TODO: assign 'version' variable here

        # buttons
        # main buttons
        flex_button(self , "See All OSs" , ((0 + (ui.margin / 8) , 55) , (50 , 30)) , self.func , qss=style.button_modern)
        flex_button(self , "Download\nan OS" , ((50 - (ui.margin / 8) , 55) , (50 , 30)) , self.func , qss=style.button_modern)
        # footer
        flex_button(self , "More..." , ((0 , 90 - ui.margin / 4) , (82 , 10)) , self.func , margin=((ui.margin * 1.5) , 0) , qss=style.button_modern)
        flex_button(self , "?" , ((82 - (ui.margin / 4) , 90 - ui.margin / 4) , (18 , 10)) , self.func , "Help" , margin=(ui.margin / 2 , 0) ,qss=style.button_modern)
        self.show()

    def func(self) :
        print("function called!")

    def search(self) :
        print("search")

class MorePage(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.layout  = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
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
        """.format(font=ui.font, fontsize=str(ui.fontsize), border=style.colors.win_border[0]))

        #header
        flex_button(self, "<back", ((0,0),(25,12)),self.back, qss=style.button_modern, margin=(ui.margin/2,ui.margin/2))
        button(self , "X" , ((ui.winx - (ui.quitbuttonsize + ui.margin / 2) - 14 , (ui.margin / 2) + 2) , (ui.quitbuttonsize + 12 , ui.quitbuttonsize)) , quit , qss=style.button_close)

        #main
        flex_button(self , "OSR on GitHub" , ((20,20),(60,25)) , lambda self: webbrowser.open("www.github.com/freeturk/osrepo") , qss=style.button_modern)
        flex_button(self , "Open Repo in\nText Editor" , ((20,40),(60,25)) , lambda self: system(f"start {shutil.copy2('osrepo.yaml', os.path.join(tempfile.gettempdir() , 'osrepo.tmp.yaml'))}") , qss=style.button_modern)

        #footer
        label(self, "made with \u2665 by \n@baris-inandi and @FreeTurk",((0,70),(100,25)),qss="border-style:none;qproperty-alignment: AlignCenter;")

        self.show()

    def back(self) :
        print("back")

class Window(QMainWindow) :
    def __init__(self):
        mainmenu = MainMenu()
        morepage = MorePage()
        self.Stack = mainmenu

def quit(): QCoreApplication.quit()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
