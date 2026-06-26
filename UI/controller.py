import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genere = None
        self.artista = None

    def fillDDGenre(self):
        self._generi = self._model.getAllGeneri()
        gen = list(map(lambda x: ft.dropdown.Option(key=x.Name,
                                                    data=x,
                                                    on_click= self._choice
                                                    ), self._generi))
        self._view._ddGenre.options = gen
        self._view.update_page()

    def _choice(self, e):
        self._genere = e.control.data

    def fillDDArtist(self):
        self._view._ddArtist.options.clear()
        for a in self._model.mappaArtisti.values():
            self._view._ddArtist.options.append(ft.dropdown.Option(key=a.Name, data=a, on_click= self._choice2))
        self._view.update_page()

    def _choice2(self, e):
        self.artista = e.control.data

    def handleCreaGrafo(self, e):
        if self._genere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("selezionare"))
            self._view.update_page()
            return #DA METTERE

        self._model.creaGrafo(self._genere)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text("grafo creato correttamente"))
        self._view.txt_result.controls.append(ft.Text(f"nodi {self._model.getN()} e archi {self._model.getA()} "
                                                   f"e maggiore influenza: {self._model.influenza}"))
        for l in self._model.pesoMa():
            self._view.txt_result.controls.append(ft.Text(f"{l[0]} -> {l[1]} con peso {l[2]["weight"]}"))
        self._view.update_page()

        self.fillDDArtist()
        self._view.update_page()

    def handleCreaGrafo1(self,e):
        pass

    def handleCammino(self,e):
        if self.artista is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("Selezionare un artista"))
            self._view.update_page()
            return

            # Punto 2b
        # = self._model.camminoLungo(self.artista)
        # Punto 2c
        cammino_crescente = self._model.camminoCrescente(self.artista)

        self._view.txt_result.controls.clear()

        #self._view.txt_result.controls.append(ft.Text(f"Cammino più lungo ({len(cammino_lungo)} nodi):"))
        #for nodo in cammino_lungo:
         #   self._view.txt_result.controls.append(ft.Text(f"  {nodo.Name}"))

        self._view.txt_result.controls.append(ft.Text(""))  # riga vuota

        self._view.txt_result.controls.append(ft.Text(f"Cammino pesi crescenti ({len(cammino_crescente)} nodi):"))
        for nodo in cammino_crescente:
            self._view.txt_result.controls.append(ft.Text(f"  {nodo.Name}"))

        self._view.update_page()