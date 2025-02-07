import geopandas as geo
from shapely.geometry import Point,LineString
import rtree

class puntoInicial:
	def __init__(self,i,p):
		self.id_punto=i
		self.punto=p
		self.ramaIni=None
		self.buscaRamas()

	def buscaRamas(self):
		tmp = list(rtreeIdx.intersection(self.punto.bounds))
		lin = lineas.iloc[tmp]
		for g  in lin.geometry:
			ini,fin=Point(*g.coords[0]),Point(*g.coords[-1])
			self.ramaIni =  rama(tmp[0],ini if fin == self.punto else fin)

class rama:
	def __init__(self,id,pts):
		self.id = id
		self.punto = pts
		self.subramas = self.buscaSubramas()
	def buscaSubramas(self):
		setUsados(self.id)
		tmp = [idx for idx in  list(rtreeIdx.intersection(self.punto.bounds))  if idx not in usadas]
		print(tmp)
		ramTmp=[]
		if len(tmp)>0:
			lin = lineas.iloc[tmp]
			for  ir,l in  lin.iterrows():
				print(l)
				ini,fin = Point(*l.geometry.coords[0]),Point(*l.geometry.coords[-1])
				new_punto = ini if fin == self.punto else fin
				ramTmp.append(rama(ir,new_punto))
			return ramTmp
		return None



def build_arboles(puntos):
    arboles = []
    usadas = set()
    stack = []
    for i, row in puntos.iterrows():
        stack.append(Rama(i, row.geometry, usadas))
    while stack:
        rama_node = stack.pop()
        arboles.append(rama_node)
        if rama_node.subramas:
            stack.extend(rama_node.subramas)
    return arboles



def setUsados(id):
	usadas.append(id)
	print(usadas)

def indiceLineas(ruta,cant=None,campos=None):
	gdf = geo.read_file(ruta,rows=cant,columns=campos)
	idx =  rtree.index.Index()
	reng = [l.bounds for l in gdf.geometry]
	for  i , bbox in  enumerate(reng):
		idx.insert(i,bbox)
	return  idx, gdf

usadas=[]
rtreeIdx, lineas = indiceLineas("datos/corrientesAgua.shp",None,["geometry"])
puntos = geo.read_file("datos/puntos_dren.shp",columns=["geometry"])
arboles = []
for i,p in puntos.iterrows():
	arboles.append(puntoInicial(i,p.geometry))

print(arboles)
#a1 = arbol(1,[1,1])

