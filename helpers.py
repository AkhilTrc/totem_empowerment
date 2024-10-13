import random
import numpy as np
from sklearn import preprocessing
import warnings
import scipy.special
from scipy import stats


def softmax(values, temperature=1):
    """Applies softmax on a given list considering a temperature value. Softmax is applied row-wise if list is 2D.

    Args:
        x (ndarray(dtype=float, ndim=2) or dict_values): Array with values. Can be 1D or 2D.
        temperature (float, optional): Temperature that is applied to softmax.
                    A temperature > 1 produces a softer probability distribution and < 1 a probability distribution twords argmax.
                    Defaults to 1.

    Returns:
        ndarray(dtype=float, ndim=2): Probabilities row-wise.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        
        if not isinstance(x, np.ndarray):
            x = list(x)
            x = np.array(x)
        
        if x.ndim == 2:
            x = preprocessing.scale(x, axis=1)
            x_temperature = x/temperature
            probabilities = scipy.special.softmax(x_temperature, axis=1)
        if x.ndim == 3:
            x = preprocessing.scale(x, axis=2)
            x_temperature = x/temperature
            probabilities = scipy.special.softmax(x_temperature, axis=2)
        else:
            x = preprocessing.scale(x)
            x_temperature = x/temperature
            probabilities = scipy.special.softmax(x_temperature)

        return probabilities
    
def jsonKeys2int(x):
    """Casts str keys to int.

    Args:
        x (dict): Dictionary with str keys.

    Returns:
        dict: Dictionary with int keys.
    """
    if isinstance(x, dict):
        return {int(k):v for k,v in x.items()}      # Need to change to int(value or '0')

    return x

def split_numbers(n_elements, split):
    """Splits elements into groups of (nearly) equal size.

    Args:
        n_elements (int): Number of elements that have to be split.
        n_splits (int): Number of splits.

    Returns:
        (ndarray(dtype=int, ndim=2)): Array that contains multiple sub-arrays of (nearly) equal size filled with element indices.
    """
    x = np.arange(n_elements)   # Generates the index values. 
    random.shuffle(x)   # List of randomly shuffled index values. 

    return np.array_split(x, split)

def softmax(x, temperature=1):
    """Applies softmax on a given list considering a temperature value. Softmax is applied row-wise if list is 2D.

    Args:
        x (ndarray(dtype=float, ndim=2) or dict_values): Array with values. Can be 1D or 2D.
        temperature (float, optional): Temperature that is applied to softmax.
                    A temperature > 1 produces a softer probability distribution and < 1 a probability distribution twords argmax.
                    Defaults to 1.

    Returns:
        ndarray(dtype=float, ndim=2): Probabilities row-wise.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if not isinstance(x, np.ndarray):
            x = list(x)
            x = np.array(x)

        if x != ():
            if x.ndim == 2:
                x = preprocessing.scale(x, axis=1)
                x_temperature = x/temperature
                probabilities = scipy.special.softmax(x_temperature, axis=1)
            else:
                x = preprocessing.scale(x)
                x_temperature = x/temperature
                probabilities = scipy.special.softmax(x_temperature)

            return probabilities
    
def adjust_lightness(color, amount=0.5):
    """Function to lighten or darken given color by multiplying (1-luminosity) by the given amount.
                Taken from https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib

    Args:
        color (str): Color can be matplotlib color string, hex string, or RGB tuple.
        amount (float, optional): If smaller than 1, color will be darker. If higher than 1, color will be lighter.
                Defaults to 0.5.

    Returns:
        tuple: Color RGB tuple.
    """
    import colorsys

    import matplotlib.colors as mc
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

def translate_model(model_type):
    """Maps model shortcut to full name.

    Args:
        model_type (str): Model shortcut.

    Returns:
        str: Model full name.
    """
    if model_type == 'emp':
        model = 'empowerment (approx.)'
    elif model_type == 'trueemp':
        model = 'empowerment'
    else:
        raise ValueError('Undefined model version: "{}". Use "emp" or "trueemp" instead.'.format(model_type))

    return model