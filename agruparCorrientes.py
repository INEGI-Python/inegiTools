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
		tmp["id"] = tmp.index+1
		tmp["start"]=tmp.geometry.apply(lambda x: Point(*x.coords[0]))
		tmp["end"]=tmp.geometry.apply(lambda x: Point(*x.coords[-1]))
		tmp["grupo"]=-1
		tmp["orden"]=-1
		tmp["flip"]=-1
		tmp.set_index("id",inplace=True)
		self.CRS = tmp.crs.to_string()
		self.lineas = tmp.to_dict("index")
		self.rtreeIdx = self.indiceLineas(tmp)
		
	def indiceLineas(self,gdf):
		idx =  rtree.index.Index()
		reng = [l.bounds for l in gdf.geometry]
		for  i , bbox in  enumerate(reng):
			idx.insert(i,bbox)
		return  idx

	def aguasArriba(self,id,gpo):
		sub = list(self.rtreeIdx.intersection(self.lineas[id]["start"].bounds))
		print(sub)
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
		tmp["id"] = tmp.index+1
		tmp.set_index("id",inplace=True)
		tmp["linea"]=[list(h.rtreeIdx.intersection(p.bounds)) for p in tmp.geometry]
		self.puntos=tmp.to_dict("index")
		self.CRS =  tmp.crs.to_string()
		
		# for pos in tmp.index:
		# 	if tmp.loc[pos:"geometry"].distance(h.lineas[pos]["end"]) > 0:
		# 		h.lineas[pos]["geometry"]=LineString(h.lineas[pos]["geometry"].coords[::-1])
		# 		h.lineas[pos]["flip"]=1
		# 	else:
		# 		h.lineas[pos]["flip"]=3
		# 	h.lineas[pos]["grupo"]=pos
		# 	h.lineas[pos]["orden"]=1
		# 	self.puntos.append(tmp)


hidro = corrientes(tipo="LINESTRING",ruta="datos/new_hidro.shp")
puntos = puntoInicial(tipo="POINT",ruta="datos/new_renaje.shp",hidro=hidro)
arboles=[]

for i,a in puntos.puntos.values():
	print(i,a)
	arboles.extend(hidro.aguasArriba(a["linea"],i))

print(len(arboles))

misLineas = hidro.lineas
misPuntos = puntos.puntos

