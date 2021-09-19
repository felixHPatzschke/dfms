
import os
import sys

from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTreeWidgetItem

import numpy as np
pi = np.pi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from ui import mainwindow
from util import tdms



video_descriptors = []
videos_loaded = []
videos = []
vdata_max = np.zeros( (1,1,1) )
vdata_mean = np.zeros( (1,1,1) )
current_frame = 0
video_view_mode = "Frame"

def avail_frame_count():
    res = 0
    for i in range(len(videos_loaded)):
        if videos_loaded[i]:
            res += videos[i].frames
    return res

def indices_from_frame(f):
    vi = 0
    fi = f
    if f < avail_frame_count():
        for i in range(len(videos_loaded)):
            if videos_loaded[i]:
                if fi >= videos[i].frames:
                    fi -= videos[i].frames
                    vi += 1
                else:
                    return vi, fi
            else:
                vi += 1
    else:
        return False # TODO: raise a proper Error

def get_frame(f):
    if f < avail_frame_count():
        vi, fi = indices_from_frame(f)
        return videos[vi].data[fi]
    else:
        return False # TODO: raise a proper Error



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.pushButton.clicked.connect(self.select_input_files)
        self.input_files_selected = False
        
        self.ui.pushButton_3.clicked.connect(self.load_video_first)
        self.ui.pushButton_4.clicked.connect(self.load_video_last)
        #self.ui.pushButton_5.clicked.connect(self.load_video_selected)
        self.ui.pushButton_6.clicked.connect(self.load_video_all)
        
        self.ui.horizontalSlider.valueChanged.connect(self.scrub_frames)
        self.ui.comboBox_2.currentTextChanged.connect(self.change_video_view_mode)
        
        self.initialize_io_widgets()
    
    def initialize_io_widgets(self):
        self.ui.progressBar.setEnabled(False)
        
        # Video view and control
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setMaximum( avail_frame_count() )
        self.ui.label_4.setText("{c} / {a}".format(c=current_frame, a=avail_frame_count()))
        
        # Import Tab
        self.ui.treeWidget.clear()
        self.ui.treeWidget.setColumnWidth(0,172)
        self.ui.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        for btn in [ self.ui.pushButton_3, self.ui.pushButton_4, self.ui.pushButton_5, self.ui.pushButton_6 ]:
            btn.setEnabled(self.input_files_selected)
        
        # Alignment Tab
        # nothing to do here, example values are already reasonable
        
        # Type and Corrections Tab
        self.ui.listWidget.clear()
        # example values in the input fields for particle info are already resonable.
        
        # Export Tab
        # nothing to do here, example values are already reasonable
        
        # Prepare Plot Area for Microscope Image
        self.image_figure = plt.figure()
        self.image_canvas = FigureCanvas(self.image_figure)
        #self.image_toolbar = NavigationToolbar(self.image_canvas, self)
        layout = QtWidgets.QVBoxLayout()
        #layout.addWidget(self.image_toolbar)
        layout.addWidget(self.image_canvas)
        self.ui.plotWidget.setLayout(layout)
    
    def select_input_files(self):
        global video_descriptors, videos_loaded, videos
        
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;TDMS Files (*.tdms)", options=options)
        if files:
            #video_descriptors = []
            video_descriptors = tdms.files_to_descriptors(files)
            videos_loaded = []
            videos = []
            for i in range(len(video_descriptors)):
                videos_loaded.append(False)
                videos.append( tdms.Video() )
            
            self.show_video_descriptors()
            self.input_files_selected = True
            #for btn in [ self.ui.pushButton_3, self.ui.pushButton_4, self.ui.pushButton_5, self.ui.pushButton_6 ]:
            for btn in [ self.ui.pushButton_3, self.ui.pushButton_4, self.ui.pushButton_6 ]:
                btn.setEnabled(self.input_files_selected)
            
            self.ui.horizontalSlider.setMinimum(0)
            self.ui.horizontalSlider.setMaximum( avail_frame_count() )
            self.ui.label_4.setText("{c} / {a}".format(c=current_frame, a=avail_frame_count()))
    
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
    
    def load_video_first(self):
        self.load_videos( [0] )
    
    def load_video_last(self):
        self.load_videos( [-1] )
    
    #def load_video_selected(self):
    #    selected_indices = []
    #    selected_items = self.ui.treeWidget.selectedItems();
    #    
    #    self.load_videos( selected_indices )
    
    def load_video_all(self):
        self.load_videos( range(len(video_descriptors)) )
    
    def load_videos(self, indices):
        global videos, videos_loaded, video_descriptors
        #print("video_descriptors:\t{l}".format(l = len(video_descriptors)))
        #print("videos_loaded:\t{l}".format(l = len(videos_loaded)))
        #print("videos:\t{l}".format(l = len(videos)))
        
        if indices:
            self.ui.progressBar.setEnabled(True)
            self.ui.progressBar.setMinimum(0)
            self.ui.progressBar.setMaximum(len(indices))
            pos = 0
            self.ui.progressBar.setValue( pos )
            
            for idx in indices:
                videos[idx].load( video_descriptors[idx] )
                videos_loaded[idx] = True
                pos += 1
                self.ui.progressBar.setValue( pos )
        
        # debug output
        for idx in range(len(video_descriptors)):
            print("Video {i}:".format(i=idx))
            if videos_loaded[idx]:
                print("  {f} Frames".format(f=videos[idx].frames))
                print("  {w}x{h} px".format(w=videos[idx].width, h=videos[idx].height))
            else:
                print("  not loaded")
        
        maxs = []
        means = []
        for i in range(len(video_descriptors)):
            if videos_loaded[i]:
                maxs.append( np.max( videos[i].data, axis=0 ) )
                means.append( np.mean( videos[i].data, axis=0 ) )
        
        global vdata_max, vdata_mean
        vdata_max = np.max( np.array(maxs), axis=0)
        vdata_mean = np.mean( np.array(means) , axis=0)
        
        self.ui.progressBar.setEnabled(False)
        
        # set paramters to the frame scrub slider and other control elements
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setMaximum( avail_frame_count() )
        self.ui.label_4.setText("{c} / {a}".format(c=current_frame, a=avail_frame_count()))
        
        self.plot_image()
    
    def change_video_view_mode(self):
        global video_view_mode
        video_view_mode = self.ui.comboBox_2.currentText()
        framemode = (video_view_mode == "Frame")
        self.ui.horizontalSlider.setEnabled( framemode )
        self.ui.label_4.setEnabled( framemode )
        
        self.plot_image()
    
    def scrub_frames(self):
        global current_frame
        current_frame = self.ui.horizontalSlider.value()
        self.ui.label_4.setText("{c} / {a}".format(c=current_frame, a=avail_frame_count()))
        if current_frame < avail_frame_count():
            print("Current Frame: {c}".format(c=current_frame))
            vi, fi = indices_from_frame( current_frame )
            print("    In Video   {v}".format(v=vi))
            print("    Frame      {f}".format(f=fi))
            self.plot_image()
    
    def plot_image(self):
        self.image_figure.clear()
        ax = self.image_figure.add_subplot(111)
        self.image_figure.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=None, hspace=None)
        
        ax.set_axis_off()
        
        if video_view_mode == "Frame":
            #vi, fi = indices_from_frame(current_frame)
            im = ax.imshow( get_frame(current_frame) , cmap="jet")
        elif video_view_mode == "Maximum":
            im = ax.imshow( vdata_max , cmap="jet")
        elif video_view_mode == "Mean":
            im = ax.imshow( vdata_mean , cmap="jet")
        
        #ax.set_xlim([0, videos[vi].width-1])
        #ax.set_ylim([videos[vi].height-1, 0])
        
        self.image_canvas.draw()


# ENTRY POINT
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
