from pyInegi.generalizacion import webMap
import geopandas as geo
import matplotlib.pyplot as plt

     

corrientes = geo.read_file("datos/corrientes_250.gdb",layer="Corrientes_Corregidas_Copy",columns=["geometry"],rows=100)
corrientes['id']=corrientes.index+1
corrientes['flip']=0
corrientes.to_file("datos/tmp1.shp")

pts_dren = geo.read_file("datos/corrientes_250.gdb",layer="puntos_dren",columns=["geometry"],rows=100)
pts_dren['id']=pts_dren.index+1
pts_dren.to_file("datos/tmp2.shp")
 
  
webMap.WebMAP(datos=["datos/tmp1.shp","datos/tmp2.shp"],tipos=["LINESTRING","POINT"],names=["Corrientes de Agua","puntos de drenage"],color=["blue","red"],web=1)
plt.show()
