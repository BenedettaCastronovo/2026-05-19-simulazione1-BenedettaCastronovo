from operator import itemgetter

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.mappaG = {}
        self._grafo = nx.DiGraph()
        self._artisti = []

    def getAllGeneri(self):
        gen = DAO.getAllGen()
        for g in gen:
            self.mappaG[g.GenreId] = g
        return gen

    def creaGrafo(self, genere):
        self._grafo.clear()
        self._artisti = DAO.getArtisti(genere)
        self._grafo.add_edges_from(self._artisti)
        archi = DAO.edges(self.mappaG)
        for a1, a2 in archi:
            p1 = DAO.getP(a1)
            p2 = DAO.getP(a2)
            if p1 > p2:
                self._grafo.add_edge(a1, a2, weight = (p1+p2))
            elif p1 == p2:
                self._grafo.add_edge(a1, a2, weight = (p1+p2))
                self._grafo.add_edge(a2, a1, weight = (p1+p2))
            else:
                self._grafo.add_edge(a2, a1, weight = (p1+p2))

    def getN(self):
        return len(self._grafo.nodes())

    def getA(self):
        return len(self._grafo.edges())

    @property
    def influnza(self):

        influenze = []
        for n in self._artisti:
            uscenti = list(self._grafo.out_edges(n, data = True))
            entranti = list(self._grafo.in_edges(n, data = True))
            pU = 0
            pE = 0
            for u in uscenti:
                pU += u["weight"]
            for e in entranti:
                pE += e["weight"]

            influenze.append((n.Name, (pU-pE)))
            massimo = max(influenze, key=lambda x: x[1])
        return massimo[0]

    def pesoMa(self):
        lista = sorted(self._grafo.edges, key= lambda x: x[2], reverse = True)
        return lista[:5]