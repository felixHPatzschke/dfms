
# For math things
import numpy as np
from numpy import pi as pi

import matplotlib.pyplot as plt
#%matplotlib inline

from util import plotstyle



class Drawable:
    def __init__(self):
        self._X = np.array([0.0])
        self._Y = np.array([0.0])
        
        self.xsc = 1.0
        self.ysc = 1.0
        
        self.xtr = 0.0
        self.ytr = 0.0
        
        self.rot = 0.0
        
        self.preferred_colour = plotstyle.monochrome_fg()
        self.preferred_linestyle = '-'
        self.preferred_linewidth = 2
    
    def scale(self, *args):
        if len(args)==1:
            self.xsc *= args[0]
            self.ysc *= args[0]
        elif len(args)==2:
            self.xsc *= args[0]
            self.ysc *= args[1]
        # TODO: handle invalid input
        return self
        
    def translate(self, x, y):
        self.xtr += x
        self.ytr += y
        return self
    
    def rotate(self, angle):
        self.rot += angle
        return self
    
    def set_attrib(self, **kwargs):
        for key,val in kwargs.items():
            if key in [ 'c', 'col', 'color', 'colour' ]:
                self.preferred_colour = val
            elif key in [ 'ls', 'linestyle' ]:
                self.preferred_linestyle = val
            elif key in [ 'lw', 'linewidth' ]:
                self.preferred_linewidth = val 
        return self
        
    def X(self):
        return ( np.cos(self.rot)*self.xsc*self._X 
                -np.sin(self.rot)*self.ysc*self._Y + self.xtr )
    
    def Y(self):
        return ( np.sin(self.rot)*self.xsc*self._X 
                +np.cos(self.rot)*self.ysc*self._Y + self.ytr )
    
    def draw(self, axes, **kwargs):
        colour = self.preferred_colour
        linestyle = self.preferred_linestyle
        linewidth = self.preferred_linewidth
        for key,val in kwargs.items():
            if key in [ 'c', 'col', 'color', 'colour' ]:
                colour = val
            elif key in [ 'ls', 'linestyle' ]:
                linestyle = val
            elif key in [ 'lw', 'linewidth' ]:
                linewidth = val 
        axes.plot( self.X(), self.Y(), c=colour, ls=linestyle, lw=linewidth )
        
    def label(self, axes, text, anchor='left', **kwargs):
        colour = self.preferred_colour
        margin = 0.3
        #linestyle = self.preferred_linestyle
        #linewidth = self.preferred_linewidth
        for key,val in kwargs.items():
            if key in [ 'c', 'col', 'color', 'colour' ]:
                colour = val
            if key in [ 'm', 'margin' ]:
                margin = val
            #elif key in [ 'ls', 'linestyle' ]:
            #    linestyle = val
            #elif key in [ 'lw', 'linewidth' ]:
            #    linewidth = val 
        
        #X = self._X
        #Y = self._Y
        X = self.X()
        Y = self.Y()
        
        if anchor in [ 'l', 'left' ]:
            vert_align = 'center'
            hor_align = 'right'
            #pt = np.argmin(X)
            #shift = [ -0.3, 0.0 ]
            x=np.min(X)-margin
            y=np.mean(Y)
            
        elif anchor in [ 'r', 'right' ]:
            vert_align = 'center'
            hor_align = 'left'
            #pt = np.argmax(X)
            #shift = [ 0.3, 0.0 ]
            x=np.max(X)+margin
            y=np.mean(Y)

        elif anchor in [ 't', 'top' ]:
            vert_align = 'bottom'
            hor_align = 'center'
            #pt = np.argmax(Y)
            #shift = [ 0.0, 0.3 ]
            x=np.mean(X)
            y=np.max(Y)+margin
        
        elif anchor in [ 'b', 'bottom' ]:
            vert_align = 'top'
            hor_align = 'center'
            #pt = np.argmin(Y)
            #shift = [ 0.0, -0.3 ]
            
            x=np.mean(X)
            y=np.min(Y)-margin
            
        #x = ( np.cos(self.rot)*self.xsc*self._X[pt] 
        #     -np.sin(self.rot)*self.ysc*self._Y[pt] + self.xtr + shift[0] )
        #y = ( np.sin(self.rot)*self.xsc*self._X[pt] 
        #     +np.cos(self.rot)*self.ysc*self._Y[pt] + self.ytr + shift[1] )
        #x = X[pt] + shift[0]
        #y = Y[pt] + shift[1]
        
        axes.text( x, y, text, va=vert_align, ha=hor_align, c=colour )

class Curve(Drawable):
    def __init__(self):
        super().__init__()
        
        self._X = np.array( [0, 1] )
        self._Y = np.array( [0, 1] )
        
    def set_XY(self, X, Y):
        self._X = X
        self._Y = Y
        return self
    
    # TODO arbitrary coordinate transformations
        
class Polygon(Drawable):
    def __init__(self, n=3):
        super().__init__()
        
        self._X = np.sin( np.linspace( -pi, pi, n, endpoint=False) )
        self._Y = np.cos( np.linspace( -pi, pi, n, endpoint=False) )
        
class Box(Drawable):
    def __init__(self):
        super().__init__()
        
        self._X = np.array( [  1, -1, -1,  1,  1 ] )
        self._Y = np.array( [  1,  1, -1, -1,  1 ] )
        
class Plane(Drawable):
    def __init__(self):
        super().__init__()
        
        self._X = np.array( [-1.0, +1.0] )
        self._Y = np.array( [0.0, 0.0] )
    
    # TODO: remove this
    def __call__(self, x):
        return np.tan( self.rot )*(x-self.xtr)+self.ytr
    
    def y(self, x):
        return np.tan( self.rot )*(x-self.xtr)+self.ytr
    
    def x(self, y):
        return np.cot( self.rot )*(y-self.ytr)+self.xtr
        
class Grating(Plane):
    def __init__(self):
        super().__init__()
        
        self.preferred_linestyle = ':'
        #self.preferred_linewidth = 4
        
class Lens(Plane):
    def __init__(self, ctop=1.0, cbottom=1.0):
        super().__init__()
        
        X1 = np.linspace( -1, +1, 399, endpoint=False )
        X2 = np.linspace( +1, -1, 400, endpoint=True  )
        Y1 = np.square(X1)*(-1)+1
        Y2 = np.square(X2)*(+1)-1
        Y1 *= ctop
        Y2 *= cbottom
        self._X = np.append( X1, X2 )
        self._Y = np.append( Y1, Y2 )
        
    #def light_cone_X(self, f, theta, side=1):
    #    X = np.linspace( -f*np.tan(theta), f*np.tan(theta), 400 )
    #    Y = -1.0/np.tan(theta)*np.abs(X) + f
    #    Y *= side
    #    return ( np.cos(self.rot)*X 
    #            -np.sin(self.rot)*Y + self.xtr )

    #def light_cone_Y(self, f, theta, side=1):
    #    X = np.linspace( -f*np.tan(theta), f*np.tan(theta), 400 )
    #    Y = -1.0/np.tan(theta)*np.abs(X) + f
    #    Y *= side
    #    return ( np.sin(self.rot)*X 
    #            +np.cos(self.rot)*Y + self.ytr )
    
    def light_cone( self, f, theta, side=0 ):
        poly = Polygon(3)
        poly._X = np.array( [ -1, 0, 1] )
        poly._Y = np.array( [ 0, 1, 0] )
        poly.scale( f*np.tan(theta), f ).translate(self.xtr, self.ytr)
        if side%2 != 0:
            poly.rotate(pi)
        poly.set_attrib(ls=':')
        return poly
    
class Mirror(Plane):
    def __init__(self):
        super().__init__()
        
        X1 = np.array( [-1,+1] )
        Y1 = np.array( [0,0] )
        
        density = 15
        
        x = np.linspace( -1.0+1.0/density, 1.0-1.0/density, 2*density )
        X2 = np.empty( 3*x.size, dtype=x.dtype )
        X2[0::3] = x
        X2[1::3] = x
        X2[2::3] = x
        Y2 = np.zeros( 3*x.size )
        Y2[1::3] -= 1.0/density
        
        self._X = np.append( X1, X2 )
        self._Y = np.append( Y1, Y2 )
        
class Sensor(Plane):
    def __init__(self):
        super().__init__()
        
        X1 = np.array( [-1,+1] )
        Y1 = np.array( [0,0] )
        
        density = 10
        
        x = np.linspace( -1.0+1.0/density, 1.0-1.0/density, 2*density )
        X2 = np.empty( 3*x.size, dtype=x.dtype )
        X2[0::3] = x+0.333/density
        X2[1::3] = x-0.333/density
        X2[2::3] = x+0.333/density
        Y2 = np.zeros( 3*x.size )
        Y2[1::3] -= 0.666/density
        
        self._X = np.append( X1, X2 )
        self._Y = np.append( Y1, Y2 )        
        
        
class Slit(Plane):
    def __init__(self, width=0.25):
        super().__init__()
        
        X1 = np.array( [-1, -width, -width, -width] )
        X2 = np.array( [ 1,  width,  width,  width] )
        Y1 = np.array( [ 0, 0, -1, 1 ] )
        Y2 = np.array( [ 0, 0, -1, 1 ] )
        self._X = np.append( X1, X2 )
        self._Y = np.append( Y1, Y2 )
        
    def draw(self, axes, **kwargs):
        colour = self.preferred_colour
        linestyle = self.preferred_linestyle
        linewidth = self.preferred_linewidth
        for key,val in kwargs.items():
            if key in [ 'c', 'col', 'color', 'colour' ]:
                colour = val
            elif key in [ 'ls', 'linestyle' ]:
                linestyle = val
            elif key in [ 'lw', 'linewidth' ]:
                linewidth = val 
        X = self.X()
        Y = self.Y()
        axes.plot( X[:4], Y[:4], c=colour, ls=linestyle, lw=linewidth )
        axes.plot( X[4:], Y[4:], c=colour, ls=linestyle, lw=linewidth )
        
        
def path_between( p1:Plane, p2:Plane, r1, r2, side ):
    if side%2 == 0:
        sm = 1
    else:
        sm = -1
        
    #dx = p2.xtr-p1.xtr
    #dy = p2.ytr-p1.ytr
    #norm = np.sqrt( dx*dx + dy*dy )
    #dx /= norm
    #dy /= norm
    
    #dotproduct1 = dy*np.cos(p1.rot) - dx*np.sin(p1.rot)
    #dotproduct2 = -dy*np.cos(p2.rot) + dx*np.sin(p2.rot)

    #r1 *= np.sin(np.arccos(dotproduct1))
    #r2 *= np.sin(np.arccos(dotproduct2))
    
    res = Curve()
    res.set_XY( 
        np.array( [ p1.xtr + sm*r1*np.cos(p1.rot) , p2.xtr + sm*r2*np.cos(p2.rot) ] ),
        np.array( [ p1.ytr + sm*r1*np.sin(p1.rot) , p2.ytr + sm*r2*np.sin(p2.rot) ] )
    )
    return res
    



