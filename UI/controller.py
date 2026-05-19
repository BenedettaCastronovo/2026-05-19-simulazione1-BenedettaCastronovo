import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._genere = None

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

    def handleCreaGrafo(self, e):
        if self._genere is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(text = "selezionare")
            self._view.update_page()

        self._model.creaGrafo(self._genere)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(text="grafo creato correttamente")
        self._view.txt_result.controls.append(text=f"nodi {self._model.getN()} e archi {self._model.getA()} "
                                                   f"e maggiore influenza: {self._model.influenza}")
        for l in self._model.pesoMa():
            self._view.txt_result.controls.append(text=f"{l}")
        self._view.update_page()

    def handleCreaGrafo1(self,e):
        pass

    def handleCammino(self,e):
        pass