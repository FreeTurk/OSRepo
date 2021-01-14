from tkinter import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette , QColor
from PyQt5.QtWidgets import *

app = QApplication([])

class ui :
    winx , winy = 300 , 350
    margin = 8
    font, fontsize = "Trebuchet MS", 14
    class style:
        # colors
        background = 20 , 20 , 24
        text = 190 , 190 , 190
        button = 61 , 64 , 82
        border = 10 , 10 , 10
        # stylesheets
        button_modern="""
            QPushButton{
               background:rgba(0,0,0,.33);
               border-radius: 0;
               border: none;
            }
            QPushButton:hover{
              background:rgba(200,200,255,.1);
            }
            QPushButton:hover:!pressed{
               
                background:rgba(0,0,0,.1);
            }
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
    if css!=None: buttonobject.setStyleSheet(css)
    if tooltip != None : buttonobject.setToolTip(tooltip)
    buttonobject.setGeometry(posxpercent , posypercent , sizexpercent , sizeypercent)
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


class Window(QMainWindow) :

    def __init__(self):
        super(Window, self).__init__()
        self.layout  = QVBoxLayout()
        # self.layout.addWidget(MyBar(self))
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


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
