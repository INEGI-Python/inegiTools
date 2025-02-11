import geopandas as geo	
from shapely.geometry import Point,LineString,Polygon
import rtree
import os
import sys
import json
import argparse
import logging

def main():
	parser = argparse.ArgumentParser(description="Convertir archivo de texto a shapefile")
	parser.add_argument("origen",help="origen del archivo de origen, puede ser un shape, geojson o csv")
	parser.add_argument("geom",help="Tipo de geometria a convertir",choices=["linea","punto"])
	parser.add_argument("salida",help="origen del archivo de salida.shp")
	args = parser.parse_args()
	if not os.path.exists(args.origen):
		logging.error("No se encontro el archivo de origen")
		sys.exit(1)
	convertir(args.origen,args.salida,args.geom)
	logging.info("Archivo convertido exitosamente")



def convertir(origen,salida,tipo):
	data = geo.read_file(origen,columns=["geometry"])
	crs = data.crs.to_string()
	datos=[{"id":i+1,"geometry":d} for i,d in enumerate(data.geometry)]
	gdf = geo.GeoDataFrame(data=datos,crs=crs)
	gdf.set_index("id",inplace=True)
	gdf.to_file(salida)




if __name__ == "__main__":
	main()