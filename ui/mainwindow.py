# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xml/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1481, 1013)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.widget_3 = QtWidgets.QWidget(self.widget_2)
        self.widget_3.setObjectName("widget_3")
        self.gridLayout = QtWidgets.QGridLayout(self.widget_3)
        self.gridLayout.setContentsMargins(0, 0, -1, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.plotWidget = QtWidgets.QWidget(self.widget_3)
        self.plotWidget.setMinimumSize(QtCore.QSize(900, 900))
        self.plotWidget.setObjectName("plotWidget")
        self.gridLayout.addWidget(self.plotWidget, 1, 1, 1, 1)
        self.horizontalScrollBar = QtWidgets.QScrollBar(self.widget_3)
        self.horizontalScrollBar.setMinimum(0)
        self.horizontalScrollBar.setMaximum(1023)
        self.horizontalScrollBar.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar.setInvertedAppearance(False)
        self.horizontalScrollBar.setObjectName("horizontalScrollBar")
        self.gridLayout.addWidget(self.horizontalScrollBar, 0, 1, 1, 1)
        self.verticalScrollBar = QtWidgets.QScrollBar(self.widget_3)
        self.verticalScrollBar.setMinimum(0)
        self.verticalScrollBar.setMaximum(1023)
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.gridLayout.addWidget(self.verticalScrollBar, 1, 0, 1, 1)
        self.widget_11 = QtWidgets.QWidget(self.widget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy)
        self.widget_11.setObjectName("widget_11")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.widget_11)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.comboBox_2 = QtWidgets.QComboBox(self.widget_11)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.horizontalLayout_10.addWidget(self.comboBox_2)
        self.horizontalSlider = QtWidgets.QSlider(self.widget_11)
        self.horizontalSlider.setMinimum(1)
        self.horizontalSlider.setMaximum(250)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.horizontalLayout_10.addWidget(self.horizontalSlider)
        self.label_4 = QtWidgets.QLabel(self.widget_11)
        self.label_4.setMinimumSize(QtCore.QSize(64, 0))
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_10.addWidget(self.label_4)
        self.gridLayout.addWidget(self.widget_11, 2, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.widget_3)
        self.line_2 = QtWidgets.QFrame(self.widget_2)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_2.addWidget(self.line_2)
        self.tabWidget = QtWidgets.QTabWidget(self.widget_2)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.widget_5 = QtWidgets.QWidget(self.tab)
        self.widget_5.setObjectName("widget_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget_5)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton = QtWidgets.QPushButton(self.widget_5)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_4.addWidget(self.pushButton)
        spacerItem = QtWidgets.QSpacerItem(410, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout_7.addWidget(self.widget_5)
        self.treeWidget = QtWidgets.QTreeWidget(self.tab)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsDropEnabled|QtCore.Qt.ItemIsEnabled)
        self.treeWidget.header().setVisible(False)
        self.treeWidget.header().setCascadingSectionResizes(False)
        self.verticalLayout_7.addWidget(self.treeWidget)
        self.widget_8 = QtWidgets.QWidget(self.tab)
        self.widget_8.setObjectName("widget_8")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.widget_8)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_8)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_5.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_8)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_5.addWidget(self.pushButton_4)
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_8)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_5.addWidget(self.pushButton_5)
        self.pushButton_6 = QtWidgets.QPushButton(self.widget_8)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_5.addWidget(self.pushButton_6)
        self.verticalLayout_7.addWidget(self.widget_8)
        self.progressBar = QtWidgets.QProgressBar(self.tab)
        self.progressBar.setEnabled(True)
        self.progressBar.setProperty("value", 50)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_7.addWidget(self.progressBar)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.widget = QtWidgets.QWidget(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBox_6 = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setObjectName("groupBox_6")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_6)
        self.gridLayout_3.setContentsMargins(32, -1, -1, -1)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(self.groupBox_6)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 1, 3, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setObjectName("label_7")
        self.gridLayout_3.addWidget(self.label_7, 3, 1, 1, 1)
        self.doubleSpinBox_y0 = QtWidgets.QDoubleSpinBox(self.groupBox_6)
        self.doubleSpinBox_y0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_y0.setDecimals(1)
        self.doubleSpinBox_y0.setMaximum(1023.0)
        self.doubleSpinBox_y0.setSingleStep(1.0)
        self.doubleSpinBox_y0.setProperty("value", 0.0)
        self.doubleSpinBox_y0.setObjectName("doubleSpinBox_y0")
        self.gridLayout_3.addWidget(self.doubleSpinBox_y0, 3, 2, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox_6)
        self.label_8.setObjectName("label_8")
        self.gridLayout_3.addWidget(self.label_8, 3, 3, 1, 1)
        self.doubleSpinBox_x0 = QtWidgets.QDoubleSpinBox(self.groupBox_6)
        self.doubleSpinBox_x0.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_x0.setDecimals(1)
        self.doubleSpinBox_x0.setMaximum(1023.0)
        self.doubleSpinBox_x0.setSingleStep(1.0)
        self.doubleSpinBox_x0.setProperty("value", 0.0)
        self.doubleSpinBox_x0.setObjectName("doubleSpinBox_x0")
        self.gridLayout_3.addWidget(self.doubleSpinBox_x0, 1, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.gridLayout_3.addWidget(self.label_5, 1, 1, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_6)
        self.groupBox_9 = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_9.sizePolicy().hasHeightForWidth())
        self.groupBox_9.setSizePolicy(sizePolicy)
        self.groupBox_9.setObjectName("groupBox_9")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBox_9)
        self.gridLayout_5.setContentsMargins(8, -1, 8, -1)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.doubleSpinBox_d = QtWidgets.QDoubleSpinBox(self.groupBox_9)
        self.doubleSpinBox_d.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_d.setDecimals(0)
        self.doubleSpinBox_d.setMinimum(2.0)
        self.doubleSpinBox_d.setMaximum(1024.0)
        self.doubleSpinBox_d.setSingleStep(2.0)
        self.doubleSpinBox_d.setProperty("value", 20.0)
        self.doubleSpinBox_d.setObjectName("doubleSpinBox_d")
        self.gridLayout_5.addWidget(self.doubleSpinBox_d, 1, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(self.groupBox_9)
        self.label_24.setObjectName("label_24")
        self.gridLayout_5.addWidget(self.label_24, 1, 2, 1, 1)
        self.label_23 = QtWidgets.QLabel(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_23.sizePolicy().hasHeightForWidth())
        self.label_23.setSizePolicy(sizePolicy)
        self.label_23.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_23.setObjectName("label_23")
        self.gridLayout_5.addWidget(self.label_23, 1, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_5.addWidget(self.label_10, 0, 0, 1, 1)
        self.doubleSpinBox_alpha = QtWidgets.QDoubleSpinBox(self.groupBox_9)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.doubleSpinBox_alpha.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox_alpha.setSizePolicy(sizePolicy)
        self.doubleSpinBox_alpha.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_alpha.setDecimals(1)
        self.doubleSpinBox_alpha.setMaximum(360.0)
        self.doubleSpinBox_alpha.setProperty("value", 180.0)
        self.doubleSpinBox_alpha.setObjectName("doubleSpinBox_alpha")
        self.gridLayout_5.addWidget(self.doubleSpinBox_alpha, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox_9)
        self.label_11.setObjectName("label_11")
        self.gridLayout_5.addWidget(self.label_11, 0, 2, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox_9)
        self.verticalLayout_2.addWidget(self.widget)
        self.groupBox_11 = QtWidgets.QGroupBox(self.tab_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_11.sizePolicy().hasHeightForWidth())
        self.groupBox_11.setSizePolicy(sizePolicy)
        self.groupBox_11.setObjectName("groupBox_11")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_11)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.comboBox_preview = QtWidgets.QComboBox(self.groupBox_11)
        self.comboBox_preview.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_preview.sizePolicy().hasHeightForWidth())
        self.comboBox_preview.setSizePolicy(sizePolicy)
        self.comboBox_preview.setObjectName("comboBox_preview")
        self.comboBox_preview.addItem("")
        self.comboBox_preview.addItem("")
        self.comboBox_preview.addItem("")
        self.verticalLayout_3.addWidget(self.comboBox_preview)
        self.previewWidget = QtWidgets.QWidget(self.groupBox_11)
        self.previewWidget.setMinimumSize(QtCore.QSize(400, 200))
        self.previewWidget.setObjectName("previewWidget")
        self.verticalLayout_3.addWidget(self.previewWidget)
        self.verticalLayout_2.addWidget(self.groupBox_11)
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.widget_4 = QtWidgets.QWidget(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_4.sizePolicy().hasHeightForWidth())
        self.widget_4.setSizePolicy(sizePolicy)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox_2 = QtWidgets.QGroupBox(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_6.addWidget(self.lineEdit_3, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setObjectName("label_3")
        self.gridLayout_6.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setObjectName("label_2")
        self.gridLayout_6.addWidget(self.label_2, 4, 0, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.gridLayout_6.addWidget(self.comboBox_3, 2, 2, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout_6.addWidget(self.lineEdit_2, 4, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_6.addWidget(self.label_9, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setObjectName("label")
        self.gridLayout_6.addWidget(self.label, 1, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout_6.addWidget(self.lineEdit, 1, 2, 1, 1)
        self.horizontalLayout_3.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.widget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(200, 0))
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.listWidget = QtWidgets.QListWidget(self.groupBox_3)
        self.listWidget.setMinimumSize(QtCore.QSize(0, 256))
        self.listWidget.setSelectionRectVisible(False)
        self.listWidget.setObjectName("listWidget")
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget.addItem(item)
        item = QtWidgets.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.listWidget.addItem(item)
        self.gridLayout_7.addWidget(self.listWidget, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox_3)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_7.addWidget(self.pushButton_2, 0, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.groupBox_3)
        self.verticalLayout_6.addWidget(self.widget_4)
        self.groupBox_12 = QtWidgets.QGroupBox(self.tab_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_12.sizePolicy().hasHeightForWidth())
        self.groupBox_12.setSizePolicy(sizePolicy)
        self.groupBox_12.setObjectName("groupBox_12")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_12)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.comboBox_preview_2 = QtWidgets.QComboBox(self.groupBox_12)
        self.comboBox_preview_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_preview_2.sizePolicy().hasHeightForWidth())
        self.comboBox_preview_2.setSizePolicy(sizePolicy)
        self.comboBox_preview_2.setObjectName("comboBox_preview_2")
        self.comboBox_preview_2.addItem("")
        self.verticalLayout_5.addWidget(self.comboBox_preview_2)
        self.previewWidget_2 = QtWidgets.QWidget(self.groupBox_12)
        self.previewWidget_2.setMinimumSize(QtCore.QSize(400, 200))
        self.previewWidget_2.setObjectName("previewWidget_2")
        self.verticalLayout_5.addWidget(self.previewWidget_2)
        self.verticalLayout_6.addWidget(self.groupBox_12)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.groupBox = QtWidgets.QGroupBox(self.tab_4)
        self.groupBox.setGeometry(QtCore.QRect(90, 360, 196, 145))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.widget_6 = QtWidgets.QWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy)
        self.widget_6.setObjectName("widget_6")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.widget_6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_26 = QtWidgets.QLabel(self.widget_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_26.sizePolicy().hasHeightForWidth())
        self.label_26.setSizePolicy(sizePolicy)
        self.label_26.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_6.addWidget(self.label_26)
        self.spinBox_particleNo = QtWidgets.QSpinBox(self.widget_6)
        self.spinBox_particleNo.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_particleNo.sizePolicy().hasHeightForWidth())
        self.spinBox_particleNo.setSizePolicy(sizePolicy)
        self.spinBox_particleNo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.spinBox_particleNo.setMinimum(1)
        self.spinBox_particleNo.setMaximum(8192)
        self.spinBox_particleNo.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.spinBox_particleNo.setObjectName("spinBox_particleNo")
        self.horizontalLayout_6.addWidget(self.spinBox_particleNo)
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem1)
        self.verticalLayout_4.addWidget(self.widget_6)
        self.widget_7 = QtWidgets.QWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.widget_7.setObjectName("widget_7")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.widget_7)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.exportButton = QtWidgets.QCommandLinkButton(self.widget_7)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exportButton.sizePolicy().hasHeightForWidth())
        self.exportButton.setSizePolicy(sizePolicy)
        self.exportButton.setObjectName("exportButton")
        self.horizontalLayout_7.addWidget(self.exportButton)
        self.verticalLayout_4.addWidget(self.widget_7)
        self.tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        self.verticalLayout.addWidget(self.widget_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(3)
        self.comboBox_preview.setCurrentIndex(0)
        self.comboBox_preview_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.tabWidget, self.pushButton)
        MainWindow.setTabOrder(self.pushButton, self.treeWidget)
        MainWindow.setTabOrder(self.treeWidget, self.pushButton_3)
        MainWindow.setTabOrder(self.pushButton_3, self.pushButton_4)
        MainWindow.setTabOrder(self.pushButton_4, self.pushButton_5)
        MainWindow.setTabOrder(self.pushButton_5, self.pushButton_6)
        MainWindow.setTabOrder(self.pushButton_6, self.doubleSpinBox_x0)
        MainWindow.setTabOrder(self.doubleSpinBox_x0, self.doubleSpinBox_y0)
        MainWindow.setTabOrder(self.doubleSpinBox_y0, self.doubleSpinBox_alpha)
        MainWindow.setTabOrder(self.doubleSpinBox_alpha, self.doubleSpinBox_d)
        MainWindow.setTabOrder(self.doubleSpinBox_d, self.comboBox_preview)
        MainWindow.setTabOrder(self.comboBox_preview, self.lineEdit_3)
        MainWindow.setTabOrder(self.lineEdit_3, self.lineEdit)
        MainWindow.setTabOrder(self.lineEdit, self.comboBox_3)
        MainWindow.setTabOrder(self.comboBox_3, self.lineEdit_2)
        MainWindow.setTabOrder(self.lineEdit_2, self.pushButton_2)
        MainWindow.setTabOrder(self.pushButton_2, self.listWidget)
        MainWindow.setTabOrder(self.listWidget, self.comboBox_preview_2)
        MainWindow.setTabOrder(self.comboBox_preview_2, self.spinBox_particleNo)
        MainWindow.setTabOrder(self.spinBox_particleNo, self.exportButton)
        MainWindow.setTabOrder(self.exportButton, self.comboBox_2)
        MainWindow.setTabOrder(self.comboBox_2, self.horizontalSlider)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dark Field Spectrum Tagging"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "Frame"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "Mean"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "Maximum"))
        self.label_4.setText(_translate("MainWindow", "1 / 0"))
        self.pushButton.setText(_translate("MainWindow", "Select Files"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "Videos"))
        self.treeWidget.headerItem().setText(1, _translate("MainWindow", "Files"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Video 0"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "Data"))
        self.treeWidget.topLevelItem(0).child(0).setText(1, _translate("MainWindow", "/path/to/file 1.tdms"))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "Metadata"))
        self.treeWidget.topLevelItem(0).child(1).setText(1, _translate("MainWindow", "/path/tp/file 2.tdms"))
        self.treeWidget.topLevelItem(1).setText(0, _translate("MainWindow", "Video 1"))
        self.treeWidget.topLevelItem(1).child(0).setText(0, _translate("MainWindow", "Data & Metadata"))
        self.treeWidget.topLevelItem(1).child(0).setText(1, _translate("MainWindow", "/path/to/file 3.tdms"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton_3.setText(_translate("MainWindow", "Load First Video"))
        self.pushButton_4.setText(_translate("MainWindow", "Load Last Video"))
        self.pushButton_5.setText(_translate("MainWindow", "Load Selected Videos"))
        self.pushButton_6.setText(_translate("MainWindow", "Load All Videos"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Import"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Position"))
        self.label_6.setText(_translate("MainWindow", "px"))
        self.label_7.setText(_translate("MainWindow", "y ="))
        self.label_8.setText(_translate("MainWindow", "px"))
        self.label_5.setText(_translate("MainWindow", "x ="))
        self.groupBox_9.setTitle(_translate("MainWindow", "ROI"))
        self.label_24.setText(_translate("MainWindow", "px"))
        self.label_23.setText(_translate("MainWindow", "d ="))
        self.label_10.setText(_translate("MainWindow", "α ="))
        self.label_11.setText(_translate("MainWindow", "deg"))
        self.groupBox_11.setTitle(_translate("MainWindow", "Preview"))
        self.comboBox_preview.setItemText(0, _translate("MainWindow", "0th Order"))
        self.comboBox_preview.setItemText(1, _translate("MainWindow", "1st Order"))
        self.comboBox_preview.setItemText(2, _translate("MainWindow", "ROI Profiles"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Alignment"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Particle"))
        self.lineEdit_3.setText(_translate("MainWindow", "0.1 µm"))
        self.label_3.setText(_translate("MainWindow", "Class: "))
        self.label_2.setText(_translate("MainWindow", "Comment:"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "Particle"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "JP"))
        self.label_9.setText(_translate("MainWindow", "Size: "))
        self.label.setText(_translate("MainWindow", "Material:"))
        self.lineEdit.setText(_translate("MainWindow", "Au"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Devices"))
        __sortingEnabled = self.listWidget.isSortingEnabled()
        self.listWidget.setSortingEnabled(False)
        item = self.listWidget.item(0)
        item.setText(_translate("MainWindow", "LED"))
        item = self.listWidget.item(1)
        item.setText(_translate("MainWindow", "Halogen Lamp"))
        item = self.listWidget.item(2)
        item.setText(_translate("MainWindow", "Objective Lens"))
        item = self.listWidget.item(3)
        item.setText(_translate("MainWindow", "Tube Lens"))
        item = self.listWidget.item(4)
        item.setText(_translate("MainWindow", "Diffraction Grating"))
        item = self.listWidget.item(5)
        item.setText(_translate("MainWindow", "EMCCD"))
        self.listWidget.setSortingEnabled(__sortingEnabled)
        self.pushButton_2.setText(_translate("MainWindow", "Refresh List"))
        self.groupBox_12.setTitle(_translate("MainWindow", "Preview"))
        self.comboBox_preview_2.setItemText(0, _translate("MainWindow", "Corrected Spectrum"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Particle Type and Corrections"))
        self.groupBox.setTitle(_translate("MainWindow", "Export"))
        self.label_26.setText(_translate("MainWindow", "Particle"))
        self.exportButton.setText(_translate("MainWindow", "Export"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Export"))
