import json
import itertools
from itertools import combinations_with_replacement

import data_handle as data_handle
import pandas as pd


"""
Modify all parts of code containing 'first' and 'second' to include for 3 element combinations. 

"""

class Tables():
    """Class functions generate Totem game tables.
    """
    def __init__(self):
        """Initializes table class.
        """
        
        
    def get_tables(self, table_type='combination', version='totem', expand=False):
        """Returns table depending on the type. Can either be combination, parent or child table.

        Args:
            table_type (str, optional): 'combination', 'parent' or 'child'. States what kind of table is going to be created. 
                        Defaults to 'combination'.
            version (str, optional): 'totem'. 
                        States what element and combination set is going to be used. 
            expand (bool, optional): True if table also includes unsuccessful combinations. False if table only includes
                        successful combinations. Defaults to False.
        """
        if table_type != 'combination' and table_type != 'parent' and table_type != 'child':
            raise ValueError('Undefined Version: "{}". Use "combination", "parent" or "child" instead.'.format(table_type))
        
        if version != 'totem':
            raise ValueError('Undefined Version: "{}". Use "totem" instead.'.format(version))
        
        # print info for user
        print('\nGet table of type {} for version {}.'.format(table_type, version))
        
        # get game tree
        gametree = data_handle.get_gametree(version)

        # initialize search table and parent respectively child table
        table = dict()
        table_csv = list()

        # traverse through game tree 
        for element in gametree:
            for parent in gametree[element]["parents"]:
                parent = tuple(sorted(parent))

                if table_type == 'combination':
    
                    # assign resulting elements to combination elements
                    for i in range(len(parent)):
                        if parent[i] not in table:
                            table[parent[i]] = {}
                        
                        # Create a key for the other parents
                        other_parents_key = tuple(sorted([p for p in parent if p != parent[i]]))
                        other_parents = ','.join(map(str, other_parents_key))  # Convert tuple to string
                        
                        if other_parents not in table[parent[i]]:
                            table[parent[i]][other_parents] = [element]
                        elif element not in table[parent[i]][other_parents]:
                            table[parent[i]][other_parents].append(element)
                    
                    # Add to CSV list
                    table_csv.append({
                        'first': parent[0],
                        'second': parent[1] if len(parent) > 1 else None,
                        'third': parent[2] if len(parent) > 2 else None,
                        'result': element
                    })    

                elif table_type == 'parent':
                    # add resulting element to parent list for each combination element
                    for p in parent:
                        if p not in table:
                            table[p] = {element}
                        else:
                            table[p].update([element])

                elif table_type == 'child':
                    # add parents to child list for resulting element
                    if element not in table:
                        table[element] = set(parent)
                    else:
                        table[element].update(parent)

        if table_type == 'combination':
            table_csv = pd.DataFrame(table_csv)
            if expand is True:                      # Includes unsuccessful elements as well. 
                table_csv = self.expand_combination_table(table_csv, version)
        else:
            # transform into DataFrame
            for element in table:
                table[element] = list(table[element])
            table_csv = pd.DataFrame({key:pd.Series(value) for key, value in table.items()})
        
        if table_type == 'combination':
            # Convert tuple keys to strings in the table dictionary
            new_table = {}
            for key, value in table.items():
                new_value = {}
                for sub_key, sub_value in value.items():
                    if isinstance(sub_key, tuple):
                        new_sub_key = ','.join(str(item) for item in sub_key)
                    else:
                        new_sub_key = sub_key
                    new_value[new_sub_key] = sub_value
                new_table[key] = new_value
            table = new_table

        # write to JSON file
        with open('data//tables//{}{}Table.json'.format(version, table_type.capitalize()), 'w') as filehandle:
            json.dump(table, filehandle, indent=4, sort_keys=True)
        
        # replace nan values with -1
        table_csv = table_csv.fillna(-1)
        
        # write to csv file
        table_csv.to_csv('data//tables//{}{}Table.csv'.format(version, table_type.capitalize()), index=False, float_format='%.f')

    def expand_combination_table(self, table_results, version='totem'):
        """Expands table to include all element combinations, whether successful or not.

        Args:
            table_results (DataFrame): DataFrame consisting of 4 columns: 
                        (1) first (element index)
                        (2) second (element index) 
                        (3) third (element index) 
                        (4) result (element index or NaN)
            version (str, optional): 'totem'. 
                        States what element and combination set is going to be used. 

        Returns:
            DataFrame: DataFrame consisting of 5 columns: 
                        (1) first (element index)
                        (2) second (element index) 
                        (3) third (element index) 
                        (4) success (0 or 1)
                        (5) result (element index or NaN)
        """
        # get umber of elements
        if version == 'totem':
            n_elements = 136        # Make sure of this!

        # transform first three entries in table to list
        parents_results = table_results[['first', 'second', 'third']].values.tolist()

        # get result for each inventory combination
        table_success = []
        for r in range(1, 4):  # 1, 2, or 3 parents
            combinations = itertools.combinations_with_replacement(range(n_elements), r)
            for c in combinations:
                combination = sorted(c)
                if len(combination) < 3:
                    combination += [None] * (3 - len(combination))
                if combination in parents_results:
                    table_success.append({'first': combination[0], 'second': combination[1], 'third': combination[2], 'success': 1})
                else:
                    table_success.append({'first': combination[0], 'second': combination[1], 'third': combination[2], 'success': 0})

        table_success = pd.DataFrame(table_success)

        table_expanded = pd.merge(table_results, table_success, how='outer', on=['first', 'second', 'third'])
        table_expanded = table_expanded[['first', 'second', 'third', 'success', 'result']]

        # return expanded table
        return table_expanded