
# For math things
import numpy as np
from scipy import interpolate
# used once in interpolation
# TODO: maybe find the numpy equivalent to improve performace
import math

# For TDMS file I/O
import nptdms

from enum import Flag, auto

from os import path

import warnings




class Content(int, Flag):
    FULL_DATA: int = 1
    ROI_DATA: int = 2
    METADATA: int = 4

class Format(int, Flag):
    VIDEO: int = 1
    MODULE: int = 2

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

    def from_dict(self, d):
        self.data_format = d['format']
        self.data_file = d['data']
        self.metadata_file = d['meta']
        return self


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



class VideoSeries(Video):
    def __init__(self):
        super().__init__()
        self.descriptors = []
        self.valid = True
        self.loaded = False
    
    # empty override
    def load_from_tdms_file(self, contents, tdms_file):
        return self
    
    def load(self, descriptors):
        self.descriptors = descriptors
        if self.descriptors:
            videos = [ Video().load(d) for d in self.descriptors ]
            
            """
            check that the loaded videos have the same format
            and sum up the frame count while we're iterating anyway
            """
            for v in videos:
                if not v.width == self.width:
                    if self.width == 0:
                        self.width = v.width
                    else:
                        self.valid = False
                
                if not v.height == self.height:
                    if self.height == 0:
                        self.height = v.height
                    else:
                        self.valid = False
                
                if not v.kinetic_cycle == self.kinetic_cycle:
                    if self.kinetic_cycle == 0:
                        self.kinetic_cycle = v.kinetic_cycle
                    else:
                        print("kinetic_cycle not equal (maybe not critical? proceeding...)")
                        #self.valid = False
                
                if not v.exposure == self.exposure:
                    if self.exposure == 0:
                        self.exposure = v.exposure
                    else:
                        print("exposure not equal (maybe not critical? proceeding...)")
                        #self.valid = False
                
                if not v.binning == self.binning:
                    if self.binning == 0:
                        self.binning = v.binning
                    else:
                        self.valid = False
                
                if self.valid:
                    self.frames += v.frames
            
            if self.valid:
                self.framerate = 1.0/self.kinetic_cycle
                
                #self.data = np.zeros( (self.frames, self.width, self.height) )
                self.data = np.zeros( (self.frames, self.height, self.width) )
                begin_frame = 0
                for v in videos:
                    #self.data[ begin_frame:begin_frame+v.frames, :, : ] = np.swapaxes( v.data, 1, 2 )
                    self.data[ begin_frame:begin_frame+v.frames, :, : ] = v.data
                    begin_frame += v.frames
            
            del videos
            self.loaded = True
        return self
    
    def interpolateXY(self, x, y):
        xf = math.floor(x)
        yf = math.floor(y)

        xm = x-xf
        ym = y-yf
        
        # If this is a bad way to do it, why is is so easy?
        try:
            va = (1-xm)*self.data[:,xf,yf]   + (xm)*self.data[:,xf+1,yf]
            vb = (1-xm)*self.data[:,xf,yf+1] + (xm)*self.data[:,xf+1,yf+1]
            return (1-ym)*va + (ym)*vb
        except IndexError:
            #return 0
            return np.min( self.data, axis=(1,2) ) # should get rid of the divide-by-zero error
    
    def interpolate(self, F, Y, X, k=3):
        x1d = np.arange( self.height )
        y1d = np.arange( self.width )
        
        #x,y = np.meshgrid( x1d, y1d )
        z = self.data[ F, :, : ]
        
        interp = interpolate.RectBivariateSpline( x1d, y1d, z, kx=k, ky=k )
        
        return interp(Y, X, grid=False)
