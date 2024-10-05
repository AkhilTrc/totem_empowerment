import json

class Gametrees():
    """Class functions generate Little Alchemy game trees.
    """
    def __init__(self):
        """Initializes game tree class.
        """

    def get_totem_gametree(self):
        """Gets game tree of Little Alchemy 1.
        """
        # print info for user
        print('\nGet alchemy1 game tree.')

        # load raw gametree
        with open('data\\nonlabelled_combinations.csv', encoding='utf8') as infile:
            old_gametree = json.load(infile)

        # initialize element storage for alchemy 1 elements
        elements = set()

        # get all elements from little alchemy 1
        for key, value in old_gametree.items():
            parents = key.split(',')
            results = value
            elements.update(parents, results)
        elements.difference_update({'water', 'fire', 'earth', 'air'})
        elements = ['water', 'fire', 'earth', 'air'] + list(elements)

        # initialize game tree
        gametree = dict()
        for element_id, element in enumerate(elements):
            gametree[element_id] = {'name': element, 'parents': []}

        # fill game tree
        for key, value in old_gametree.items():
            parents = key.split(',')
            parents = sorted([elements.index(parents[0]), elements.index(parents[1])])
            results = value
            for result in results:
                gametree[elements.index(result)]['parents'].append(parents)

        # write edited library to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/alchemy1Gametree.json', 'w') as filehandle:
            json.dump(gametree, filehandle, indent=4, sort_keys=True)

        # write elements to JSON file
        with open('empowermentexploration/resources/littlealchemy/data/alchemy1Elements.json', 'w') as filehandle:
            json.dump(elements, filehandle, indent=4, sort_keys=True)

    