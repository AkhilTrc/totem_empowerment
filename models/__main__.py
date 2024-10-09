import time
import argparse
import sys

import info_logs as log
from models.totem_model import TotemModel
from models.visualization import Visualization

if __name__ == '__main__':
    # YOUR ACTION IS REQUIRED HERE: SET APPROPRIATE VARIABLES
    # set game version: 'totem'
    
    parser = argparse.ArgumentParser(description='Reproduce the prediction')
    parser.add_argument('-g', '--game_version', required=True, dest='game_v', type=str,
                        help='Choose Desired Game Verison (totem)')
    
    parser.add_argument('-mo', '--model', required=True, dest='model', type=str,
                        help='Choose Desired Model type (emp, trueemp)')
    
    parser.add_argument('-t', '--temp', required=True,
                        dest='temp', type=float,
                        help='Choose Desired Temparature value.')        # defaults to temp = 1.0 or 0.1
    # Parse options
    args = parser.parse_args()
    
    if args.game_v is None:
        sys.exit('Input is missing!')

    if args.model is None:
        sys.exit('Model file is missing!')

    if args.temp is None:
        sys.exit('Output is not designated!')
    

    # game_version = 'totem'
    game_version = args.game_v

    # set list of models that are to be run: 'emp', 'trueemp'
    # models = ['emp']
    # models = ['trueemp']
    models = [args.model]

    # set value calculation
    # tuple contains first list of calculation info on trueemp, then emp.
    # each calculation info tuple in the list is ordered by (dynamic, local, outgoing_combinations)
    # set dynamic true for truebin oracle model, and false for normal bin on recreated gametree version
    value_calculation = ([(False,False,False)], [(None,None,False)], [(True,None,None)], [(False,None,None)])       
        # format: [(dynamic, local, outgoing_combinations)]
        # trueemp = [(False,False,False)]
        # emp = [(None,None,False)]

    # set list of temperatures that are to be run
    # temperatures = [0.1]
    temperatures = [args.temp]

    # set number of runs and steps
    runs = 100 # 1000
    steps = 200 #1000

    # set memory type: 0, 1, 2
    memory_type = 1     # memorize previous combinations 

    # set vector version the custom gameteee or word vectors are based on e.g. 'crawl300', 'ccen100
    # check if desired gametree and/or vectors are available
    vector_version = 'crawl300'
    split_version = 'data'
    # YOUR ACTION IS NOT RECQUIRED ANYMORE

    # create directory to log info from this run
    time = time.strftime('%Y%m%d-%H%M')
    log.create_directory('models/data/{}/'.format(time))

    # plot info for user
    print('\nRun models: {}. Save logs to directory models/data/{}/'.format(models, time))

    # write info on variables to file
    model = TotemModel(time, game_version=game_version, runs=runs, steps=steps, temperatures=temperatures, memory_type=memory_type,
                               models=models, value_calculation=value_calculation, vector_version=vector_version, split_version=split_version)
    log.log_model_info(model, mode=1, mode_type='{}TotemModel'.format(game_version), time=time)

    # run models
    for model_type in models:       # [trueemp and emp] for now. Might expand to [Orcale method] to perform comparisons. 
        print('\nRun model: {}.'.format(model_type))
        # run empowerment-like models
        if model_type in ['trueemp', 'emp']:
            # set list of empowerment calculations that are to be run for models ['trueemp', 'emp'].
            # (1) dynamic (2) local (3) outgoing combinations
            if model_type == 'trueemp':
                empowerment_calculation = value_calculation[0]  # [(False,False,False)]
            elif model_type == 'emp':       
                empowerment_calculation = value_calculation[1]  # [(None,None,False)]

            for e_c in empowerment_calculation:
                print('\nCalculation (dynamic, local, outgoing_combinations): {}.'.format(e_c))
                model = TotemModel(time, game_version=game_version, runs=runs, steps=steps, temperatures=temperatures, memory_type=memory_type,
                                           vector_version=vector_version, split_version=split_version)
                model.simulate_game(model_type, e_c)
        # run other models
        else:
            model = TotemModel(time, game_version=game_version, runs=runs, steps=steps, temperatures=temperatures, memory_type=memory_type,
                                       vector_version=vector_version, split_version=split_version)
            model.simulate_game(model_type)

    # initialize visualization
    visualization = Visualization(game_version, time, models, temperatures, runs, steps, memory_type)

    # plot gameprogress curves for comparison
    # visualization.plot_all(value_calculation, human=True)

    print('\nDone.')
