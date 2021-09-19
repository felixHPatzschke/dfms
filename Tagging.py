
import os
import sys

from PyQt5 import QtWidgets
from  ui import mainwindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.initialize_io_widgets()
    
    def initialize_io_widgets(self):
        # Import Tab
        self.ui.treeWidget.clear()
        for btn in [ self.ui.pushButton_3, self.ui.pushButton_4, self.ui.pushButton_5 ]:
            btn.setEnabled(False)
        
        # Alignment Tab
        # nothing to do here, example values are already reasonable
        
        # Type and Corrections Tab
        self.ui.listWidget.clear()
        # example values in the input fields for particle info are already resonable.
        
        # Export Tab
        # nothing to do here, example values are already reasonable

# ENTRY POINT
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
