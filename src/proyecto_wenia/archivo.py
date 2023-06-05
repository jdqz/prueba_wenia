import os
import pandas
from .pk_aws.nube import Nube


class Archivo:
	def __init__(self):
		"""
		Constructor de la clase Archivo
		"""
	
	def cagar_archivos(self, ruta, extensions):
		"""
		Cargar uno o varios documentos a AWS S3
		Args:
			ruta (String): con la ruta completa de la carpeta donde están los documentos o un archivo especifico
			extensions (list String): lista con las extensiones habilitadas para cargar
		Returns:
			DataFrame: con el resultado de los archivos procesados
		"""
		try:
			ruta = ruta.replace("\\","/")
			if os.path.exists(ruta):
				df = pandas.DataFrame(columns = ["Archivo", "Carga AWS", "Key", "Direccion", "Homonimas", "Homonimas 90", "Coordenadas", "Mapa", "Anotaciones"])
				if os.path.isfile(ruta):
					#Cuando la ruta representa un solo archivo se ejecuta este bloque de código
					key = os.path.basename(ruta).split('/')[-1]
					ext = os.path.splitext(ruta)[-1].lower()
					resultado = {"Archivo":ruta, "Carga AWS":"", "Key":"", "Direccion":"", "Homonimas":"", "Homonimas 90":"", "Coordenadas":"", "Mapa":"", "Anotaciones":""}
					if ext not in extensions:						
						resultado["Anotaciones"] = "No se admite la extensión " + ext + " del archivo"
					new_row = pandas.DataFrame([resultado])
					df = pandas.concat([df, new_row],ignore_index=True)
				else:
					if os.path.isdir(ruta):
						#Cuando la ruta representa una carpeta con múltiples archivos se ejecuta este bloque de código
						for path, subdirs, files in os.walk(ruta):
							path = path.replace("\\","/")
							directory_name = path.replace(ruta,"")						
							for file in files:
								path_b = os.path.join(path, file).replace("\\","/")
								resultado = {"Archivo":path_b, "Carga AWS":"", "Key":"", "Direccion":"", "Homonimas":"", "Homonimas 90":"", "Coordenadas":"", "Mapa":"", "Anotaciones":""}
								ext = os.path.splitext(file)[-1].lower()
								if ext not in extensions:
									resultado["Anotaciones"] = "No se admite la extensión " + ext + " del archivo"
								new_row = pandas.DataFrame([resultado])
								df = pandas.concat([df, new_row],ignore_index=True)
				return df
			else:
				raise Exception("Error función Archivo.cagar_archivos: La ruta " + ruta + ", no existe")
		except Exception as err:
			raise Exception("Error función Archivo.cagar_archivos: " + str(err))