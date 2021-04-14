import networkx as nx
import heapq

import queue as q
G = nx.Graph()
edge_list = [("Arad", "Zerind", 75), ("Arad", "Sibiu", 140), ("Arad", "Timisoara", 118),
             ("Bucharest", "Fagaras", 211), ("Bucharest", "Pitesti", 101), ("Bucharest", "Giurgiu", 90),
             ("Bucharest", "Urziceni", 85), ("Craiova", "RimnicuVilcea", 146), ("Craiova", "Dobreta", 120),
             ("Craiova", "Pitesti", 138), ("Dobreta", "Mehadia", 75), ("Eforie", "Hirsova", 86),
            ("Fagaras", "Sibiu", 99), ("Giurgiu", "Bucharest", 90), ("Hirsova", "Urziceni", 98), ("Hirsova", "Eforie", 86),
            ("Iasi", "Vaslui", 92), ("Iasi", "Neamt", 87), ("Lugoj", "Timisoara", 111), ("Lugoj", "Mehadia", 70),
            ("Oradea", "Zerind", 71), ("Oradea", "Sibiu", 151), ("Pitesti", "RimnicuVilcea", 97),
             ("RimnicuVilcea", "Sibiu", 80), ("Urziceni", "Vaslui", 142)]
bucharest_line_list = {"Arad": 366, "Bucharest": 0, "Craiova": 160, "Dobreta": 242,
                      "Eforie": 161, "Fagaras": 178, "Giurgiu": 77, "Hirsova": 151,
                      "Iasi": 226, "Lugoj": 244, "Mehadia": 241, "Neamt": 234,
                      "Oradea": 380, "Pitesti": 98, "RimnicuVilcea": 193, "Sibiu": 253,
                      "Timisoara": 329, "Urziceni": 80, "Vaslui": 199, "Zerind": 374}

G.add_weighted_edges_from(edge_list)
G.edges(data=True)


def heappeak(heap):
    smallest = heapq.heappop(heap)
    heapq.heappush(heap, smallest)
    return smallest


queue = q.PriorityQueue()


def Astar(city):
    edge_list = G.edges(city)
    h = []
    for e in edge_list:
        adj_edge = G.get_edge_data(e[0], e[1])

        edge_weight = G.get_edge_data(e[0], e[1])["weight"]
        new_weight = bucharest_line_list[e[1]]
        edge_list = [new_weight + edge_weight, new_weight, edge_weight, e[0], e[1]]

        heapq.heappush(h, edge_list)

    while True:
        popped_list = []
        new_popped_list = []
        num = len(heappeak(h))
        for i in range(num):
            popped_list.append(heappeak(h)[i])
        heapq.heappop(h)
        popped_name = popped_list[-1]
        popped_weight = popped_list[0]

        if (popped_name == "Bucharest"):
            print("From city:", city)
            print("To city: Bucharest")
            path = "Best route: "
            for i in range(3, len(popped_list)):
                if i == 3:
                    path += popped_list[i]
                else:
                    path += (" - " + popped_list[i])
            print(path)
            print("Total distance:", popped_list[0])

            return
        edge_list = G.edges(popped_name)
        for e in edge_list:

            for i in popped_list:
                new_popped_list.append(i)

            edge_weight = G.get_edge_data(e[0], e[1])["weight"]

            new_weight = bucharest_line_list[e[1]]
            new_popped_list[2] += edge_weight
            new_popped_list[1] = new_weight
            new_popped_list[0] = new_popped_list[1] + new_popped_list[2]
            new_popped_list.append(e[1])
            heapq.heappush(h, new_popped_list)
            new_popped_list = []


Astar("Lugoj")