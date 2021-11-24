
# For math things
import numpy as np
import numpy.typing
import scipy.signal
#from scipy import interpolate
# used once in interpolation
# TODO: maybe find the numpy equivalent to improve performace
import math

# For reading TIFF files
import skimage.io

from enum import Flag, auto

from os import path

import warnings



"""
A utility class to simplify access to array slices.
The idea is to call an instance of this class with an array as the argument.
Should improve code readability. ( ROI(image) as opposed to image[ROI.ymin:ROI.ymax,ROI.xmin:ROI.xmax] )
"""
class PrimitiveImageROI:
    # Constructor
    def __init__(self, **kwargs):
        self.xmin = 0
        self.xmax = 0
        self.ymin = 0
        self.ymax = 0
        for kw in kwargs:
            if kw in ['xmin', 'left']:
                self.xmin = kwargs[kw]
            elif kw in ['xmax', 'right']:
                self.xmax = kwargs[kw]
            elif kw in ['ymin', 'top']:
                self.ymin = kwargs[kw]
            elif kw in ['ymax', 'bottom']:
                self.ymax = kwargs[kw]
    
    def xmid(self):
        return 0.5*(self.xmin+self.xmax)
    
    def ymid(self):
        return 0.5*(self.ymin+self.ymax)
    
    def width(self):
        return self.xmax-self.xmin
    
    def height(self):
        return self.ymax-self.ymin
    
    def to_extent(self):
        return [ self.xmin-0.5, self.xmax-0.5, self.ymax-0.5, self.ymin-0.5 ]
    
    """
    In case one wants to use the object like this:
    ROI(image)
    """
    def __call__(self, arr:np.typing.ArrayLike):
        return arr[self.ymin:self.ymax,self.xmin:self.xmax]
    
    """
    The i.m.o. more elegant implementation should enable usage like this:
    image[ROI]
    but I don't currently know how that would work.
    Implicit conversion to a tuple of slice-objects, i should think.
    For now...
    """
    def idxs(self):
        return ( slice(self.ymin, self.ymax), slice(self.xmin, self.xmax) )
    
    def to_string(self):
        return "ROI: x:[{a}:{b}], y:[{c}:{d}]".format(a=self.xmin, b=self.xmax, c=self.ymin, d=self.ymax)

class TIFF_Metadata:
    def __init__(self):
        self.camera_type = ""
        self.width = 0
        self.height = 0
        self.frames = 0
        self.binningx = 1
        self.binningy = 1
        self.exposure = 0.0
        self.delay = 0.0
        #self.adc_operation = 1
        self.ir_sensitivity = False
        self.px_rate = 0.0
        self.conversion_factor = 1.0 # e/count
    
    def copy(self):
        res = TIFF_Metadata()
        res.camera_type = self.camera_type
        res.width = self.width
        res.height = self.height
        res.frames = self.frames
        res.binningx = self.binningx
        res.binningy = self.binningy
        res.exposure = self.exposure
        res.delay = self.delay
        res.ir_sensitivity = self.ir_sensitivity
        res.px_rate = self.px_rate
        res.conversion_factor = self.conversion_factor
        return res
    
    def load_file(self, fn):
        return self

class TIFF_Stack:
    def __init__(self):
        self.metadata = TIFF_Metadata()
        self.data = np.zeros( (1,1,1) )
    
    def load_file(self, fn:str):
        self.data = skimage.io.imread( fn )
        self.metadata.frames, self.metadata.height, self.metadata.width = self.data.shape
        return self

class Calibration:
    def __init__(self):
        self.px_ref = 1.0
        self.lda_ref = 1.0
        self.px_err = 0.0
        self.lda_err = 0.0
    
    def __call__(self):
        return self.lda_ref/self.px_ref
    
    def px_to_lda(self, a:np.typing.ArrayLike=1):
        return (self.lda_ref/self.px_ref)*a
    
    def lda_to_px(self, a:np.typing.ArrayLike=1):
        return (self.px_ref/self.lda_ref)*a
    
    def to_dict(self):
        return { 'ldaref':self.lda_ref, 'pxref':self.px_ref, 'ldaerr':self.lda_err, 'pxerr':self.px_err }
    

"""
Abstraction Layer to hold the information on the data extracted from an image series with the slit in one specific position
"""
class SliceDataset:
    # Constructor
    def __init__(self):
        """ I know this isn't exactly necessary, but coming from C-style languages I prefer to have variables declared somewhere """
        
        # Image Data
        self.img_data_avg = np.zeros( (1,1) )
        self.img_data_std = np.zeros( (1,1) )
        self.img_mask = np.zeros( (1,1) )
        self.img_bg = np.zeros( (1,1) )
        
        # Metadata
        self.metadata = TIFF_Metadata()
        self.onslit_displacement = 0.0
        
        # R'sOI
        self.rois = []
        self.roi_mids = np.zeros( (1,1) )
        self.roi_devs = np.zeros( (1,1) )
        self.SLICE = PrimitiveImageROI()
        self.SMEAR = PrimitiveImageROI()
    
    # because I can't be fucked to type out "INTENSITY" every time
    def INSY(self, y:np.typing.ArrayLike):
        return 0.0
    
    def SPEC(self, y:np.typing.ArrayLike):
        return np.zeros( (1) )
    
    def LDA(self):
        return np.zeros( (1) )
    
    def load_image_data(self, tiff:TIFF_Stack):
        self.img_data_avg = np.mean( tiff.data, axis=0 ) / np.max(tiff.data)
        self.img_data_std = np.std( tiff.data, axis=0 ) / np.max(tiff.data)
        
        self.metadata = tiff.metadata.copy()
        #self.metadata.frames = 1
        
        # guess a constant background intensity from the top and bottom lines and subtract
        topline = np.copy( self.img_data_avg[0] )
        botline = np.copy( self.img_data_avg[-1] )
        #bg = np.empty_like( cumulative_img )
        #for y in range( cumulative_img.shape[0] ):
        #    #fac = y/(cumulative_img.shape[0]-1)
        #    fac=0.5
        #    bg[y] = fac*topline + (1-fac)*bottomline
        const_bg_guess = 0.5*(np.mean(topline)+np.mean(botline))
        self.img_data_avg -= const_bg_guess
        
        return self
    
    def gen_mask(self):
        # create a first mask: all points where the mean intensity is greater than sqrt2 times the standard deviation
        self.img_mask = np.where( self.img_data_avg > np.sqrt(2)*np.mean(self.img_data_avg, axis=None), 1, 0 )
        
        # now, find points among these that have enough neighbours to be unlikely to be due to noise
        NNEIGHBOURS = 3
        NITERATIONS = 2
        IDWEIGHT = 16 # must be >8
        kernel = np.array( [[ 1,    1    , 1 ],
                            [ 1, IDWEIGHT, 1 ],
                            [ 1,    1    , 1 ]] )
        for i in range(NITERATIONS):
            self.img_mask = np.where( scipy.signal.convolve2d(self.img_mask, kernel, mode='same')-IDWEIGHT >= NNEIGHBOURS, 1, 0 )
        
        return self
    
    def gen_rois(self):
        # project the mask onto the x- and y-axes
        xmask = np.where( np.sum(self.img_mask,axis=0)>2, 1, 0 )
        ymask = np.where( np.sum(self.img_mask,axis=1)>2, 1, 0 )
        
        # rising and falling edges
        xrising  =  np.clip( np.diff( xmask ),  0, 1 )
        xfalling = -np.clip( np.diff( xmask ), -1, 0 )
        yrising  =  np.clip( np.diff( ymask ),  0, 1 )
        yfalling = -np.clip( np.diff( ymask ), -1, 0 )
        
        # build R'sOI
        self.rois = []
        maskstate = False
        for x in range( xrising.shape[0] ):
            if not maskstate:
                if xrising[x] > 0.5:
                    xmin = x
                    maskstate = True
            else:
                if xfalling[x] > 0.5:
                    xmax = x+1
                    self.rois.append( PrimitiveImageROI( 
                            xmin=xmin, 
                            xmax=xmax, 
                            ymin=np.min( np.nonzero(yrising) ), 
                            ymax=np.max( np.nonzero(yfalling) ) 
                        ) 
                    )
                    maskstate = False
        
        # reject too narrow ROI's (probably only noise)
        ROI_MINIMUM_WIDTH = 4
        self.rois = [ roi for roi in self.rois if roi.width()>=ROI_MINIMUM_WIDTH ]
        
        return self
    
    def get_calibration(self):
        # instance calibration wrapper object
        calibration = Calibration()
        calibration.lda_ref = 532.0
        calibration.lda_err = 0.0
        
        # find line-wise mids for each ROI
        mids = np.zeros( (len(self.rois), self.rois[0].height()) )
        devs = np.zeros( (len(self.rois), self.rois[0].height()) )
        
        for i in range( len( self.rois ) ):
            X = np.arange(self.rois[i].width())
            for y in range( self.rois[0].height() ):
                norm      =          np.sum(            (self.rois[i](self.img_data_avg)[y]) )
                mids[i,y] =          np.sum(            (self.rois[i](self.img_data_avg)[y]/norm)*(X) )
                devs[i,y] = np.sqrt( np.sum( np.square( (self.rois[i](self.img_data_avg)[y]/norm)*(X-mids[i,y]) ) ) )
            #mids[i] /= norm
            #devs[i] /= norm
        
        """
        up to here, the result seem to be correct
        """
        
        # replace mids with too large of an uncertainty by the mean of the ones with sufficient confidence
        DEV_THRESHOLD = 4.0
        midweights = np.zeros( devs.shape )
        for i in range( len( self.rois ) ):
            midweights[i] = np.where( devs[i] <= DEV_THRESHOLD, 1.0, 0.0 )
            midweights[i] /= np.sum( midweights[i] )
        #print(midweights[1])
        meanmids = np.sum( mids*midweights, axis=1 )
        meandevs = np.sum( devs*midweights, axis=1 )
        #print(meanmids)
        #print(meandevs)
        for i in range( len( self.rois ) ):
            mids[i] = np.where( midweights[i]>0, mids[i], meanmids[i] )
            devs[i] = np.where( midweights[i]>0, devs[i], meandevs[i] )
        
        self.roi_mids = np.copy(mids)
        self.roi_devs = np.copy(devs)
        
        """
        There's something happening here...
        What it is ain't exactly clear...
        """
        
        # compute relative offsets (w/ errors), line-by-line and for each roi
        shift_ny = np.copy( mids[1:] )
        shiftdev_ny = np.copy( devs[1:] )
        for i in range( shift_ny.shape[0] ):
            shift_ny[i] -= mids[0]
            # adjust for different R'sOI
            shift_ny[i] += self.rois[i+1].xmin - self.rois[0].xmin
            # divide by degree of separation
            shift_ny[i] /= i+1
            
            # propagate error accordingly
            shiftdev_ny[i] += devs[0]
            shiftdev_ny[i] /= i+1
        
        # just a weighting function to assign weight n to the n-th order
        shiftweight_ny = np.zeros( shift_ny.shape )
        for i in np.arange(shift_ny.shape[0]):
            shiftweight_ny[i] += i+1
        
        # average over orders, result is only line-by-line
        shift_y = np.sum( shift_ny*shiftweight_ny, axis=0 ) / np.sum( shiftweight_ny, axis=0 )
        shiftdev_y = np.sum( shiftdev_ny*shiftweight_ny, axis=0 ) / np.sum( shiftweight_ny, axis=0 )
        
        # average over all lines (y-dimension) and write to calibration wrapper object
        calibration.px_ref = np.mean(shift_y)
        calibration.px_err = np.mean(shiftdev_y)
        
        return calibration


#class ImageDataset:
#    def __init__(self):


