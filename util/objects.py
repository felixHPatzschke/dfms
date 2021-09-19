
# For math things
import numpy as np

# for serialization and deserialization
import json
import pickle

from util import tdms, devices



FORMAT_VERSION = '0.2'

class ParticleInfo:
    def __init__(self, **description):
        self.size = "unknown sized"
        self.material = "unknown"
        self.ptype = "unknown"
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
                        'ref_wavelength':self.ldaref
                    },
                    'img_width':self.roi_width,
                    'particle':self.particle.to_dict(),
                    'devices':[ device.uid for device in self.devices ]
                }

    def serialize(self, *args, **kwargs):
        # dtermine desired output format
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




