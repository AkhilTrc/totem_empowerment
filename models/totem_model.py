import data_handle as data_handle
import info_logs as log
from models.emp_model import EmpModel
from models.inventory import Inventory
from models.trueemp_model import TrueEmpModel
from models.visualization import Visualization

class TotemModel():
    """Model that plays the game Totem.
    """
    def __init__(self, time, game_version='totem', runs=100, steps=1000, temperatures=[1.0], memory_type=0,
                 models=None, value_calculation=None,
                 vector_version='crawl300', split_version='data'):
        """Initializes a little Totem game model.           

        Args:
            time (str): Timestamp. This will be used for logs.
            game_version (str, optional): 'totem'. States what element and combination set is going to be used.
            runs (int, optional): Number of simulations. Defaults to 100.
            steps (int, optional): Number of steps for each simulation. Defaults to 1000.    For CrossValidation?
            temperatures (list): List of temperatures (float) that are used to compute probabilities.
                        There will be one complete run for each temperature. Defaults to [1.0]. Can  also change to 0.1
                        High temparature might help increase diversity and creativity in softmax output probablity distribution. 
            memory_type (int, optional): States whether it should be memorized what combinations have been used before.
                        (1) 0 = no memory
                        (2) 1 = memory
                        (3) 2 = fading memory (delete random previous combination every 5 steps)
                        Defaults to 0.
            models (list, optional): List of models that are to be run. Defaults to None.
            value_calculation (tuple, optional): Tuple of value calculation Tuple contains first calculation info on trueemp, then emp.
                        Defaults to None.
            vector_version (str, optional): 'ccen100', 'ccen300', 'crawl100', 'crawl300', 'wiki100' or 'wiki300'.
                        States what element vectors the empowerment info should be based on.
                        Defaults to 'crawl300'.
            split_version (str, optional): 'data' or 'element'. States what cross validation split the empowerment info should be based on.
                        Defaults to 'data'.
        """
        # print info for user
        print('\nInitialize totem model based on gametree {}.'.format(game_version))

        # set general info
        self.time = time
        self.game_version = game_version
        self.runs = runs
        self.steps = steps
        self.temperatures = temperatures
        self.memory_type = memory_type
        self.models = models
        self.value_calculation = value_calculation
        self.vector_version = vector_version
        self.split_version = split_version

        # load info table
        self.combination_table = data_handle.get_combination_table(game_version, csv=False)

    def simulate_game(self, model_type, empowerment_calculation=(True,True,False)):
        """Simulates game.

        Args:
            model_type (str): model_version (str, optional): States what kind of model is going to be used.
                        (1) 'trueemp' = empowerment model based on the true game tree
                        (2) 'emp' = empowerment model based on the self-constructed game tree
            empowerment_calculation (tuple, optional): Tuple made of three entries. Defaults to (True,True,False).
                        - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                        - local (bool): Whether calculation of empowerment is done locally or globally.
                        - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations
                                    or length of set of resulting elements.
        """
        # print info for user
        print('\nStart game for using model {} on gametree {}, memory={}.'.format(model_type, self.game_version, self.memory_type))

        # initialize model specific info
        model = self.initialize_model(model_type, empowerment_calculation)            

        # initialize visualization
        visualization = Visualization(self.game_version, self.time, model_type, self.temperatures, self.runs, self.steps, self.memory_type, empowerment_calculation)

        # initialize inventory
        inventory = Inventory(self.game_version, len(self.temperatures), self.runs, self.steps)

        for temperature_idx, temperature_value in enumerate(self.temperatures):
            print('\nRun {} simulations for temperature value {}.'.format(self.runs, temperature_value))

            for run in range(self.runs):

                # reset inventories: one only holds usable elements and no final elements, the other one tracks all elements
                inventory.reset()

                # reset model specific info
                model.reset()                       

                for step in range(self.steps):
                    print("Step {}: ".format(step))
                    combination = model.choose_combination(temperature_value, (step==0 or self.memory_type == 1 or self.memory_type == 2 or len(results[0]) != 0))
                    # if combination is not None:
                    results = inventory.update(combination, temperature_idx, run, step)
                    model.update_model_specifics(combination, results, inventory, step)

            # visualization of inventory sizes
            visualization.plot_inventory_sizes(inventory, temperature_idx)

        # visualization of training progress
        visualization.plot_gameprogress(inventory)

        # store inventory data
        log.store_inventory(self.game_version, inventory, self.time, model_type, self.memory_type, empowerment_calculation)
  
    def initialize_model(self, model_type, empowerment_calculation):
        """Return model instance depending on what version is requested.

        Args:
            model_version (str, optional): States what kind of model is going to be used.
                        (1) 'trueemp' = empowerment model based on the true game tree
                        (2) 'emp' = empowerment model based on the self-constructed game tree
            empowerment_calculation (tuple): Tuple made of three entries.
                        - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                        - local (bool): Whether calculation of empowerment is done locally or globally.
                        - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations
                                    or length of set of resulting elements.

        Returns:
            Model: Model instance depending on what version is requested.
        """
        if model_type == 'trueemp':
            return TrueEmpModel(self.game_version, self.memory_type, empowerment_calculation)
            """
        elif model_type == 'emp':
            # Needs  "EmpowermentTable-X-Y.csv" file from customgametree to run this. 
            # Input through get_empowerment_info() function in data_handle.py
            return EmpModel(self.game_version, self.memory_type, empowerment_calculation, self.vector_version, self.split_version,)
            """
        else:
            raise ValueError('Undefined model version: "{}". Use "emp" or "trueemp" instead.'.format(model_type))
