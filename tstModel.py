from model.model import Model
mymdl = Model()

mymdl.creaGrafo('Rock')
nodi, archi = mymdl.getGraphDetails()
print(f"Grafo creato! Il grafo ha {nodi} nodi e {archi} archi.")