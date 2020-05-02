import random
import networkx as nx

def roll_dice():
    '''
    Does this have a normal distribution with mean at 7?
    '''
    return random.randint(1,6) + random.randint(1,6)


def search(G, root):

    def _search(G, source, depth):
        if depth > 5:
            return  []

        visited[source] = True

        neighbors = nx.neighbors(G, source)

        # print(('\t'*depth) + str(source))
        for neighbor in neighbors:
            if depth == 5 and neighbor == root:
                # print(('\t'*(depth+1)) + str(neighbor))
                return [neighbor]

            if neighbor not in visited:
                m = _search(G, neighbor, depth + 1)
                if len(m) > 0:
                    return  [neighbor] + m

        return []

    # ==================

    visited = dict()
    return _search(G, root, 0)
    
        