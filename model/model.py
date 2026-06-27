import copy
from operator import itemgetter

import networkx as nx
#
from database.DAO import DAO
#
#
class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self.mappaArtisti = {}
        self.best = []

    def getGenere(self):
        return DAO.getGenere()

    def creaGrafo(self, genere):
        self._grafo.clear()
        self._generi = DAO.getNodes(genere)
        self._grafo.add_nodes_from(self._generi)
        for n in self._generi:
            self.mappaArtisti[n.ArtistId] = n
        self._archi = DAO.getEdges(genere)
        self._pop = DAO.getPop(genere)
        for u, v in self._archi:
            up = self._pop[u]
            vp = self._pop[v]
            if up > vp:
                self._grafo.add_edge(self.mappaArtisti[u], self.mappaArtisti[v], weight = up + vp)
            elif up < vp:
                self._grafo.add_edge(self.mappaArtisti[v], self.mappaArtisti[u], weight = up + vp)
            else:
                self._grafo.add_edge(self.mappaArtisti[u], self.mappaArtisti[v], weight = up + vp)
                self._grafo.add_edge(self.mappaArtisti[v], self.mappaArtisti[u], weight = up + vp)

    def getGraphDetails(self):
        return len(self._grafo.nodes()), len(self._grafo.edges())

    def getMax(self):
        listNodesPesata = []
        for n in self._grafo.nodes:
            score = 0
            for e in self._grafo.out_edges(n, data=True):
                score += e[2]["weight"]
            for e in self._grafo.in_edges(n, data=True):
                score -= e[2]["weight"]
            listNodesPesata.append((n, score))
        listNodesPesata.sort(key=lambda x: x[1], reverse=True)
        return listNodesPesata[0]

    def getTop5Archi(self):
        return sorted(self._grafo.edges(data=True), key=lambda x: x[2]["weight"], reverse=True)[:5]

    def getAllNodes(self):
        return list(self._grafo.nodes())

    def cercaCammino(self, source):
        self.best = []
        parziale = [source]
        for n in self._grafo.successors(source):
            parziale.append(n)
            self._ricorsione(parziale)
            parziale.pop()
        return self.best

    def _ricorsione(self, parziale):
        if len(parziale) > len(self.best):
            self.best = copy.deepcopy(parziale)

        for n in self._grafo.successors(parziale[-1]):
            if n not in parziale and self.is_valid(parziale, n):
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()

    def is_valid(self, parziale, n):
        if len(parziale) >= 2:
            if self._grafo[parziale[-2]][parziale[-1]]["weight"] < self._grafo[parziale[-1]][n]["weight"]:
                return True
        return False


#     def getAllGeneri(self):
#         gen = DAO.getAllGen()
#         for g in gen:
#             self.mappaG[g.GenreId] = g
#         return gen
#
#     def creaGrafo(self, genere):
#         self._grafo.clear()
#         self._artisti = DAO.getArtisti(genere)
#         self._grafo.add_nodes_from(self._artisti)
#         # Creiamo un set di ID per un controllo istantaneo e sicuro al 100%
#         #id_artisti_validi = {a.ArtistId for a in self._artisti}
#         self.mappaArtisti = {a.ArtistId: a for a in self._artisti}
#         self._archi = DAO.getArchi(genere)
#         for a in self._archi:
#             if a[2] > a[3]:
#                 self._grafo.add_edge(self.mappaArtisti[a[0]], self.mappaArtisti[a[1]], weight = a[4])
#             elif a[3] > a[2]:
#                 self._grafo.add_edge(self.mappaArtisti[a[1]], self.mappaArtisti[a[0]], weight = a[4])
#             else:
#                 self._grafo.add_edge(self.mappaArtisti[a[0]], self.mappaArtisti[a[1]], weight=a[4])
#                 self._grafo.add_edge(self.mappaArtisti[a[1]], self.mappaArtisti[a[0]], weight = a[4])
#
#         # archi = DAO.edges(self.mappaArtisti, genere)
#         # pesi = DAO.getAllP(self.mappaArtisti, genere)  # ← one query instead of N*2
#         # for a1, a2 in archi:
#         #     # BLINDATURA: Salta l'arco se uno dei due artisti non appartiene al genere selezionato
#         #     if a1.ArtistId not in id_artisti_validi or a2.ArtistId not in id_artisti_validi:
#         #         continue
#         #     #p1 = DAO.getP(a1) facendone uno per volta impiega più tempo e sbaglia anche i nodi
#         #     #p2 = DAO.getP(a2)
#         #     p1 = int(pesi[a1.ArtistId, 0])
#         #     p2 = int(pesi[a2.ArtistId, 0])
#         #     if p1 > p2:
#         #         self._grafo.add_edge(a1, a2, weight = (p1+p2))
#         #     elif p1 == p2:
#         #         self._grafo.add_edge(a1, a2, weight = (p1+p2))
#         #         self._grafo.add_edge(a2, a1, weight = (p1+p2))
#         #     elif p1<p2:
#         #         self._grafo.add_edge(a2, a1, weight = (p1+p2))
#
#     def getN(self):
#         return len(self._grafo.nodes())
#
#     def getA(self):
#         return len(self._grafo.edges())
#
#     @property
#     def influenza(self):
#
#         influenze = []
#         for n in self._artisti:
#             uscenti = list(self._grafo.out_edges(n, data = True))
#             entranti = list(self._grafo.in_edges(n, data = True))
#             pU = 0
#             pE = 0
#             for u in uscenti:
#                 pU += u[2]["weight"] #u["weight"] non va bene #devo indicare anche u[2]
#             for e in entranti:
#                 pE += e[2]["weight"]
#
#             influenze.append((n.Name, (pU-pE)))
#         massimo = max(influenze, key=lambda x: x[1])
#         return massimo[0]
#
#     def pesoMa(self):
#         lista = sorted(self._grafo.edges(data=True), key= lambda x: x[2]["weight"], reverse = True) #anche qua devo mettere ["weight"[
#         return lista[:5]
#
#     #data = True IMPORTANTE
#
#     #def camminoLungo(self, artista):
#         self._best = []
#         self._dfsLungo(artista, [])
#         return self._best
#
#     #def _dfsLungo(self, nodo, cammino_corrente):
#         cammino_corrente.append(nodo)
#         if len(cammino_corrente) > len(self._best):
#             self._best = list(cammino_corrente)
#
#         #La condizione terminale è implicita nel ciclo for — la ricorsione si ferma naturalmente quando non ci sono più vicini da esplorare, cioè quando:
#         #il nodo non ha archi uscenti, oppure
#         #tutti i vicini sono già in cammino_corrente
#
#         for _, vicino, data in self._grafo.out_edges(nodo, data=True):
#             if vicino not in cammino_corrente:  # semplice = no cicli
#                 self._dfsLungo(vicino, cammino_corrente)
#
#         cammino_corrente.pop()  # backtracking
#
#     #def camminoCrescente(self, artista):
#         self._best = []
#         self._dfsCrescente(artista, [], 0)
#         return self._best
#
#     #def _dfsCrescente(self, nodo, cammino_corrente, ultimo_peso):
#         cammino_corrente.append(nodo)
#         if len(cammino_corrente) > len(self._best):
#             self._best = list(cammino_corrente)
#
#         for _, vicino, data in self._grafo.out_edges(nodo, data=True):
#             peso = int(data["weight"])
#             if peso > ultimo_peso and vicino not in cammino_corrente:
#                 self._dfsCrescente(vicino, cammino_corrente, peso)
#
#         cammino_corrente.pop()  # backtracking
#
#     def camminoLungo(self, artista):
#         self._best = []
#         parziale = [artista]
#         self._dfsLungo(parziale)
#         return self._best
#
#     def _dfsLungo(self, parziale):
#         if len(parziale) > len(self._best):
#             self._best = copy.deepcopy(parziale)
#
#         for n in self._grafo.successors(parziale[-1]):
#             if n not in parziale:
#                 parziale.append(n)
#                 self._dfsLungo(parziale)
#                 parziale.pop()
#
#
#
#     def camminoCrescente(self, artista):
#         self._best = []
#         parziale = [artista]
#         for n in self._grafo.successors(parziale[-1]):
#             parziale.append(n)
#             self._dfsCrescente(parziale)
#             parziale.pop()
#         return self._best
#
#     def _dfsCrescente(self, parziale):
#         if len(parziale) > len(self._best):
#             self._best = copy.deepcopy(parziale)
#
#         for n in self._grafo.successors(parziale[-1]):
#             if self._grafo[parziale[-2]][parziale[-1]]["weight"] < self._grafo[parziale[-1]][n]["weight"] and n not in parziale:
#                 parziale.append(n)
#                 self._dfsCrescente(parziale)
#                 parziale.pop()