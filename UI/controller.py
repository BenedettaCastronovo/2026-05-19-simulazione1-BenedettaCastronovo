import flet as ft
#
#
class Controller:
    def __init__(self, view, model):
         # the view, with the graphical elements of the UI
         self._view = view
         # the model, which implements the logic of the program and holds the data
         self._model = model
         self._genere = None
         self._artista = None

    def fillDDGenre(self):
       self._generi = self._model.getGenere()
       for y in self._generi:
           self._view._ddGenre.options.append(ft.dropdown.Option(key=y.Name,
                                                                 data=y,
                                                                 on_click = self._choice))
       self._view.update_page()

    def _choice(self,e):
        self._genere = e.control.key #faccio sempre questo e via
    #
#     def fillDDGenre(self):
#         self._generi = self._model.getAllGeneri()
#         gen = list(map(lambda x: ft.dropdown.Option(key=x.Name,
#                                                     data=x,
#                                                     on_click= self._choice
#                                                     ), self._generi))
#         self._view._ddGenre.options = gen
#         self._view.update_page()
#
#     def _choice(self, e):
#         self._genere = e.control.data
#
#     def fillDDArtist(self):
#         self._view._ddArtist.options.clear()
#         for a in self._model.mappaArtisti.values():
#             self._view._ddArtist.options.append(ft.dropdown.Option(key=a.Name, data=a, on_click= self._choice2))
#         self._view.update_page()
#
#     def _choice2(self, e):
#         self.artista = e.control.data
#
    def handleCreaGrafo(self, e):
        self._genere = self._view._ddGenre.value
        if self._genere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("valori nulli, riprova", color="red"))
            self._view.update_page()
            return

        self._model.creaGrafo(self._genere)
        nNodes, nEdges = self._model.getGraphDetails()

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato:", color="green"))
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo contiene {nNodes} nodi e {nEdges} archi."))

        artista, influenza = self._model.getMax()
        self._view.txt_result.controls.append(ft.Text(f"Artista con maggiore influenza: {artista} - influenza: {influenza}"))
        archi = self._model.getTop5Archi()
        for l in archi:
            self._view.txt_result.controls.append(ft.Text(f"{l[0]} -> {l[1]} con peso {l[2]["weight"]}"))
        self._view.update_page()

        allNodes = self._model.getAllNodes()
        self._fillDropdown(allNodes)  # se li riempio a partire da altro poi devo sempre fare CLEAR
        self._view.update_page()

    def _fillDropdown(self, allNodes):
        self._view._ddArtist.options.clear()
        if len(allNodes) < 1:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("valori nulli, riprova", color="red"))
        for s in allNodes:
            self._view._ddArtist.options.append(ft.dropdown.Option(key=s.Name,
                                                                   data=s,
                                                                   on_click=self._choiceA))
            self._view.update_page()

    def _choiceA(self, e):
        self._artista = e.control.data


    #
#         for l in self._model.pesoMa():
#             self._view.txt_result.controls.append(ft.Text(f"{l[0]} -> {l[1]} con peso {l[2]["weight"]}"))
#         self._view.update_page()
#
#         self.fillDDArtist()
#         self._view.update_page()
#
#     def handleCreaGrafo1(self,e):
#         pass
#
    def handleCammino(self,e):
        if self._artista is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("seleziona un valore, riprova", color="red"))
            self._view.update_page()
            return

        best = self._model.cercaCammino(self._artista)
        if len(best) == 0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text(f"Cammino non trovato per {self._artista}", color="orange"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Cammino trovato"))
        for a in best:
            self._view.txt_result.controls.append(ft.Text(f" {a}"))
        self._view.update_page()

#         if self.artista is None:
#             self._view.txt_result.controls.clear()
#             self._view.txt_result.controls.append(ft.Text("Selezionare un artista"))
#             self._view.update_page()
#             return
#
#             # Punto 2b
#         # = self._model.camminoLungo(self.artista)
#         # Punto 2c
#         cammino_crescente = self._model.camminoCrescente(self.artista)
#
#         self._view.txt_result.controls.clear()
#
#         #self._view.txt_result.controls.append(ft.Text(f"Cammino più lungo ({len(cammino_lungo)} nodi):"))
#         #for nodo in cammino_lungo:
#          #   self._view.txt_result.controls.append(ft.Text(f"  {nodo.Name}"))
#
#         self._view.txt_result.controls.append(ft.Text(""))  # riga vuota
#
#         self._view.txt_result.controls.append(ft.Text(f"Cammino pesi crescenti ({len(cammino_crescente)} nodi):"))
#         for nodo in cammino_crescente:
#             self._view.txt_result.controls.append(ft.Text(f"  {nodo.Name}"))
#
#         self._view.update_page()