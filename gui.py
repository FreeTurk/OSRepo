from tkinter import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys

app = QApplication([])

def rgb(r,g,b):
    return "rgb({},{},{})".format(r,g,b), (r,g,b)

class ui :
    winx , winy = 300 , 350
    margin = 16
    font, fontsize = "Trebuchet MS", 14
    class style:

        # colors
        class colors:
            background =        rgb(28,     28,     32)
            text =              rgb(190 ,   190 ,   190)
            box =               rgb(61 ,    64 ,    82)
            border =            rgb(10 ,    10 ,    10)
            accent =            rgb(42 ,    155 ,   250)

        # stylesheets
        button_modern="""
            QPushButton{
                border-top-right-radius:6px;
                background:rgba(25,25,25,1);
                border-radius: 0;
                border-style: none;}
            QPushButton:hover{
                background:rgba(200,200,255,.2);}
            QPushButton:hover:!pressed{
                border: 2px solid rgb(42 , 155 , 250)
                background:rgba(0,0,0,.1);}
        """
        button_modern_bordered="""
            QPushButton{
                border-width: 1px; border-style: solid; border-color: rgb(20,20,23);
                border-bottom-right-radius: 10px; border-bottom-left-radius: 2px; border-top-right-radius: 10px; border-top-left-radius: 2px;
                background:rgba(25,25,25,1);}
            QPushButton:hover{
                border-width: 1px; border-style: solid; border-color: rgb(42 , 155 , 250);
                border-bottom-right-radius: 10px; border-bottom-left-radius: 2px; border-top-right-radius: 10px; border-top-left-radius: 2px;
                background:rgba(200,200,255,.2);}
            QPushButton:hover:!pressed{
                border-width: 1px; border-style: solid; border-color: rgb(20,20,23);
                border-bottom-right-radius: 10px; border-bottom-left-radius: 2px; border-top-right-radius: 10px; border-top-left-radius: 2px;
                background:rgba(200,200,255,.2);}
        """
        button_close="""
            QPushButton{
                background:rgba(0,0,0,0.33);
                border-radius: 1px;
                border-style: none;}
            QPushButton:hover{
                background:rgba(232,17,35,0.33);}
            QPushButton:hover:!pressed{
                background:rgba(232,17,35,1);}
        """
def qssvars():
    members = [attr for attr in dir(ui.style.colors) if not callable(getattr(ui.style.colors , attr)) and not attr.startswith("__")]
    print(members)
qssvars()
def winpos(dispx , dispy , winx=ui.winx , winy=ui.winy) :
    if winx % 2 != 0 : winx += 1
    if winy % 2 != 0 : winy += 1
    return int((dispx / 2) - (winx / 2)) , int((dispy / 2) - (winy / 2))

def flex_button(item , content="Button" , geometry=((0 , 0) , (20 , 20)) , onclick=None , tooltip=None , margin=(ui.margin, ui.margin), css=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    marginx,marginy = margin
    posxpercent , posypercent =     int((posx * ui.winx) / 100) + marginx ,             int((posy * ui.winy) / 100) + marginy
    sizexpercent , sizeypercent =   int((sizex * ui.winx) / 100) - (marginx * 2) ,      int((sizey * ui.winy) / 100) - (marginy * 2)
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

def searchbar(item , content="search" , geometry=((0 , 0) , (20 , 20)) ,  margin=(ui.margin, ui.margin), css=None) :
    pos , size = geometry
    sizex , sizey = size
    posx , posy = pos
    marginx,marginy = margin
    posxpercent , posypercent =     int((posx * ui.winx) / 100) + marginx ,             int((posy * ui.winy) / 100) + marginy
    sizexpercent , sizeypercent =   int((sizex * ui.winx) / 100) - (marginx * 2) ,      int((sizey * ui.winy) / 100) - (marginy * 2)
    inputobject = QLineEdit(item)
    inputobject.setPlaceholderText(content)
    inputobject.setGeometry(posxpercent , posypercent , sizexpercent , sizeypercent)
    if css!=None: inputobject.setStyleSheet(css)

# Dark Mode
style = ui.style
app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window ,              QColor(*style.colors.background[1]))
palette.setColor(QPalette.WindowText ,          QColor(*style.colors.text[1]))
palette.setColor(QPalette.Base ,                QColor(25 , 25 , 25))
palette.setColor(QPalette.AlternateBase ,       QColor(53 , 53 , 53))
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
root = Tk()


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
        quitsize = 32
        button(self, "X", ( (ui.winx-(quitsize+ui.margin/2)-10 , ui.margin/2) , (quitsize+10 , quitsize)), quit, css=style.button_close)

        # search bar
        searchbar(self, " search",  ((0,0),  (74,14)),    margin=(10,10))
        flex_button(self, ">",      ((68,0), (16,14)),   self.search,css=style.button_modern_bordered, margin=(10,10))

        # buttons
        # main buttons
        flex_button(self , "All OSes" , ((0+(ui.margin/8) ,  56) ,                 (50 , 30)) , self.func ,                                      css = style.button_modern)
        flex_button(self , "Download" , ((50-(ui.margin/8) , 56) ,                 (50 , 30)) , self.func ,                                      css = style.button_modern)

        # footer
        flex_button(self , "More..." ,  ((0 ,  90-ui.margin/4) ,                   (88 , 10)) , self.func , margin=((ui.margin*1.5), 0),         css = style.button_modern)
        flex_button(self , "?" ,        ((88-(ui.margin/4),90-ui.margin/4) ,       (12 , 10)) , self.func , "Help" , margin=(ui.margin/2, 0),    css = style.button_modern)
        self.show()

        self.textbox = QLineEdit()
        self.textbox2 = QLineEdit()

        txt1 = QLabel("case indes" , self)
        txt1.setAlignment(Qt.AlignCenter)
        central_widget = QWidget()
        mytext = QFormLayout(central_widget)
        mytext.addRow(txt1 , self.textbox)  # not showing in Aligned position
        mytext.addRow("Case type" , self.textbox2)  # not working

        # Create a button in the window
        self.button = QPushButton('Show text')
        mytext.addRow(self.button)
        # connect button to function on_click
        self.button.clicked.connect(self.func)

    def func(self) :
        print("function called!")

    def search(self):
        print("search")

    def quit(self):
        sys.exit()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
