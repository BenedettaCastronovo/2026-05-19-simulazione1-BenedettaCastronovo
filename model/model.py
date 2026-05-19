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
        self._grafo.add_nodes_from(self._artisti)
        # Creiamo un set di ID per un controllo istantaneo e sicuro al 100%
        id_artisti_validi = {a.ArtistId for a in self._artisti}
        mappaArtisti = {a.ArtistId: a for a in self._artisti}
        archi = DAO.edges(mappaArtisti, genere)
        pesi = DAO.getAllP(mappaArtisti)  # ← one query instead of N*2
        for a1, a2 in archi:
            # BLINDATURA: Salta l'arco se uno dei due artisti non appartiene al genere selezionato
            if a1.ArtistId not in id_artisti_validi or a2.ArtistId not in id_artisti_validi:
                continue
            #p1 = DAO.getP(a1) facendone uno per volta impiega più tempo e sbaglia anche i nodi
            #p2 = DAO.getP(a2)
            p1 = int(pesi.get(a1.ArtistId, 0))
            p2 = int(pesi.get(a2.ArtistId, 0))
            if p1 > p2:
                self._grafo.add_edge(a1, a2, weight = (p1+p2))
            elif p1 == p2:
                self._grafo.add_edge(a1, a2, weight = (p1+p2))
                self._grafo.add_edge(a2, a1, weight = (p1+p2))
            elif p1<p2:
                self._grafo.add_edge(a2, a1, weight = (p1+p2))

    def getN(self):
        return len(self._grafo.nodes())

    def getA(self):
        return len(self._grafo.edges())

    @property
    def influenza(self):

        influenze = []
        for n in self._artisti:
            uscenti = list(self._grafo.out_edges(n, data = True))
            entranti = list(self._grafo.in_edges(n, data = True))
            pU = 0
            pE = 0
            for u in uscenti:
                pU += u[2]["weight"] #u["weight"] non va bene #devo indicare anche u[2]
            for e in entranti:
                pE += e[2]["weight"]

            influenze.append((n.Name, (pU-pE)))
        massimo = max(influenze, key=lambda x: x[1])
        return massimo[0]

    def pesoMa(self):
        lista = sorted(self._grafo.edges(data=True), key= lambda x: x[2]["weight"], reverse = True) #anche qua devo mettere ["weight"[
        return lista[:5]

    #data = True IMPORTANTE