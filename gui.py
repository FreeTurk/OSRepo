from tkinter import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

app = QApplication([])

class ui :
    winx , winy = 300 , 350
    margin = 8
    font, fontsize = "Trebuchet MS", 14
    class style:
        # colors
        background =    28, 28, 32
        text =          190 , 190 , 190
        button =        61 , 64 , 82
        border =        10 , 10 , 10
        # stylesheets
        button_modern="""
            QPushButton{
                 background:rgba(0,0,0,.33);
                 border-radius: 0;
                 border-style: none;}
            QPushButton:hover{
                background:rgba(200,200,255,.2);}
            QPushButton:hover:!pressed{
                background:rgba(0,0,0,.1);}
        """
        button_close="""
            QPushButton{
                background:rgba(255,0,0,.5);
                border-radius: 1px;
                border-style: none;}
            QPushButton:hover{
                background:rgba(255,0,0,.3);}
            QPushButton:hover:!pressed{
                background:rgba(255,0,0,.4);}
        """

def winpos(dispx , dispy , winx=ui.winx , winy=ui.winy) :
    if winx % 2 != 0 : winx += 1
    if winy % 2 != 0 : winy += 1
    return int((dispx / 2) - (winx / 2)) , int((dispy / 2) - (winy / 2))

def flex_button(item , content="Button" , geometry=((0 , 0) , (20 , 20)) , onclick=None , tooltip=None , margin=(ui.margin, ui.margin), css=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    marginx,marginy = margin
    posxpercent , posypercent = int((posx * ui.winx) / 100) + marginx , int((posy * ui.winy) / 100) + marginy
    sizexpercent , sizeypercent = int((sizex * ui.winx) / 100) - (marginx * 2) , int((sizey * ui.winy) / 100) - (marginy * 2)
    buttonobject = QPushButton(content , item)
    buttonobject.setGeometry(posxpercent , posypercent , sizexpercent , sizeypercent)
    if css!=None: buttonobject.setStyleSheet(css)
    if tooltip != None : buttonobject.setToolTip(tooltip)
    if onclick != None : buttonobject.clicked.connect(onclick)

def button(item , content="Button" , geometry=((0,0),(20,20)) , onclick=None , tooltip=None , css=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    buttonobject = QPushButton(content , item)
    buttonobject.setGeometry(posx , posy , sizex , sizey)
    if css!=None: buttonobject.setStyleSheet(css)
    if tooltip != None : buttonobject.setToolTip(tooltip)
    if onclick != None : buttonobject.clicked.connect(onclick)

# Dark Mode

style = ui.style
app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window ,           QColor(*style.background))
palette.setColor(QPalette.WindowText ,       QColor(*style.text))
palette.setColor(QPalette.Base ,             QColor(25 , 25 , 25))
palette.setColor(QPalette.AlternateBase ,    QColor(53 , 53 , 53))
palette.setColor(QPalette.ToolTipBase ,      Qt.white)
palette.setColor(QPalette.ToolTipText ,      Qt.white)
palette.setColor(QPalette.Text ,             Qt.white)
palette.setColor(QPalette.Button ,           QColor(*style.button))
palette.setColor(QPalette.ButtonText ,       Qt.white)
palette.setColor(QPalette.BrightText ,       Qt.yellow)
palette.setColor(QPalette.Link ,             QColor(42 , 130 , 218))
palette.setColor(QPalette.Highlight ,        QColor(42 , 130 , 218))
palette.setColor(QPalette.HighlightedText ,  Qt.black)
app.setPalette(palette)
app.setApplicationName("OSRepo")
root = Tk()

#
BUTTON_HEIGHT = 30
# button width
BUTTON_WIDTH = 30
# title bar height
TITLE_HEIGHT = 30

class Window(QMainWindow) :

    def __init__(self):
        super(Window, self).__init__()
        self.layout  = QVBoxLayout()
        #add titlebar
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addStretch(-1)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.setWindowTitle("OSRepo")
        self.setGeometry(*winpos(root.winfo_screenwidth() , root.winfo_screenheight()) , ui.winx , ui.winy)
        self.setFixedSize(ui.winx , ui.winy)
        self.setStyleSheet(
        """
        font-family: {};
        font-size: {}px;
        """.format(ui.font, str(ui.fontsize)))

        #quit button
        button(self, " X ", ( (ui.winx-(24) , 4) , (20 , 20)), quit, css=style.button_close)

        # add search bar here

        # buttons
        # main buttons
        flex_button(self , "All OSes" , ((0+(ui.margin/8) ,  50) ,                 (50 , 25)) , self.func ,                                      css = style.button_modern)
        flex_button(self , "Download" , ((50-(ui.margin/8) , 50) ,                 (50 , 25)) , self.func ,                                      css = style.button_modern)

        # footer
        flex_button(self , "More..." ,  ((0 ,  90-ui.margin/4) ,                   (88 , 10)) , self.func , margin=((ui.margin*1.5), 0),         css = style.button_modern)
        flex_button(self , "?" ,        ((88-(ui.margin/4) , 90-ui.margin/4) ,     (12 , 10)) , self.func , "Help" , margin=(ui.margin/2, 0),    css = style.button_modern)
        self.show()

    def func(self) :
        print("function called!")

    def search(self , param) :
        print("search function called: " , param)

    def quit(self):
        sys.exit()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
