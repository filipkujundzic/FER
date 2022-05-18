#Napredni algoritmi i strukture podataka
#Laboratorijska vježba

from collections import defaultdict 

def i(character):
	return ord(character) - 65

def get_char(number):
    return chr(number + 65)

 
class Graph: 
  
    def __init__(self, vertices): 
        self.V = vertices 
        self.graph = [] 
   
    def addEdge(self, u, v, w): 
        self.graph.append([u, v, w]) 
          

    def printDst(self, dist, src, dest): 
   
        k = 0
        for i in range(self.V): 
            a = get_char(k)
            if(k == dest):
                result = dist[i]
            k = k + 1
        print("Distance from " + get_char(src) + " to " + get_char(dest) + ": " + str(result))

    def print_path(self, src, dest, previous):

        i = -1000
        lista = []
        lista.append(dest)
        while(dest != src):
            lista.append(previous[dest])
            dest = previous[dest]

        lista.reverse()

        lista[:] = [get_char(i) for i in lista]
        print(lista)

    def BellmanFord(self, src, dest): 
  
        dist = [float("Inf")] * (self.V + 1)
        dist[src] = 0 
        previous = [None] * (self.V + 1)
        previous[src] = 0
  
        for i in range(self.V - 1): 

            for u, v, w in self.graph:
                tmp = dist[u] + w
                if dist[u] != float("Inf") and tmp < dist[v]: 
                        dist[v] = tmp
                        previous[v] = u

        for u, v, w in self.graph: 
                if dist[u] != float("Inf") and dist[u] + w < dist[v]: 
                        print ("Graph contains negative weight cycle")
                        return

        self.printDst(dist, src, dest) 
        self.print_path(src,dest,previous)



g = Graph(18)
g.addEdge(i('A'), i('B'),2)
g.addEdge(i('A'), i('C'),6)
g.addEdge(i('A'), i('D'),12)
g.addEdge(i('D'), i('H'),-2)
g.addEdge(i('B'), i('C'),3)
g.addEdge(i('B'), i('E'),9)
g.addEdge(i('C'), i('F'),1)
g.addEdge(i('G'), i('I'),1)
g.addEdge(i('F'), i('E'),2)
g.addEdge(i('E'), i('G'),1)
g.addEdge(i('F'), i('H'),4)
g.addEdge(i('H'), i('I'),3)
g.addEdge(i('I'), i('J'),-1)
g.addEdge(i('J'), i('H'),5)
g.addEdge(i('H'), i('K'),1)
g.addEdge(i('K'), i('J'),1) #
g.addEdge(i('H'), i('L'),-3)
g.addEdge(i('N'), i('O'),1) #
g.addEdge(i('H'), i('M'),-2)
g.addEdge(i('K'), i('O'),-9)
g.addEdge(i('M'), i('L'),2)
g.addEdge(i('L'), i('P'),7)
g.addEdge(i('M'), i('R'),2)
g.addEdge(i('N'), i('S'),-9)
g.addEdge(i('O'), i('S'),11)
g.addEdge(i('P'), i('S'),-6)
g.addEdge(i('R'), i('S'),3)


g.BellmanFord(i('A'),i('H'))