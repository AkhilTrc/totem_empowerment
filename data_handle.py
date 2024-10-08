import json

import numpy as np
import pandas as pd
import scipy.io

def get_gametree(version='totem'):
    """Returns a (true) game tree depending on the version.

    Args:
        version (str, optional): 'totem'.
                    States what element and combination set is going to be used. 
    Returns:
        dict: Game tree information of the given version.
    """
    if version == 'totem':
        with open('data\\gametrees\\{}Gametree.json'.format(version),
                  encoding='utf8') as infile:
            gametree = json.load(infile)
            gametree = {int(k):v for k,v in gametree.items()}
    else:
        raise ValueError('Undefined version: "{}". Use "totem" instead.'.format(version))

    return gametree

def get_elements(version='totem'):
    """Returns elements for given version.

    Args:
        version (str, optional): 'totem'.
                    States what element and combination set is going to be used.

    Returns:
        list: Elements of the given version.
    """
    if version == 'totem':
        with open('data/{}Elements.json'.format(version),
                  encoding='utf8') as infile:
            elements = json.load(infile)
    else:
        raise ValueError('Undefined version: "{}". Use "totem" instead.'.format(version))

    return elements

def get_wordvectors(game_version='totem', vector_version='crawl300'):
    """Returns wordvectors for given version. 

    Args:
        game_version (str, optional): 'totem'.
                    States what element and combination set is going to be used.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on. Defaults to 'crawl300'.

    Returns:
        ndarray(dtype=float, ndim=2): Word vectors for elements of the given version.
    """
    if game_version == 'totem':
        if vector_version == 'ccen100' or vector_version == 'ccen300' or vector_version == 'crawl100' or vector_version == 'crawl300' or vector_version == 'wiki100' or vector_version == 'wiki300':
            vectors = np.loadtxt('data/vectors/{}ElementVectors-{}.txt'.format(game_version, vector_version))
        else:
            raise ValueError('Undefined vector_version: "{}". Use "ccen100", "ccen300", "crawl100", "crawl300", "wiki100" or "wiki300" instead.'.format(vector_version))
    else:
        raise ValueError('Undefined version: "{}". Use "totem"'.format(game_version))

    return vectors


"""
def get_parent_table():     # This comes in follow-up to custom gametree creations. 

def get_custom_parent_table():      # This also comes after custom game tree.
"""