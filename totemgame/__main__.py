# from totemgame.empowerment import Empowerment
# from totemgame.similarity import Similarity
from totemgame.gametrees import Gametrees
from totemgame.tables import Tables
# from totemgame.vectors import Vectors

if __name__ == '__main__':
    # YOUR ACTION IS REQUIRED HERE: CHOOSE APPROPRIATE METHOD AND METHOD ARGUMENTS
    gametree = Gametrees()
    gametree.get_totem_gametree()

    table = Tables()
    table.get_tables('combination','totem', expand=True)
    table.get_tables('parent','totem')
    table.get_tables('child','totem')

    """
    vector = Vectors()
    vector.get_wordvectors('totem_game', 'crawl', 300)
    
    Similarity('totem_game', 'crawl300')

    Empowerment('totem_game', 'data', 'crawl300')
    # YOUR ACTION IS NOT RECQUIRED ANYMORE
    """