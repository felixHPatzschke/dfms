
# For math things
import numpy as np
from numpy import pi as pi

# for serialization and deserialization
import json
import pickle

from util import tdms, devices



FORMAT_VERSION = '0.2'

class ParticleInfo:
    def __init__(self, **description):
        self.size = "unknown sized"
        self.material = "unknown"
        self.ptype = "Particle"
        self.comment = ""
        
        self.set_info(**description)
    
    def set_info(self, **description):
        for attrib in description:
            if attrib in [ 's', 'S', 'size', 'Size', 'SIZE' ]:
                self.size = description[attrib]
            if attrib in [ 'm', 'M', 'mat', 'Mat', 'MAT', 'material', 'Material', 'MATERIAL' ]:
                self.material = description[attrib]
            if attrib in [ 't', 'T', 'type', 'Type', 'TYPE', 'c', 'C', 'class', 'Class', 'CLASS' ]:
                self.ptype= description[attrib]
            if attrib in [ 'comment', 'Comment', 'COMMENT' ]:
                self.comment = description[attrib]
    
    def descr_str(self):
        if len(self.comment) == 0:
            return "{s} {m} {t}".format( s=self.size, m=self.material, t=self.ptype )
        else:
            return "{s} {m} {t} ({c})".format( s=self.size, m=self.material, t=self.ptype, c=self.comment )
    
    def to_dict(self):
        return  {
                    'size':self.size,
                    'material':self.material,
                    'class':self.ptype,
                    'comment':self.comment
                }
    
    def from_dict(self, d):
        self.size = d['size']
        self.material = d['material']
        self.ptype = d['class']
        self.comment = d['comment']
        return self



class Descriptor:
    def __init__(self):
        self.videos = []
        self.x = 0
        self.y = 0
        self.angle = 0.0
        self.sref = 0.0
        self.ldaref = 0.0
        self.roi_width = 0
        self.particle = ParticleInfo()
        self.devices = []
    
    def to_dict(self):
        return  {
                    'version':FORMAT_VERSION,
                    'files':[ video.to_dict() for video in self.videos ],
                    '0th-order':[ self.x, self.y ],
                    '1st-order':{
                        'angle':self.angle,
                        'ref-offset':self.sref,
                        'ref-wavelength':self.ldaref
                    },
                    'img_width':self.roi_width,
                    'particle':self.particle.to_dict(),
                    'devices':self.devices
                }

    def from_dict(self, d):
        #self.videos = []
        #for f in d['files']:
        #    self.videos.append( tdms.Descriptor().from_dict(f) )
        self.videos = [ tdms.Descriptor().from_dict(f) for f in d['files'] ]
        self.x = d['0th-order'][0]
        self.y = d['0th-order'][1]
        self.angle = d['1st-order']['angle']
        self.sref = d['1st-order']['ref-offset']
        self.ldaref = d['1st-order']['ref-wavelength']
        self.roi_width = d['img_width']
        self.particle = ParticleInfo().from_dict(d['particle'])
        self.devices = d['devices']
        return self
    
    def serialize(self, *args, **kwargs):
        # determine desired output format
        output_format = 'json'
        for arg in args:
            if arg in [ 'j', 'J', 'json', 'Json', 'JSON' ]:
                output_format = 'json'
            elif arg in [ 'p', 'P', 'pickle', 'Pickle', 'PICKLE' ]:
                output_format = 'pickle'
        
        for kw in kwargs:
            if kw in [ 'f', 'F', 'format', 'f' ]:
                if kwargs[kw] in [ 'j', 'J', 'json', 'Json', 'JSON' ]:
                    output_format = 'json'
                elif kwargs[kw] in [ 'p', 'P', 'pickle', 'Pickle', 'PICKLE' ]:
                    output_format = 'pickle'
        
        # actual serialization
        if output_format == 'json':
            return json.dumps(self.to_dict(), indent=2)
        elif output_format == 'pickle':
            return pickle.dumps(self)
        else:
            return ""


class Object:
    def __init__(self):
        self.descriptor = Descriptor()
        self.video = tdms.VideoSeries()
        self.correction = devices.Correction()
        
        self.MAX_LDA = 0.0
        self.roi_generated = False
        self.ROI = self.data = np.zeros( (1,1,1) )
        self.LDA = self.data = np.zeros( (1,1,1) )
        
    def gen_roi_coords(self, MAX_LDA = False):
        if not MAX_LDA:
            MAX_LDA = self.MAX_LDA

        dim = [
                  int(self.descriptor.roi_width + self.descriptor.sref*MAX_LDA/self.descriptor.ldaref),
                  int(self.descriptor.roi_width)
              ]
        
        # ranges of X and Y coordinates
        X1 = np.arange( dim[0] ) - (self.descriptor.roi_width-1)/2
        Y1 = np.arange( dim[1] ) - (self.descriptor.roi_width-1)/2
        
        # areas of X and Y coordinates
        X2, Y2 = np.meshgrid( X1, Y1 )
        
        # apply rotation
        X3 = np.cos( pi/180.0*self.descriptor.angle )*X2 - np.sin( pi/180.0*self.descriptor.angle )*Y2
        Y3 = np.cos( pi/180.0*self.descriptor.angle )*Y2 + np.sin( pi/180.0*self.descriptor.angle )*X2
        
        # apply translation
        X3 = X3 + self.descriptor.x
        Y3 = Y3 + self.descriptor.y
        
        LDA = X2*self.descriptor.ldaref/self.descriptor.sref
        
        return X3, Y3, LDA
    
    def gen_roi(self, MAX_LDA = 900.0, k=3):
        self.MAX_LDA = MAX_LDA
        X, Y, self.LDA = self.gen_roi_coords(self.MAX_LDA)
        
        roi_data = np.zeros( ( self.video.frames, X.shape[0], X.shape[1] ) )
        for F in range( self.video.frames ):
            roi_data[ F, :, : ] = self.video.interpolate( F, Y, X, k )
        
        #return roi_data, LDA
        self.ROI = roi_data
        self.roi_generated = True
        return self
    
    def roi_extent(self, MAX_LDA = False):
        if not MAX_LDA:
            MAX_LDA = self.MAX_LDA

        origin = (self.descriptor.roi_width-1)/2
        
        left = -0.5 - origin
        right = int(self.descriptor.roi_width + self.descriptor.sref*MAX_LDA/self.descriptor.ldaref) - 0.5 - origin
        bottom = int(self.descriptor.roi_width) - 0.5 - origin
        top = -0.5 - origin
        
        return ( left, right, bottom, top )
    
    def roi(self, MAX_LDA = False):
        if not MAX_LDA:
            if self.roi_generated:
                MAX_LDA = self.MAX_LDA
            else:
                self.MAX_LDA = 900
                MAX_LDA = 900
        
        if ( not MAX_LDA == self.MAX_LDA ) or ( not self.roi_generated ):
            self.gen_roi(MAX_LDA)
        return self.ROI
    
    def zeroth_order(self):
        if self.roi_generated:
            return self.ROI[ : , : , 0:self.ROI.shape[1] ]
    
    def subtract_background(self):
        if o.roi_generated:
            bg_upper = o.ROI[ : , 0 , : ]
            bg_lower = o.ROI[ : ,-1 , : ]

            bg = np.empty_like( o.ROI )
            for y in range( bg.shape[1] ):
                a_lower = y/( bg.shape[1]-1 )
                a_upper = 1-a_lower
                bg[ : , y , : ] = a_lower*bg_lower + a_upper*bg_upper
            self.ROI -= bg

        return self



