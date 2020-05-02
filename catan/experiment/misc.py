import random
import networkx as nx

def roll_dice():
    '''
    Does this have a normal distribution with mean at 7?
    '''
    return random.randint(1,6) + random.randint(1,6)

        
def die_roll_prob(n):
    p = 1. / 36.
    if n == 2 or n== 12:
        return p
    elif n == 3 or n== 11:
        return 2 * p
    elif n == 4 or n== 10:
        return 3 * p
    elif n == 5 or n== 9:
        return 4 * p
    elif n == 6 or n== 7:
        return 5 * p
    elif n == 7:
        return 6 * p
    else:
        return 0


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
    