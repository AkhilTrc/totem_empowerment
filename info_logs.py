import csv
import json
import os

import numpy as np
import pandas as pd
import scipy.io


def create_directory(directory_name):
    """Creates directory if it was not existent before.

    Args:
        directory_name (str): Directory path.
    """
    os.makedirs(os.path.dirname(directory_name), exist_ok=True)

def create_gametreetable_file(time=None, prediction_model=0, n_elements=None, game_version='totem', split_version='data', vector_version='crawl300'):
    """Creates file for later result logging depending on model type (link or element prediction model).

    Args:
        time (str, optional): Timestamp. Defaults to None.
        link_prediction (bool, optional): States for what model the data is generated,
                    True = link prediction model, False = element prediction model.
                    Defaults to True.
        n_elements (int, optional): Number of elements used in the game. Is only of interest if link_prediction is False.
                    Defaults to None.
        game_version (str, optional): 'totem'. States what element and combination set the table should be based on.
        split_version (str, optional): 'data' or 'element'. States what cross validation split the table should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on.
                    Defaults to 'crawl300'.
    """
    if prediction_model == 0:
        append_gametreetable_file(['first', 'second', 'third', 'trueSuccess', 'trueResult', 'predSuccess'], time=time, prediction_model=prediction_model, first_line=True, game_version=game_version, split_version=split_version, vector_version=vector_version)
        # change this to include 3 combinable elements.
    elif prediction_model == 1:
        first_line = ['first', 'second', 'third', 'trueSuccess', 'trueResult']       # change this to include 3 combinable elements.
        for element_idx in range(n_elements):
            first_line.append(str(element_idx))
        append_gametreetable_file(first_line, time=time, prediction_model=prediction_model, first_line=True, game_version=game_version, split_version=split_version, vector_version=vector_version)
    else:
        append_gametreetable_file(['first', 'second', 'third', 'trueSuccess', 'trueResult', 'predEmp'], time=time, prediction_model=prediction_model, first_line=True, game_version=game_version, split_version=split_version, vector_version=vector_version)


def create_empowermenttable_file(game_version='totem', split_version='data', vector_version='crawl300'):
    """Creates file for later result logging of empowerment table.

    Args:
        game_version (str, optional): 'totem'. States what element and combination set the table should be based on.
        split_version (str, optional): 'data' or 'element'. States what cross validation split the table should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on.
                    Defaults to 'crawl300'.
    """
    append_empowermenttable_file(['first', 'second', 'third', 'predResult', 'empComb', 'empChild', 'binComb', 'binChild'], first_line=True, game_version=game_version, split_version=split_version, vector_version=vector_version)

def append_gametreetable_file(*data, time=None, prediction_model=0, first_line=False, game_version='totem', split_version='data', vector_version='crawl300'):
    """Writes test results to csv file continuously.

    Args:
        data (tuple): Tuple made of either a list (str) or two numpy arrays (ndarray(dtype=float, ndim=2))
                    where each row consists of elements involved in combination, true success and true results
                    and predicted success probability or element probabilities.
        time (str, optional): Timestamp. Defaults to None.
        link_prediction (bool, optional): States for what model the data is logged,
                    True = link prediction model, False = element prediction model.
                    Defaults to True.
        first_line (bool, optional): Indicates whether first line of file is written. Defaults to False.
        game_version (str, optional): 'totem'. States what element and combination set the table should be based on.
        split_version (str, optional): 'data' or 'element'. States what cross validation split the table should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on.
                    Defaults to 'crawl300'.
    """
    # write first line
    if first_line is False:
        if len(data) == 1:
            data_new = np.concatenate((data[0]), axis=1)
        elif len(data) == 2:
            data_new = np.concatenate((data[0], data[1]), axis=1)
        elif len(data) == 3:
            data_new = np.concatenate((data[0], data[1], data[2]), axis=1)
    else:
        data_new = data

    # append data
    for line in data_new:
        if prediction_model == 0:
            with open('gametree/data/{}/{}LinkPredTable-{}-{}.csv'.format(time, game_version, split_version, vector_version), 'a+', newline='') as outfile:
                # = '/235545/tinyalchemyLinkPredTable-data-crawl300.csv' for this example. 
                writer = csv.writer(outfile)
                writer.writerow(line)
        elif prediction_model == 1:
            with open('gametree/data/{}/{}ElemPredTable-{}-{}.csv'.format(time, game_version, split_version, vector_version), 'a+', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(line)
        else:
            with open('gametree/data/{}/{}EmpPredTable-{}-{}.csv'.format(time, game_version, split_version, vector_version), 'a+', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerow(line)

def append_empowermenttable_file(*data, first_line=False, game_version='totem', split_version='data', vector_version='crawl300'):
    """Writes test results to csv file continuously.

    Args:
        data (tuple): Tuple made of either a list (str) or two numpy arrays (ndarray(dtype=float, ndim=2))
                    where each row consists of elements involved in combination, true success and true results
                    and predicted success probability or element probabilities.
        first_line (Boolean, optional): Indicates whether first line of file is written. Defaults to False.
        game_version (str, optional): 'totem'. States what element and combination set the table should be based on.
                    Defaults to 'alchemy2'.
        split_version (str, optional): 'data' or 'element'. States what cross validation split the table should be based on.
                    Defaults to 'data'.
        vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                    States what element vectors the table should be based on.
                    Defaults to 'crawl300'.
    """
    # write first line
    if first_line is True:
        data_new = data
    else:
        data_new = data[0]

    # append data
    for line in data_new:
        with open('customgametree/data/{}EmpowermentTable-{}-{}.csv'.format(game_version, split_version, vector_version), 'a+', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(line)

def log_model_info(model_info, mode, mode_type, time):
    """Log info on model to file.

    Args:
        model_info (TotemModel, HumanModel or CrossValidation): Model that is to be logged.
        mode (int): 1 = model, 2 = human, 3 = gametree
        mode_type (str): States for what model the data is logged.
                    (1) mode 1 - 'emp', 'truebin', 'trueemp'
                    (2) mode 2 - 'emp', 'truebin', 'trueemp'
                    (3) mode 3 - 'linkPred' or 'elemPred'
        time (str): Timestamp.
    """
    if mode == 1:
        filename = 'models/data/{}/{}ModelInfo.txt'.format(time, mode_type)
    elif mode == 2:
        filename = 'gametree/data/human/{}/{}ModelInfo.txt'.format(time, mode_type)
        model_info.data = {}
    elif mode == 3:
        filename = 'gametree/data/{}/{}ModelInfo.txt'.format(time, mode_type)    # = '/2387532/tinyalchemyLinkPredModelInfo.txt' for this example. 

    # convert object information to dictionary
    model_dictionary = model_info.__dict__      # converts the CrossValidation object into dictionary. For the game tree in this case. 

    with open(filename, 'w') as f:
        json.dump(model_dictionary, f, indent=4, sort_keys=True)     # Stores all the parameter values of the model in json format. 

def store_inventory(game_version, inventory, time, model_type, memory, empowerment_calculation=None):
    """Writes inventory sizes for each temperature, run and step to mat file.

    Args:
        game_version (str): 'totem'. States what element and combination set the table should be based on.
        inventory: (Inventory): Inventory info.
        time (str): Timestamp.
        model_type (str): Model type.
        memory (int): States whether it should be memorized what combinations have been used before. There are different options
                    (1) 0 = no memory
                    (2) 1 = memory
                    (3) 2 = fading memory (delete random previous combination every 5 steps)
        empowerment_calculation (tuple, optional): Tuple made of three entries. Defaults to None.
                    - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                    - local (bool): Whether calculation of empowerment is done locally or globally.
                    - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations
                                or length of set of resulting elements.

    """
    if model_type in ['emp', 'trueemp']:
        filename = 'models/data/{}/{}-{}-{}-memory{}-inventory.mat'.format(time, game_version, model_type, empowerment_calculation, memory)
    else:
        filename = 'models/data/{}/{}-{}-memory{}-inventory.mat'.format(time, game_version, model_type, memory)
    scipy.io.savemat(filename, mdict={'out': inventory.inventory_size_over_time}, oned_as='row')

    # convert to dataframe
    combinations = pd.DataFrame(inventory.combination_storage)
    if model_type in ['emp', 'trueemp']:
        filename = 'models/data/{}/{}{}Combinations-{}-memory{}.csv'.format(time, game_version, model_type.capitalize(), empowerment_calculation, memory)
    else:
        filename = 'models/data/{}/{}{}Combinations-memory{}.csv'.format(time, game_version, model_type.capitalize(), memory)
    combinations.to_csv(filename, index=False)

def store_utility(utilities, time, game_version, data_source, model_type, memory, empowerment_calculation=None, subset_type=None, sru_success=False):
    """Writes player utilities to csv file.

    Args:
        utilities (DataFrame): Player utility values.
        time (str): Timestamp.
        game_version (str): 'totem'.
                    States what game version the data is based on.
        data_source (str, optional): States what kind of model is going to be used as data source:
                    'human', 'base', 'bin', 'emp', 'truebin', 'trueemp', 'sim', 'cbu', 'cbv'.
                    Defaults to 'human'.
        model_type (str): Model type.
        memory (int): States whether it should be memorized what combinations have been used before. There are different options
                    (1) 0 = no memory
                    (2) 1 = memory
                    (3) 2 = fading memory (delete random previous combination every 5 steps)
        empowerment_calculation (tuple, optional): Tuple made of three entries. Defaults to None.
                    - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                    - local (bool): Whether calculation of empowerment is done locally or globally.
                    - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations
                                or length of set of resulting elements.
        subset_type (str, optional): Player subset can either be 'max', 'min' or 'rand'
                    Defaults to 'max'.
        sru_success (boolean, optional): True if utilities of only successful combinations are considered.
                    Of interest only for trueemp and truebin models. Defaults to False.
j
    """
    if subset_type is not None:
        subset_type = '-{}'.format(subset_type)
    else:
        subset_type = ''

    if sru_success is not False:
        sru_success = '-successfulonly'
    else:
        sru_success = ''
    if model_type in ['emp', 'trueemp']:
        empowerment_calculation = '-{}'.format(empowerment_calculation)
    else:
        empowerment_calculation = ''
    filename = 'data/human/{}/{}{}Utility-{}{}-memory{}{}{}.csv'.format(time, game_version, model_type.capitalize(), data_source,
                                                                                                 empowerment_calculation, memory, subset_type,
                                                                                                 sru_success)
    utilities.to_csv(filename, index=False)

def store_regression_data(data, time, z_score, model_type, memory_type, game_version):
    """Writes player utilities for later regression to csv file.

    Args:
        data (DataFrame): Data holding information on (1) player id, (2) decision between two arms,
                    (3)-(6) differences for values of model strategies
        time (str): Timestamp.
        z_score (boolean): True if z score for model differences should be caculated, False otherwise.
        model_type (str): Model type, which is either 'human' or any selection from 'base', 'emp', 'bin', 'trueemp',
                    'truebin', 'cbv', 'sim' or 'cbu' if data is generated for simulated data.
        memory_type (int): Memory type that was used for data generation. There are different options
                    (1) 0 = no memory
                    (2) 1 = memory
                    (3) 2 = fading memory (delete random previous combination every 10 steps)
        game_version (str): 'totem'.
                        States what player data set is going to be used.
    """
    if z_score is True:
        z_score = '-scaled'
    else:
        z_score = ''
    filename = 'data/regression/{}-{}-valuedifferences-{}{}-{}.csv'.format(time, game_version, model_type, z_score, memory_type)
    data.to_csv(filename, index=False)
