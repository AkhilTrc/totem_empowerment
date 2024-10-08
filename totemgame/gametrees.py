import json

class Gametrees():
    """Class functions generate Totem game trees.
    """
    def __init__(self):
        """Initializes game tree class.
        """

    def get_totem_gametree(self):
        """Gets game tree of Totem Game.
        """
        # print info for user
        print('\nGet Totem game tree.')

        # load raw gametree
        with open('data\\elements.json', encoding='utf8') as infile:
            old_gametree = json.load(infile)

        # initialize element storage for Totem game elements
        elements = set()

        # get all elements from Totem game
        for key, value in old_gametree.items():
            parents = key.split(',')
            parents = [p.strip() for p in parents]
            results = value
            elements.update(parents, results)

        elements.difference_update({'Big_Tree', 'Tree', 'Stone', 'Red_Berry', 'Blue_Berry', 'Antler'})
        elements = ['Big_Tree', 'Tree', 'Stone', 'Red_Berry', 'Blue_Berry', 'Antler'] + list(elements)

        # initialize game tree
        gametree = dict()
        for element_id, element in enumerate(elements):
            gametree[element_id] = {'name': element, 'parents': []}

        # fill game tree
        for key, value in old_gametree.items():
            parents = key.split(',')
            parents = [p.strip() for p in parents]
            if len(parents) == 1:
                parents = sorted([elements.index(parents[0])])
            elif len(parents) == 2:
                parents = sorted([elements.index(parents[0]), elements.index(parents[1])])
            elif len(parents) == 3:
                parents = sorted([elements.index(parents[0]), elements.index(parents[1]), elements.index(parents[2])])
            results = value
            for result in results:
                gametree[elements.index(result)]['parents'].append(parents)

        # write edited library to JSON file
        with open('data\\gametrees\\totemGametree.json', 'w') as filehandle:
            json.dump(gametree, filehandle, indent=4, sort_keys=True)

        # write elements to JSON file
        with open('data\\gametrees\\totemElements.json', 'w') as filehandle:
            json.dump(elements, filehandle, indent=4, sort_keys=True)

    