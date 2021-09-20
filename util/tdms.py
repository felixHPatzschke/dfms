
# For math things
import numpy as np

# For TDMS file I/O
import nptdms

from enum import Flag, auto

from os import path

import warnings




class Content(int, Flag):
    FULL_DATA: int = auto()
    ROI_DATA: int = auto()
    METADATA: int = auto()

class Format(int, Flag):
    VIDEO: int = auto()
    MODULE: int = auto()

class Descriptor:
    def __init__(self):
        self.data_file = ""
        self.metadata_file = ""
        self.data_format = 0
    
    # assuming the dictionary is valid
    def from_dict(self, dictionary):
        self.data_file = dictionary['data']
        self.metadata_file = dictionary['meta']
        self.data_format = dictionary['format']
    
    def to_dict(self):
        return { 'format' : self.data_format, 'data' : self.data_file, 'meta' : self.metadata_file }


# turn a list of filenames into a list of descriptors
# assume default file name scheme
def files_to_descriptors(files):
    FULL_OR_META = '_video.tdms'
    ROI = '_module.tdms'
    
    DICT_DATA_KEY = 'data'
    DICT_META_KEY = 'meta'
    DICT_FMT_KEY = 'format'
    
    split_by_basename = {}
    # a dictionary to bundle the files that belong together 
    # and use the base names, which ought to be the same, as keys
    for fn in files:
        passing = True
        if fn.endswith('.tdms'):
            # will weed out anything that isn't a TDMS file
            if fn.endswith(FULL_OR_META):
                # should either be a full video or a metadata file
                bn = fn[:-len(FULL_OR_META)]
                suffix = FULL_OR_META
                
            elif fn.endswith(ROI):
                # should be an ROI video file
                bn = fn[:-len(ROI)]
                suffix = ROI
                
            else:
                warnings.warn("{f} is not a recognized format and will be ignored.".format(f=fn))
                passing = False
                
            if passing:
                # create an entry for this basename if it doesn't exist yet
                if bn not in split_by_basename:
                    split_by_basename[bn] = {}
                
                if suffix == FULL_OR_META:
                    split_by_basename[bn][DICT_META_KEY] = fn
                elif suffix == ROI:
                    split_by_basename[bn][DICT_DATA_KEY] = fn
                else:
                    warnings.warn("something has gone VERY wrong")
            
        else:
            if not fn.endswith('.tdms_index'):
                warnings.warn("{f} is not a recognized format and will be ignored.".format(f=fn))
    
    res = []
    # array for output
    for bn in split_by_basename:
        passing = True
        if DICT_DATA_KEY not in split_by_basename[bn]:
            split_by_basename[bn][DICT_DATA_KEY] = split_by_basename[bn][DICT_META_KEY]
            split_by_basename[bn][DICT_FMT_KEY] = Format.VIDEO
        else:
            if DICT_META_KEY not in split_by_basename[bn]:
                warnings.warn("{b} is missing metadata and will be ignored.".format(b=bn))
                # TODO actually remove it from the list
                passing = False
            else:
                split_by_basename[bn][DICT_FMT_KEY] = Format.MODULE
        if passing:
            res.append( Descriptor() )
            res[-1].from_dict( split_by_basename[bn] )
    
    return res
    #return [ Descriptor().from_dict( d ) for d in res ]


class Video:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.frames = 0
        self.kinetic_cycle = 0.0
        self.framerate = 0.0
        self.exposure = 0.0
        self.binning = 0
        self.data = np.zeros( (1,1,1) )
        
    def load_from_tdms_file(self, contents, tdms_file):
        #tdms_file = nptdms.TdmsFile(filename)
        props = tdms_file.properties
        
        if Content.FULL_DATA in contents:
            self.width = int( props['dimx'] )
            self.height = int( props['dimy'] )
            self.frames = int( props['dimz'] )
            self.binning = int( props['binning'] )
            self.kinetic_cycle = float( props['kinetic_cycle'] )
            self.framerate = 1.0/self.kinetic_cycle
            try:
                self.exposure = float( props['exposure_time'] )
            except KeyError:
                self.exposure = self.kinetic_cycle
            
            raw_data = tdms_file['Image']['Image'].data
            raw_data = raw_data.reshape( self.frames, self.width, self.height )
            self.data = raw_data/np.max(raw_data)
        
        if Content.ROI_DATA in contents:
            self.width = int( props['X Pixels'] )
            self.height = int( props['Y Pixels'] )
            #self.frames = int( props['Frames'] ) # !!! BUG: 'Frames' is always 0, needs to be fixed in LabVIEW

            raw_data = tdms_file['Data']['Image ROI'].data
            self.frames = int( raw_data.size/(self.width*self.height) ) # FIX: Get the number of frames from data size and the number of pixel per images
            raw_data = raw_data.reshape( self.frames, self.height, self.width )
            np.swapaxes( raw_data, 1, 2 )
            self.data = raw_data/np.max(raw_data)
        
        if Content.METADATA in contents:
            #self.width = int( props['dimx'] )
            #self.height = int( props['dimy'] )
            #self.frames = int( props['dimz'] )
            self.binning = int( props['binning'] )
            self.kinetic_cycle = float( props['kinetic_cycle'] )
            self.framerate = 1.0/self.kinetic_cycle
            try:
                self.exposure = float( props['exposure_time'] )
            except KeyError:
                self.exposure = self.kinetic_cycle
        
        return self
    
    def load(self, descriptor):
        if descriptor.data_format == Format.VIDEO:
            tdms_file = nptdms.TdmsFile( descriptor.data_file )
            self.load_from_tdms_file( Content.FULL_DATA, tdms_file )
            #del tdms_file
        elif descriptor.data_format == Format.MODULE:
            tdms_file = nptdms.TdmsFile( descriptor.data_file )
            self.load_from_tdms_file( Content.ROI_DATA, tdms_file )
            tdms_file = nptdms.TdmsFile( descriptor.metadata_file )
            self.load_from_tdms_file( Content.METADATA, tdms_file )
            #del tdms_file
        else:
            warnings.warn("something has gone terribly wrong:\ndescriptor.data_format is not a recognized value.")
        return self
    
    def px_to_um(self):
        return (1.8/250)*8*self.binning
    
    
    
    
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



    
