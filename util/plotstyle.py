
import matplotlib.pyplot as plt
from cycler import cycler

from enum import Flag, auto

import json

class Mode(Flag):
    DEFAULT = auto()
    DARK = auto()
    LIGHT = auto()
    PRINT = auto()

defaults_path = "persistent/plotstyles/"

# defaults
nonstandard_params = {
    "asymm_cmap":"jet",
    "symm_cmap":"twilight",
    "monochrome_cmap":"gist_heat",
    "binary_cmap":"binary_r",
    "width":12,
    "error_range_alpha":0.2
}


def monochrome_fg():
    return plt.rcParams['text.color']

def monochrome_bg():
    return plt.rcParams['axes.facecolor']

def figsize(aspect):
    WIDTH = nonstandard_params['width']
    HEIGHT = width/aspect
    return (WIDTH,HEIGHT)

def err_alpha():
    return nonstandard_params['error_range_alpha']

def c(idx):
    #return plt.rcParams['axes.prop_cycle'][idx]['color']
    return plt.rcParams['axes.prop_cycle'].by_key()['color'][idx]


def style_filename(mode):
    if mode == Mode.DARK:
        return "darkmode.json"
    elif mode == Mode.LIGHT:
        return "lightmode.json"
    elif mode == Mode.PRINT:
        return "printmode.json"
    else:
        return "matplotlib_default.json"

def cmap(datatype=''):
    if datatype in [ 'a', 'asymm', 'asymmetric' ]:
        return nonstandard_params['asymm_cmap']
    if datatype in [ 'b', 'bin', 'binary' ]:
        return nonstandard_params['binary_cmap']
    elif datatype in [ 's', 'symm', 'symmetric' ]:
        return nonstandard_params['symm_cmap']
    elif datatype in [ 'm', 'mono', 'monochrome' ]:
        return nonstandard_params['monochrome_cmap']
    else:
        return plt.rcParams['image.cmap']


def objectify_cycler(cycler):
    arr = []
    for entry in cycler:
        arr.append( entry )
    return arr


def objectify_rcparams(params):
    obj = {}
    for key in params:
        obj[key] = params[key]
    
    if 'axes.prop_cycle' in obj:
        obj['axes.prop_cycle'] = objectify_cycler( obj['axes.prop_cycle'] )
    
    return obj


def reconstruct_cycler(arr):
    if len(arr)>0:
        obj = {}
        for key in arr[0]:
            keyarr = []
            for entry in arr:
                keyarr.append(entry[key])
            obj[key] = keyarr
        
        cyclers = [ cycler( key, obj[key] ) for key in obj ]
        res = cyclers[0]
        if len(cyclers) > 1:
            for c in cyclers[1:]:
                res = res + c
        return res
    
    else:
        # something must have gone wrong if this happens
        return False


def reconstruct_rcparams(obj):
    if 'axes.prop_cycle' in obj:
        prop_cycle = reconstruct_cycler( obj['axes.prop_cycle'] )
        obj.pop('axes.prop_cycle')
    else: 
        prop_cycle = False
    if 'nonstandard_params' in obj:
        global nonstandard_params
        for key in obj['nonstandard_params']:
            nonstandard_params[key] = obj['nonstandard_params'][key]
        obj.pop('nonstandard_params')
    return obj, prop_cycle


def load( style ):
    fn = defaults_path + style + ".json"
    try:
        inputfile = open( fn, 'r' )
    except FileNotFoundError:
        return False
    
    obj = json.loads( inputfile.read() )
    inputfile.close()
    params, cycler = reconstruct_rcparams( obj )
    
    plt.rcParams.update( params )
    if cycler:
        plt.rc('axes', prop_cycle=cycler)
    
    return True
