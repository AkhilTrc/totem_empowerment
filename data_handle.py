import json

import numpy as np
import pandas as pd
import scipy.io
import helpers

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
        with open('data//gametrees//{}Elements.json'.format(version),
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

def get_combination_table(version='totem', csv=True):
    """Returns a combination table with four columns:
        (1) first: element index
        (2) second: element index
        (3) third: element index
        (4) success: 0 or 1
        (5) result: element index, if available

    Args:
        version (str, optional): 'totem'.
                    States what element and combination set is going to be used. 
        csv (bool, optional): True if csv version is to be returned, False for json file. Defaults to True.

    Returns:
        DataFrame or dict: Contains information about elements involved in combination.
    """
    if version == 'totem':
        if csv is True:
            combination_table = pd.read_csv('data/tables/{}CombinationTable.csv'.format(version),
                                dtype={'first': int, 'second': int, 'third': int, 'success': int, 'result': int})
        else:
            with open('data/tables/{}CombinationTable.json'.format(version),
                      encoding='utf8') as infile:
                combination_table = json.load(infile, object_hook=helpers.jsonKeys2int)
    else:
        raise ValueError('Undefined version: "{}". Use "totem" instead.'.format(version))

    return combination_table

def get_parent_table(version='totem'):
    """Returns a parent table where each parent has its own dict entry consisting of all resulting children.

    Args:
        version (str, optional): 'totem'.
                    States what element and combination set is going to be used. 

    Returns:
        dict: Parent table where each parent has its own dict entry consisting of all resulting children.
    """
    if version == 'totem':
        with open('data/tables/{}ParentTable.json'.format(version),
                  encoding='utf8') as infile:
            parent_table = json.load(infile)
            parent_table = {int(k):v for k,v in parent_table.items()}   # Key:value pair format?
    else:
        raise ValueError('Undefined version: "{}". Use "totem" instead.'.format(version))

    return parent_table

def get_custom_parent_table(game_version='totem', split_version='data', vector_version='crawl300'):
    """Returns a parent table where each parent has its own dict entry consisting of all resulting children.

    Args:
        game_version (str, optional): 'totem'.
                    States what element and combination set is going to be used. 
        split_version (str, optional): 'data' or 'element'. States what cross validation split the empowerment info should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the empowerment info should be based on.
                    Defaults to 'crawl300'.

    Returns:
        dict: Parent table where each parent has its own dict entry consisting of all resulting children.
    """
    if game_version == 'totem':
        with open('empowermentexploration/resources/customgametree/data/{}ChildrenEmpowermentTable-{}-{}.json'.format(game_version, split_version, vector_version),
                  encoding='utf8') as infile:
            parent_table = json.load(infile)
            parent_table = {int(k):v for k,v in parent_table.items()}
    else:
        raise ValueError('Undefined version: "{}". Use "totem" instead.'.format(game_version))

    return parent_table

def get_probability_table(game_version='totem', split_version='data', vector_version='crawl300'):
    """Returns probability table from custom gametree.

    Args:
        game_version (str, optional): 'totem'.
                    States what element and combination set is going to be used. 
        split_version (str, optional): 'data' or 'element'. States what cross validation split the table should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on.
                    Defaults to 'crawl300'.

    Returns:
        DataFrame: Probability table from custom gametree. Includes combination elements, true success and result,
                    predicted success and prediction for each element.
    """
    try:
        probability_table = pd.read_hdf('empowermentexploration/resources/customgametree/data/{}GametreeTable-{}-{}.h5'.format(game_version, split_version, vector_version))

        return probability_table
    except:
        raise ValueError('Corresponding custom gametree table not found. Check if input was correct or create the needed table using "empowermentexploration.gametree"')