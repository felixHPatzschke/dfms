
# For math things
import numpy as np

# For TDMS file I/O
import nptdms

from enum import Flag, auto




class TDMS_CONTENTS(Flag):
    FULL_DATA = auto()
    ROI_DATA = auto()
    METADATA = auto()

class TDMS_FORMATS(Flag):
    VIDEO = auto()
    MODULE = auto()
    



class Video:
    def __init__(self, *args, **kwargs):
        self.width = 0
        self.height = 0
        self.frames = 0
        self.kinetic_cycle = 0.0
        self.exposure = 0.0
        self.binning = 0
        self.data = np.zeros( (1,1,1) )
        
    def load(self, contents, tdms_file):
        #tdms_file = nptdms.TdmsFile(filename)
        props = tdms_file.properties
        
        if TDMS_CONTENTS.FULL_DATA in contents:
            self.width = int( props['dimx'] )
            self.height = int( props['dimy'] )
            self.frames = int( props['dimz'] )
            self.binning = int( props['binning'] )
            self.kinetic_cycle = int( props['kinetic_cycle'] )
            self.exposure = int( props['exposure_time'] )
            
            raw_data = tdms_file['Image']['Image'].data
            raw_data.reshape( self.frames, self.width, self.height )
            self.data = raw_data/np.max(raw_data)
        
        if TDMS_CONTENTS.ROI_DATA in contents:
            self.width = int( props['X Pixels'] )
            self.height = int( props['Y Pixels'] )
            #self.frames = int( props['Frames'] ) # !!! BUG: 'Frames' is always 0, needs to be fixed in LabVIEW

            raw_data = tdms_file['Data']['Image ROI'].data
            self.frames = int(self.data.size/(self.width*self.height)) # FIX: Get the number of frames from data size and the number of pixel per images
            raw_data.reshape( self.frames, self.width, self.height )
            self.data = raw_data/np.max(raw_data)
        
        if TDMS_CONTENTS.METADATA in contents:
            #self.width = int( props['dimx'] )
            #self.height = int( props['dimy'] )
            #self.frames = int( props['dimz'] )
            self.binning = int( props['binning'] )
            self.kinetic_cycle = int( props['kinetic_cycle'] )
            self.exposure = int( props['exposure_time'] )
        
        return self
        
    def framerate(self):
        return 1.0/self.kinetic_cycle
    
    
    
    
# Returns:
#   fully initialized instance of Video
# Usages:
#   read_TDMS( "/path/Sample_001_video.tdms" ) 
#     -> recognize as complete data file
#   read_TDMS( "/path/Sample_001_module.tdms" ) 
#     -> recognize as ROI file
#     -> find and read Metadata file automatically
#   read_TDMS( "/path/Sample_001" )
#     -> recognize as incomplete filename
#def read_TDMS( filename ):



    
