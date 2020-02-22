import sys,os,time
from PyQt5.QtWidgets import QFileDialog, QApplication, QFontDialog,QGraphicsScene,QGraphicsPixmapItem , QInputDialog
from PyQt5.QtWidgets import QFileSystemModel
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import QPrintDialog,QPrinter,QPrintPreviewDialog
from Gui import *
from pathlib import Path


opened_file = ""
opened_fille = ""
toggle_statusbar = True
word_Wrap = False
modify = False


        

class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionNew.triggered.connect(self.new)
        self.ui.actionOpen.triggered.connect(self.open)
        self.ui.actionSave.triggered.connect(self.save)
        self.ui.textEdit.cursorPositionChanged.connect(self.update_status)
        self.ui.textEdit.document().modificationChanged.connect(self.mody)
        self.ui.actionSave_As.triggered.connect(self.save_as)
        self.ui.actionStatusbar.triggered.connect(self.ctr_statusbar)
        self.ui.actionPrint.triggered.connect(self.PageView)
        self.ui.actionPrint_2.triggered.connect(self.Print)
        self.ui.actionExit.triggered.connect(self.exit_on)
        self.ui.actionUndo.triggered.connect(self.Undo)
        self.ui.actionCut.triggered.connect(self.Cut)
        self.ui.actionCopy.triggered.connect(self.Copy)
        self.ui.actionPaste.triggered.connect(self.Paste)
        self.ui.actionDelete.triggered.connect(self.DeleteAll)
        self.ui.actionWordwrap.triggered.connect(self.ctrl_word_wrap)
        self.ui.actionGo_To.triggered.connect(self.go_to)
        self.ui.actionFont.triggered.connect(self.font_)
        self.ui.actionSelect_All.triggered.connect(self.select_all)
        self.ui.actionTime_Date.triggered.connect(self.date_time)
        self.ui.actionHelp.triggered.connect(self.help_)
        self.ui.actionAbout_Unikx.triggered.connect(self.about_)
        self.ui.actionReplace.triggered.connect(self.replaceThis)
        self.pre_()
        self.ui.textEdit.setFocus()
# --------------------------------------------------------------- set Completer -------------------------------------------------------------
       
        # self.completer = QCompleter(self)
        # # self.completer.setModel(self.modelFromFile(self.root + '/resources/wordlist.txt'))
        # self.completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        # self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        # self.completer.setWrapAround(False)
        # self.completer.setCompletionRole(Qt.EditRole)
        # self.ui.textEdit.setCompleter(self.completer)
# --------------------------------------------------------------- Window Show -------------------------------------------------------------

        self.show()
# --------------------------------------------------------------- Get Line Number-------------------------------------------------------------

    def getLineNumber(self):
        self.editor.moveCursor(self.cursor.StartOfLine)
        linenumber = self.editor.textCursor().blockNumber() + 1
        return linenumber
# --------------------------------------------------------------- Go to -------------------------------------------------------------
       
    def gotoLine(self):
        ln = int(self.gotofield.text())
        linecursor = QTextCursor(self.editor.document().findBlockByLineNumber(ln-1))
        self.editor.moveCursor(QTextCursor.End)
        self.editor.setTextCursor(linecursor)
# --------------------------------------------------------------- Get Selected text -------------------------------------------------------------

    def textUnderCursor(self):
        tc = self.ui.textEdit.textCursor()
        tc.select(QTextCursor.WordUnderCursor)

        return tc.selectedText()        
# --------------------------------------------------------------- replace -------------------------------------------------------------
    def replaceThis(self):
        global modify
        rtext = self.ui.textEdit.textCursor().selectedText()
        text = QInputDialog.getText(self, "replace with","replace '" + rtext + "' with:", QLineEdit.Normal, "")
        oldtext = self.ui.textEdit.document().toPlainText()
        if not (text[0] == ""):
            newtext = oldtext.replace(rtext, text[0])
            self.ui.textEdit.setPlainText(newtext)
            modify = True
# --------------------------------------------------------------- About -------------------------------------------------------------
            
            
    def about_(self):
        pass
       
        
        
        
# --------------------------------------------------------------- Help -------------------------------------------------------------
        
    def help_(self):
        pass
        
# --------------------------------------------------------------- Date Time -------------------------------------------------------------
    
    def date_time(self):
        t = time.localtime()
        self.ui.textEdit.insertPlainText(time.asctime(t))

# --------------------------------------------------------------- Font -------------------------------------------------------------
        
    def font_(self):
        font,ok = QFontDialog.getFont()
        if ok:
            self.ui.textEdit.setFont(font)
# ---------------------------------------------------------------  go To -------------------------------------------------------------
 
    def go_to(self):
        text , ok = QInputDialog.getText(self,"Go To","line Number :")
        if ok:
            self.ui.textEdit.moveCursor(int(text))
        else:
            print("Enter Valid Line Number")

# --------------------------------------------------------------- Toggle Word Wrap -------------------------------------------------------------
    def ctrl_word_wrap(self):
        global word_Wrap
        if word_Wrap == False:
            self.ui.textEdit.setLineWrapMode(QtWidgets.QTextEdit.WidgetWidth)
            word_Wrap = True
        else:
            self.ui.textEdit.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
            word_Wrap = False
            
# --------------------------------------------------------------- Small Functions -------------------------------------------------------------        
    def select_all(self):
        self.ui.textEdit.selectAll()
        
    def Undo(self):
        self.ui.textEdit.undo()
 
    # def Redo(self):
    #     self.ui.textEdit.redo()
 
    def Cut(self):
        self.ui.textEdit.cut()
 
    def Copy(self):
        self.ui.textEdit.copy()
 
    def Paste(self):
        self.ui.textEdit.paste() 
    
    def DeleteAll(self):
        self.ui.textEdit.clear()
# --------------------------------------------------------------- Print -------------------------------------------------------------               
    def PaintPageView(self, printer):
        self.ui.textEdit.print_(printer)
        
    def PageView(self):
        preview = QPrintPreviewDialog()
        preview.paintRequested.connect(self.PaintPageView)
        preview.exec_()
 
    def Print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.ui.textEdit.document().print_(dialog.printer())
# --------------------------------------------------------------- Update Statusbar -------------------------------------------------------------                
    def update_status(self):
        line = self.ui.textEdit.textCursor().blockNumber()
        col = self.ui.textEdit.textCursor().columnNumber()
        word=len(self.ui.textEdit.toPlainText().split())
        character=(self.ui.textEdit.toPlainText().replace(" ",""))
        try:
            character.replace("/t","")
        except:
            pass
        linecol = ("Line: "+str(line)+" | "+"Column: "+str(col) +" | "+"Word: "+str(word)+" | "+"Character: "+str(len(character)))
        self.ui.statusBar.showMessage(linecol)        
# --------------------------------------------------------------- Toggle Statusbar -------------------------------------------------------------
    def ctr_statusbar(self):
        global toggle_statusbar
        
        if toggle_statusbar == True:
            self.ui.statusBar.hide()
            toggle_statusbar = False
        else:
            self.ui.statusBar.show()
            toggle_statusbar = True
            
# --------------------------------------------------------------- Imp -------------------------------------------------------------            
    def pre_(self):
        self.setWindowTitle("Untitled - Notepad")
            
    def mody(self):
        global modify
        modify = True
        return modify
    
# --------------------------------------------------------------- Save -------------------------------------------------------------    
    def save(self):
        global opened_file , modify
        
        
        Editor_content = self.ui.textEdit.toPlainText()
        if opened_file != "" :
            file = open(opened_file,"w+")
            file.write(Editor_content)
            file.close()
        else:
            self.save_as()
        
    def save_as(self):
        Editor_content = self.ui.textEdit.toPlainText()
        fname = QFileDialog.getSaveFileName(self,"Save File","","All Files (*);;Python Files (*.py)")
        if fname[0]:
            file = open(fname[0],mode="w+")
            file.write(Editor_content)
            file.close()
        else:
            pass
           
# --------------------------------------------------------------- Open -------------------------------------------------------------      
    
    def open(self):
        global opened_file , modify
        
        Editor_content = self.ui.textEdit.toPlainText()
        if modify == True:
            if opened_file != "":
                f_name = os.path.basename(opened_file)
                msg = QMessageBox.question(self,"Notepad",f"Do you want to save changes {f_name}",QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel)
                if msg == QMessageBox.Save:
                    self.save()
                    fname = QFileDialog.getOpenFileName(self,"Open File","","All Files (*);;Python Files (*.py)") 
                    if fname[0]:
                        file = open(fname[0],mode="r+")
                        content_file = file.read()
                        self.ui.textEdit.clear()
                        self.ui.textEdit.setText(content_file)
                        file.close()  
                        f_name = os.path.basename(fname[0])
                        file_n = f_name[0:f_name.rfind(".")]
                        self.setWindowTitle(f"{file_n} - Notepad")
                        modify =False
                        opened_file = fname[0]
                        return modify , opened_file
                    else:
                        pass
                    
                elif msg == QMessageBox.Discard:
                    fname = QFileDialog.getOpenFileName(self,"Open File","","All Files (*);;Python Files (*.py)") 
                    if fname[0]:
                        file = open(fname[0],mode="r+")
                        content_file = file.read()
                        self.ui.textEdit.clear()
                        self.ui.textEdit.setText(content_file)
                        file.close()  
                        f_name = os.path.basename(fname[0])
                        file_n = f_name[0:f_name.rfind(".")]
                        self.setWindowTitle(f"{file_n} - Notepad")
                        modify =False
                        opened_file = fname[0]
                        return modify , opened_file
                    else:
                        pass
                else:
                    pass
            else:
                msg = QMessageBox.question(self,"Notepad",f"Do you want to save changes",QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel)
                if msg == QMessageBox.Save:
                    self.save_as()
                    fname = QFileDialog.getOpenFileName(self,"Open File","","All Files (*);;Python Files (*.py)") 
                    if fname[0]:
                        file = open(fname[0],mode="r+")
                        content_file = file.read()
                        self.ui.textEdit.clear()
                        self.ui.textEdit.setText(content_file)
                        file.close()  
                        f_name = os.path.basename(fname[0])
                        file_n = f_name[0:f_name.rfind(".")]
                        self.setWindowTitle(f"{file_n} - Notepad")
                        modify =False
                        opened_file = fname[0]
                        return modify , opened_file
                    else:
                        pass
                    
                elif msg == QMessageBox.Discard:
                    fname = QFileDialog.getOpenFileName(self,"Open File","","All Files (*);;Python Files (*.py)") 
                    if fname[0]:
                        file = open(fname[0],mode="r+")
                        content_file = file.read()
                        self.ui.textEdit.clear()
                        self.ui.textEdit.setText(content_file)
                        file.close()  
                        f_name = os.path.basename(fname[0])
                        file_n = f_name[0:f_name.rfind(".")]
                        self.setWindowTitle(f"{file_n} - Notepad")
                        modify =False
                        opened_file = fname[0]
                        return modify , opened_file
                    else:
                        pass
                else:
                    pass   
                 
        elif modify ==False:
            fname = QFileDialog.getOpenFileName(self,"Open File","","All Files (*);;Python Files (*.py)") 
            
            if fname[0]:
                file = open(fname[0],mode="r+")
                content_file = file.read()
                self.ui.textEdit.clear()
                self.ui.textEdit.setText(content_file)
                file.close()  
                f_name = os.path.basename(fname[0])
                file_n = f_name[0:f_name.rfind(".")]
                self.setWindowTitle(f"{file_n} - Notepad")
                modify =False
                opened_file = fname[0]
        
                return modify , opened_file
            else:
                pass
        else:
            pass

# --------------------------------------------------------------- New -------------------------------------------------------------
    def new(self):
        global opened_file , modify
        
        Editor_content = self.ui.textEdit.toPlainText()
        if modify == True:
            if opened_file != "":
                f_name = os.path.basename(opened_file)
                msg = QMessageBox.question(self,"Notepad",f"Do you want to save changes {f_name}",QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel)
                if msg == QMessageBox.Save:
                    self.save()
                    self.ui.textEdit.clear()
                    self.setWindowTitle("Untitled - Notepad ")
                    opened_file = ""
                    modify = False
                    
                elif msg == QMessageBox.Discard:
                    self.ui.textEdit.clear()
                    self.setWindowTitle("Untitled - Notepad ")
                    opened_file = ""
                    modify = False
                    
                else:
                    pass
            else:
                msg = QMessageBox.question(self,"Notepad",f"Do you want to save changes",QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel)
                if msg == QMessageBox.Save:
                    self.save_as()
                    self.ui.textEdit.clear()
                    self.setWindowTitle("Untitled - Notepad ")
                    opened_file = ""
                    modify = False
                    
                elif msg == QMessageBox.Discard:
                    self.ui.textEdit.clear()
                    self.setWindowTitle("Untitled - Notepad ")
                    opened_file = ""
                    modify = False
                else:
                    pass   
                 
        elif modify ==False:
            self.ui.textEdit.clear()
            self.setWindowTitle("Untitled - Notepad ")
            opened_file = ""
            modify = False
            
        else:
            pass               
# --------------------------------------------------------------- Exit -------------------------------------------------------------         
    def exit_on(self):
        global opened_file , modify
        
        Editor_content = self.ui.textEdit.toPlainText()
        if modify == True:
            if opened_file != "":
                f_name = os.path.basename(opened_file)
                msg = QMessageBox.question(self,"Notepad",f"Do you want to save changes {f_name}",QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel)
                if msg == QMessageBox.Save:
                    self.save()
                    sys.exit(app.exec_())
                    
                elif msg == QMessageBox.Discard:
                    sys.exit(app.exec_())
                    
                else:
                    pass
            else:
                msg = QMessageBox.question(self,"Notepad",f"Do you want to save changes",QMessageBox.Save|QMessageBox.Discard|QMessageBox.Cancel)
                if msg == QMessageBox.Save:
                    self.save_as()
                    sys.exit(app.exec_())
                    
                elif msg == QMessageBox.Discard:
                    sys.exit(app.exec_())
                else:
                    sys.exit(app.exec_())  
                 
        elif modify ==False:
            sys.exit(app.exec_())
            
        else:
            sys.exit(app.exec_())               
# --------------------------------------------------------------- Exit -------------------------------------------------------------
        
if __name__=="__main__":
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())