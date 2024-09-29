import json

import numpy as np
import pandas as pd
import scipy.io

def get_gametree(version='alchemy2'):
    """Returns a (true) game tree depending on the version.

    Args:
        version (str, optional): 'totem_game'.
                    States what element and combination set is going to be used. 
    Returns:
        dict: Game tree information of the given version.
    """
    if version == 'totem_game':
        with open('data/{}Gametree.json'.format(version),
                  encoding='utf8') as infile:
            gametree = json.load(infile)
            gametree = {int(k):v for k,v in gametree.items()}
    else:
        raise ValueError('Undefined version: "{}". Use "totem_game" instead.'.format(version))

    return gametree

def get_elements(version='totem_game'):
    """Returns elements for given version.

    Args:
        version (str, optional): 'totem_game'.
                    States what element and combination set is going to be used.

    Returns:
        list: Elements of the given version.
    """
    if version == 'totem_game':
        with open('data/{}Elements.json'.format(version),
                  encoding='utf8') as infile:
            elements = json.load(infile)
    else:
        raise ValueError('Undefined version: "{}". Use "totem_game" instead.'.format(version))

    return elements