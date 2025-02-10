import geopandas as geo
from shapely.geometry import Point,LineString
import rtree



class corrientes(object):
	def __init__(self,**a):
		self.lineas = []
		self.CRS=None
		self.tipo=a["tipo"]
		self.rtreeIdx = None
		self.importar(a["ruta"])

	def importar(self,ruta):
		tmp = geo.read_file(ruta,columns=["geometry"])
		self.CRS = tmp.crs.to_string()
		for i,l in tmp.iterrows():
			lin=dict(id=i+1,geometry=l.geometry,start=Point(*l.geometry.coords[0]),end=Point(*l.geometry.coords[-1]),grupo=-1,orden=-1,flip=-1)
			self.lineas.append(lin)
		self.rtreeIdx = self.indiceLineas(tmp)
		
	def indiceLineas(self,gdf):
		idx =  rtree.index.Index()
		reng = [l.bounds for l in gdf.geometry]
		for  i , bbox in  enumerate(reng):
			idx.insert(i,bbox)
		return  idx

	def aguasArriba(self,id,gpo):
		sub = list(self.rtreeIdx.intersection(self.lineas[id]["start"].bounds))
		ramas,res = [self.lineas[i]["id"] for i in sub if self.lineas[i]["id"] != id],[]
		if len(ramas)==0:
			return self.lineas[id]["id"]
		for s in sub:
			self.lineas[s]["grupo"] = gpo
			self.lineas[s]["orden"] = self.lineas[id]["orden"]+1
			if self.lineas[id]["start"].distance(self.lineas[s]["end"]) > 0:
				self.lineas[s]["geometry"] = LineString(self.lineas[s]["geometry"].coords[::-1])
				self.lineas[s]["flip"] = 1
			else:
				self.lineas[s]["flip"] = 0
			res.append(self.aguasArriba(s,gpo))
		return res
class puntoInicial(object):
	def __init__(self,**a):
		self.puntos=[]
		self.CRS=None
		self.tipo=a["tipo"]
		self.importar(a["ruta"],a["hidro"])

	def importar(self,ruta,h):
		tmp = geo.read_file(ruta,columns=["geometry"])
		self.CRS = tmp.crs.to_string()
		for i,p in tmp.iterrows():
			pun=dict(id=i+1,geometry=p.geometry,linea=list(h.rtreeIdx.intersection(p.geometry.bounds))[0])
			if pun["geometry"].distance(h.lineas[pun["linea"]]["end"]) > 0:
				h.lineas[pun["linea"]]["gemeotry"]=LineString(h.lineas[pun["linea"]]["geometry"].coords[::-1])
				h.lineas[pun["linea"]]["flip"]=1
			else:
				h.lineas[pun["linea"]]["flip"]=3
			h.lineas[pun["linea"]]["grupo"]=pun["id"]
			h.lineas[pun["linea"]]["orden"]=1
			self.puntos.append(pun)


hidro = corrientes(tipo="LINESTRING",ruta="datos/corrientesAgua.shp")
puntos = puntoInicial(tipo="POINT",ruta="datos/puntos_dren.shp",hidro=hidro)
arboles=[h["id"]  for h in hidro.lineas]
arch = open("datos/arboles.txt","w")	
arch.write(str(arboles))
arch.close()

for p in puntos.puntos:
	arboles.extend(hidro.aguasArriba(p["linea"],p["id"]))

print(len(arboles))

misLineas = hidro.lineas[:150]
misPuntos = puntos.puntos[:150]

