
import os
import sys

# For math things
import numpy as np
from scipy.interpolate import interp1d

# for serialization and deserialization
import pickle



class SpectrometerDataSet:
    def __init__(self):
        self.LDA = np.array( [0.0, 1000.0] )
        self.VAL = np.array( [1.0, 1.0] )
        self.normalization = 1.0
    
    def load(self, filename, separator=';', normalize=True):
        file_instance = open(filename, 'r')
        lines = file_instance.readlines()
        file_instance.close()
        
        nlines = len(lines)
        LDA = np.zeros( nlines )
        VAL = np.zeros( nlines )
        i = 0
        section = ""
        
        for line in lines:
            if line[:1] == '[':
                section = line[1:-2]
                #print( section, file=sys.stderr )
            else:
                if section == "SpectrumHeader":
                    prop = line.split(separator)[0]
                    if prop == "#Date":
                        self.date = line.split(separator)[1][:-1]
                    elif prop == "#Time":
                        self.time = line.split(separator)[1][:-1]
                    elif prop == "#InstrModel":
                        self.instrument_model = line.split(separator)[1][:-1]
                if section == "Data":
                    strings = line.split(separator)
                    LDA[i] = ( strings[0] )
                    VAL[i] = ( strings[1] )
                    i += 1
        
        self.LDA = LDA[:i]
        self.VAL = VAL[:i]
        if normalize:
            self.normalization = np.mean( self.VAL )
            
        return self
    
    def interpolate(self, lda):
        i = 0
        res = np.empty_like( lda )
        # catch ArrayIndexOutOfBoundsException here (except it's not called that in python)
        for j in range(len(lda)):
            try:
                while lda[j] > self.LDA[i+1]:
                    i += 1
                
                la = self.LDA[i]    
                lb = self.LDA[i+1]
                
                d = (lda[j]-la)/(lb-la) 
                
                va = self.VAL[i]
                vb = self.VAL[i+1]
                
                vd = vb-va
                
                res[j] = va+d*vd
            except IndexError:
                res[j] = 0.0
            
        return res


class Descriptor:
    def __init__(self, **descr):
        self.name = ""
        self.vendor = ""
        self.function = ""
        self.uid = "" # unique identifier (TODO: make sure they're actually unique)
        
        for attrib in descr:
            if attrib == 'name':
                self.name = descr[attrib]
            elif attrib == 'vendor':
                self.vendor = descr[attrib]
            elif attrib == 'function':
                self.function = descr[attrib]
            elif attrib == 'uid':
                self.uid = descr[attrib]
    
    def descr_str(self):
        return "{f}: {v} {n}".format( f=self.function, v=self.vendor, n=self.name )
    
    def to_dict(self):
        return { 'vendor':self.vendor, 'name':self.name, 'function':self.function, 'uid':self.uid }

    def from_dict(self, d):
        self.vendor = d['vendor']
        self.name= d['name']
        self.function= d['function']
        self.uid= d['uid']
        return self

# characteristic spectra of optical components involved, such as
#  -> light sources
#  -> camera seonsors
#  -> lenses
#  -> ...
class Device:
    def __init__(self, **descr):
        self.name = ""
        self.vendor = ""
        self.function = ""
        self.uid = ""
        
        self.id_data = Descriptor(**descr).to_dict()
        self.spec_val = interp1d( np.array([0.0, 500.0, 1000.0]),
                                  np.array([1.0, 1.0, 1.0]),
                                  kind=2 )
        self.spec_err = interp1d( np.array([0.0, 500.0, 1000.0]),
                                  np.array([0.0, 1.0, 0.0]),
                                  kind=2 )
        self.ldamin = 500.0
        self.ldamax = 700.0
        
        for attrib in descr:
            if attrib == 'name':
                self.name = descr[attrib]
            elif attrib == 'vendor':
                self.vendor = descr[attrib]
            elif attrib == 'function':
                self.function = descr[attrib]
            elif attrib == 'uid':
                self.uid = descr[attrib]

    
    def evaluate(self, LDA):
        return self.spec_val(LDA), self.spec_err(LDA)
    
    def ingest_spectrometer_data(self, datasets, normalize=True):
        self.ldamin = np.max( np.array( [ np.min(dataset.LDA) for dataset in datasets ] ) )
        self.ldamax = np.min( np.array( [ np.max(dataset.LDA) for dataset in datasets ] ) )
        
        # maybe make sample density variable?
        samples = int( np.sum( np.array( [ dataset.LDA.shape[0] for dataset in datasets ] ) ) / len(datasets) )
        
        lda = np.linspace( self.ldamin, self.ldamax, num=samples, endpoint=True )
        
        vals = np.array( [ dataset.interpolate(lda)/dataset.normalization for dataset in datasets ] )
        val = np.mean( vals, axis=0 )
        err = np.sqrt( np.sum( np.square( vals-val ), axis=0 ) )
        
        if normalize:
            norm = np.max(val)
            val /= norm
            err /= norm
        
        self.spec_val = interp1d( lda, val, kind=2 )
        self.spec_err = interp1d( lda, err, kind=2 )
        
    def descr_str(self):
        return "{f}: {v} {n}".format( f=self.function, v=self.vendor, n=self.name )
    
    def set_limits(self, ldamin, ldamax):
        self.ldamin = ldamin
        self.ldamax = ldamax
    
    def set_description(self, **descr):
        self.id_data = Descriptor(**descr).to_dict()



persistent_data_path = "persistent/devices/"

def export(dev):
    filename = "{d}/{u}.pickle".format( d=persistent_data_path, u=dev.uid )
    exportfile = open( filename, 'wb' )
    exportfile.write( pickle.dumps(dev) )
    exportfile.close()

def load(filename):
    inputfile = open( filename, 'rb' )
    dev = pickle.loads( inputfile.read() )
    inputfile.close()
    return dev

"""
def load_all():
    filenames = os.listdir( persistent_data_path )
    devices = [ load( "{d}/{f}".format( d=persistent_data_path, f=fn ) ) for fn in filenames ]
    return devices
"""

def load_all():
    filenames = os.listdir( persistent_data_path )
    devices = {}
    for fn in filenames:
        dev = load( "{d}/{f}".format( d=persistent_data_path, f=fn ) )
        devices[dev.uid] = dev
    return devices
