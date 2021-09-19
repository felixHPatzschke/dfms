
import os
import sys

from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTreeWidgetItem

from ui import mainwindow
from util import tdms



video_descriptors = []



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pushButton.clicked.connect(self.select_input_files)
        self.input_files_selected = False
        
        self.initialize_io_widgets()
    
    def initialize_io_widgets(self):
        # Import Tab
        self.ui.treeWidget.clear()
        self.ui.treeWidget.setColumnWidth(0,172)
        self.ui.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        for btn in [ self.ui.pushButton_3, self.ui.pushButton_4, self.ui.pushButton_5 ]:
            btn.setEnabled(self.input_files_selected)
        
        # Alignment Tab
        # nothing to do here, example values are already reasonable
        
        # Type and Corrections Tab
        self.ui.listWidget.clear()
        # example values in the input fields for particle info are already resonable.
        
        # Export Tab
        # nothing to do here, example values are already reasonable
    
    def select_input_files(self):
        global video_descriptors
        
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;TDMS Files (*.tdms)", options=options)
        if files:
            #video_descriptors = []
            video_descriptors = tdms.files_to_descriptors(files)
            self.show_video_descriptors()
            self.input_files_selected = True
            for btn in [ self.ui.pushButton_3, self.ui.pushButton_4, self.ui.pushButton_5 ]:
                btn.setEnabled(self.input_files_selected)
    
    def show_video_descriptors(self):
        global video_descriptors
        
        items = []
        vidx = 0
        for dsc in video_descriptors:
            top_level_entries = [ "Video {i}".format(i=vidx), "" ]
            children = []
            if dsc.data_format == tdms.Format.VIDEO:
                #top_level_entries.append( "(AIO)" )
                children.append( QTreeWidgetItem(["Data & Metadata", dsc.data_file]) )
            elif dsc.data_format == tdms.Format.MODULE:
                #top_level_entries.append( "(ROI + Metadata)" )
                children.append( QTreeWidgetItem(["Data", dsc.data_file]) )
                children.append( QTreeWidgetItem(["Metadata", dsc.metadata_file]) )
            
            item = QTreeWidgetItem( top_level_entries )
            for child in children:
                child.setFlags(QtCore.Qt.ItemIsEnabled)
                item.addChild(child)
            #item.setExpanded(True)
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled)
            items.append(item)
            vidx += 1
        self.ui.treeWidget.clear()
        self.ui.treeWidget.insertTopLevelItems(0, items)
        for i in items:
            self.ui.treeWidget.expandItem(i)


# ENTRY POINT
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
