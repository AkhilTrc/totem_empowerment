from empowerment import Empowerment
from totemgame.similarity import Similarity
from gametrees import Gametrees
from tables import Tables
from vectors import Vectors

if __name__ == '__main__':
    # YOUR ACTION IS REQUIRED HERE: CHOOSE APPROPRIATE METHOD AND METHOD ARGUMENTS
    gametree = Gametrees()
    gametree.get_totem_gametree()

    table = Tables()
    table.get_tables('combination','totem_game', expand=True)
    table.get_tables('parent','totem_game')
    table.get_tables('child','totem_game')

    vector = Vectors()
    vector.get_wordvectors('totem_game', 'crawl', 300)
    
    Similarity('totem_game', 'crawl300')

    Empowerment('totem_game', 'data', 'crawl300')
    # YOUR ACTION IS NOT RECQUIRED ANYMORE
