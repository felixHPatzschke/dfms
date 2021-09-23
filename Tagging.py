
import os
import sys

from PyQt5 import QtCore,QtWidgets
from PyQt5.QtWidgets import QFileDialog, QTreeWidgetItem, QListWidgetItem

import numpy as np
pi = np.pi
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import pathlib
import datetime

from ui import mainwindow
from util import tdms, devices, objects



obj_dsc = objects.Descriptor()

#video_descriptors = []
videos_loaded = []
videos = []
NOT_INITIALIZED = -1
videos_width = NOT_INITIALIZED 
videos_height = NOT_INITIALIZED 

vdata_max = np.zeros( (1,1,1) )
vdata_mean = np.zeros( (1,1,1) )
current_frame = 0
video_view_mode = "Frame"

devs = []



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

def draw_guide_line( ax, x0, y0, alpha, dist, direction, shift, color ):
    if direction == 0:
        dx = np.cos( pi*alpha/180.0 )
        dy = np.sin( pi*alpha/180.0 )
    else: 
        dx = -np.sin( pi*alpha/180.0 )
        dy = np.cos( pi*alpha/180.0 )
    l = np.max( np.array( [ videos_width, videos_height] ) )
    
    x0 += shift*dist*dy
    y0 -= shift*dist*dx
    
    if direction==0: # lines to show the ROI
        fwd = l
        if shift==0: # central line, used for aiming
            bwd = l
        else:        # bounding box
            bwd = dist
    else:            # orthogonal lines
        if shift==0: # central line, used for aiming
            fwd = l
            bwd = l
        else:        # bounding box
            fwd = dist
            bwd = dist

    xa = x0 - bwd*dx
    ya = y0 - bwd*dy
    xb = x0 + fwd*dx
    yb = y0 + fwd*dy
    
    ax.plot( [xa, xb], [ya, yb], c=color, ls=':', lw=1 )



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
        
        self.ui.doubleSpinBox_x0.valueChanged.connect(self.move_x_box)
        self.ui.doubleSpinBox_y0.valueChanged.connect(self.move_y_box)
        self.ui.horizontalScrollBar.valueChanged.connect(self.move_x_scroll)
        self.ui.verticalScrollBar.valueChanged.connect(self.move_y_scroll)
        
        self.ui.doubleSpinBox_alpha.valueChanged.connect(self.change_alpha)
        self.ui.doubleSpinBox_d.valueChanged.connect(self.change_d)
        
        self.ui.pushButton_2.clicked.connect(self.load_devices)
        self.ui.listWidget.itemClicked.connect(self.update_selected_devices)
        
        self.ui.exportButton.clicked.connect(self.export)
        
        self.video_items = []
        self.dev_items = []
        #self.selected_dev_items = []
        
        self.initialize_io_widgets()
        self.load_devices()
        
        self.ui.tabWidget.setCurrentIndex(0)
    
    def initialize_io_widgets(self):
        self.ui.progressBar.setValue(0)
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
        self.ui.doubleSpinBox_d.setValue(3)
        self.ui.doubleSpinBox_d.setValue(21)
        # nothing else to do here, example values are already reasonable
        
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
        global obj_dsc, videos_loaded, videos, videos_width, videos_height
        
        videos_width = NOT_INITIALIZED
        videos_height = NOT_INITIALIZED
        
        options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self,"Select TDMS Files", "","TDMS Files (*.tdms);;All Files (*)", options=options)
        if files:
            #obj_dsc.videos = []
            obj_dsc.videos = tdms.files_to_descriptors(files)
            videos_loaded = []
            videos = []
            for i in range(len(obj_dsc.videos)):
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
        global obj_dsc
        
        self.video_items = []
        vidx = 0
        for dsc in obj_dsc.videos:
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
            #item.setCheckState(0, False)
            self.video_items.append(item)
            vidx += 1
        self.ui.treeWidget.clear()
        self.ui.treeWidget.insertTopLevelItems(0, self.video_items)
        for i in self.video_items:
            self.ui.treeWidget.expandItem(i)
    
    def load_video_first(self):
        self.load_videos( [0] )
    
    def load_video_last(self):
        self.load_videos( [-1] )
    
    """
    def load_video_selected(self):
        selected_indices = []
        selected_items = self.ui.treeWidget.selectedItems();
        
        self.load_videos( selected_indices )
    """
    
    def load_video_all(self):
        self.load_videos( range(len(obj_dsc.videos)) )
    
    def load_videos(self, indices):
        global videos, videos_loaded, obj_dsc, videos_width, videos_height
        #print("video_descriptors:\t{l}".format(l = len(obj_dsc.videos)))
        #print("videos_loaded:\t{l}".format(l = len(videos_loaded)))
        #print("videos:\t{l}".format(l = len(videos)))
        
        if indices:
            self.ui.progressBar.setEnabled(True)
            self.ui.progressBar.setMinimum(0)
            self.ui.progressBar.setMaximum(len(indices))
            pos = 0
            self.ui.progressBar.setValue( pos )
            
            for idx in indices:
                videos[idx].load( obj_dsc.videos[idx] )
                videos_loaded[idx] = True
                if videos_width == NOT_INITIALIZED:
                    videos_width = videos[idx].width
                    videos_height = videos[idx].height
                else:
                    if not ( (videos_width == videos[idx].width) and (videos_height == videos[idx].height) ):
                        print( "WARNING: video {i} does not have the same dimensions as the previously loaded data!".format(i=idx) )
                        videos_loaded[idx] = False
                        # TODO: actually handle the error
                pos += 1
                self.ui.progressBar.setValue( pos )
        
        # debug output
        """
        for idx in range(len(obj_dsc.videos)):
            print("Video {i}:".format(i=idx))
            if videos_loaded[idx]:
                print("  {f} Frames".format(f=videos[idx].frames))
                print("  {w}x{h} px".format(w=videos[idx].width, h=videos[idx].height))
            else:
                print("  not loaded")
        """
        
        if indices:
            maxs = []
            means = []
            for i in range(len(obj_dsc.videos)):
                if videos_loaded[i]:
                    maxs.append( np.max( videos[i].data, axis=0 ) )
                    means.append( np.mean( videos[i].data, axis=0 ) )
            
            global vdata_max, vdata_mean
            vdata_max = np.max( np.array(maxs), axis=0)
            vdata_mean = np.mean( np.array(means) , axis=0)
            
            obj_dsc.x = int( videos_width / 2 )
            obj_dsc.y = int( videos_height / 2 )
            #print( vdata_max.size )
            obj_dsc.angle = 180.0
            if obj_dsc.roi_width > np.min( vdata_max.size ):
                obj_dsc.roi_width = np.min( vdata_max.size )
            
            self.ui.horizontalScrollBar.setMinimum(0)
            self.ui.horizontalScrollBar.setMaximum(videos_width-1)
            self.ui.horizontalScrollBar.setValue( obj_dsc.x )
            self.ui.doubleSpinBox_x0.setMaximum(videos_width-1)
        
            self.ui.verticalScrollBar.setMinimum(0)
            self.ui.verticalScrollBar.setMaximum(videos_height-1)
            self.ui.verticalScrollBar.setValue( obj_dsc.y )
            self.ui.doubleSpinBox_y0.setMaximum(videos_height-1)
        
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
    
    def move_x_scroll(self):
        global obj_dsc
        
        obj_dsc.x = self.ui.horizontalScrollBar.value()
        self.ui.doubleSpinBox_x0.setValue(obj_dsc.x)
    
    def move_y_scroll(self):
        global obj_dsc
        
        obj_dsc.y = self.ui.verticalScrollBar.value()
        self.ui.doubleSpinBox_y0.setValue(obj_dsc.y)
    
    def move_x_box(self):
        global obj_dsc
        
        obj_dsc.x = self.ui.doubleSpinBox_x0.value()
        
        self.plot_image()
        #self.plot_preview()
    
    def move_y_box(self):
        global obj_dsc
        
        obj_dsc.y = self.ui.doubleSpinBox_y0.value()
        
        self.plot_image()
        #self.plot_preview()
    
    def change_alpha(self):
        global obj_dsc
        obj_dsc.angle = -1.0*self.ui.doubleSpinBox_alpha.value()
        self.plot_image()
        #self.plot_preview()
    
    def change_d(self):
        global obj_dsc
        obj_dsc.roi_width = self.ui.doubleSpinBox_d.value()
        self.plot_image()
        #self.plot_preview()
    
    def scrub_frames(self):
        global current_frame
        current_frame = self.ui.horizontalSlider.value()
        self.ui.label_4.setText("{c} / {a}".format(c=current_frame, a=avail_frame_count()))
        if current_frame < avail_frame_count():
            #print("Current Frame: {c}".format(c=current_frame))
            #vi, fi = indices_from_frame( current_frame )
            #print("    In Video   {v}".format(v=vi))
            #print("    Frame      {f}".format(f=fi))
            self.plot_image()
    
    def plot_image(self):
        if avail_frame_count() > 0:
            self.image_figure.clear()
            #self.image_figure.set_facecolor('black')
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
            
            # draw crosshairs
            x0, y0 = obj_dsc.x, obj_dsc.y
            alpha = obj_dsc.angle
            dist = 0.5*(obj_dsc.roi_width-1)
            
            for shift in [0, -1, 1]:
                for direction in [0, 1]:
                    draw_guide_line( ax, x0, y0, alpha, dist, direction, shift, 'w' )
            
            ax.set_xlim( [ -0.5, videos_width-0.5 ] )
            ax.set_ylim( [ videos_height-0.5, -0.5 ] )
            
            self.image_canvas.draw()
    
    def load_devices(self):
        global devs
        devs = devices.load_all()
        
        self.ui.listWidget.clear()
        self.dev_items = []
        self.dev_ids = []
        for ID in devs:
            text = "{f}\n{v} {n}".format( f=devs[ID].function, v=devs[ID].vendor, n=devs[ID].name )
            item = QListWidgetItem( text )
            item.setFlags( QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable )
            item.setCheckState( 2 )
            
            self.dev_ids.append( devs[ID].uid )
            self.dev_items.append(item)
            self.ui.listWidget.addItem( item )
    
    def update_selected_devices(self):
        #self.selected_dev_items = []
        global obj_dsc
        obj_dsc.devices = []
        for i in range(len( self.dev_items )):
            #print( self.dev_items[i].checkState() )
            if self.dev_items[i].checkState():
                obj_dsc.devices.append( self.dev_ids[i] )
        
        """
        # DEBUG OUTPUT
        print( "-------------------------------------" )
        for d in self.selected_dev_items:
            print( d.uid )
        """
    
    def export(self):
        #obj_dsc.x = self.ui.doubleSpinBox_x0.value()
        #obj_dsc.y = self.ui.doubleSpinBox_y0.value()
        obj_dsc.particle.size = self.ui.lineEdit_3.text()
        obj_dsc.particle.material = self.ui.lineEdit.text()
        obj_dsc.particle.comment = self.ui.lineEdit_2.text()
        obj_dsc.particle.ptype = self.ui.comboBox_3.currentText()
        
        date_string = datetime.datetime.fromtimestamp( pathlib.Path( obj_dsc.videos[0].data_file ).stat().st_mtime ).__format__('%y-%m-%d')
        part_no = self.ui.spinBox_particleNo.value()
        exportfile = open('out/objects/{DATE}-object{NR:04d}.json'.format(NR=part_no, DATE=date_string), "w")
        exportfile.write( obj_dsc.serialize('json') )
        exportfile.close()
        self.ui.spinBox_particleNo.setValue(part_no + 1)


# ENTRY POINT
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
