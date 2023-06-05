from .archivo import Archivo
from .pk_aws.nube import Nube
from .pk_direcciones.direccion import Direccion
from .pk_google.mapa import Mapa
import os
import json
import logging
import pkg_resources


LOG_FILENAME = "logging.out"
logging.basicConfig(
	filename=LOG_FILENAME,
	level=logging.INFO,
	format="%(asctime)s %(levelname)-8s %(message)s",
	datefmt="%Y-%m-%d %H:%M:%S"
)


def obtener_parametros(ruta):
	"""
	Obtiene las variables del archivo de configuración
	Returns:
		json: con la lista de parámetros de configuración
	"""
	infile = ""
	try:
		with open(f'{ruta}/config/config.json', encoding="utf-8") as infile:
			return json.load(infile)
	except Exception as err:
		raise Exception("Error función obtener_parametros: " + str(err))

def obtener_raiz():
	"""
	Obtiene la ruta raíz del proyecto
	Returns:
		String: con la ruta completa hasta la carpeta src
	"""
	return pkg_resources.resource_filename(__name__, 'static')
	
def carpeta_resultados(ruta):
	"""
	Obtiene la ruta donde se guardaran los resultados del procesamiento
	Returns:
		String: con la ruta donde guardar los resultados
	"""
	if os.path.exists(ruta):
		if os.path.isfile(ruta):
			dirname, basename = os.path.split(ruta)
			return dirname
		else:
			return ruta	
	return None

def main():
	#Obtener el o los archivos a procesar
	ruta = input("Ingrese la ruta o el archivo: ")
	ruta_resultado = carpeta_resultados(ruta)
	if ruta_resultado:
		#Ubicación del proyecto
		raiz = obtener_raiz()
		#Parametros del archivo config
		params = obtener_parametros(raiz)
		
		#Busacar archivos
		archivo = Archivo()
		resultado = archivo.cagar_archivos(ruta, params["extensions"])
		
		
		#Conectar a la nube
		nube = Nube(params["Access_key_ID"],params["Secret_access_key"])
		nube.conectar_aws()
		#Caragar archivos a la nube
		for index, row in resultado.iterrows():
			anotaciones = row["Anotaciones"]
			if anotaciones == "":
				archivo = row["Archivo"]
				key = os.path.basename(archivo).split('/')[-1]
				re, err = nube.cagar_archivo(archivo, key, params["bucket_name"])
				resultado.at[index,"Key"] = key
				resultado.at[index,"Carga AWS"] = re
				resultado.at[index,"Anotaciones"] = err
		
		#Extraer Direcciones
		direccion = Direccion()
		for index, row in resultado.iterrows():
			anotaciones = row["Anotaciones"]
			if anotaciones == "":
				archivo = row["Archivo"]
				dir, err = direccion.extraer_direccion_pdf(archivo)
				resultado.at[index,"Direccion"] = dir
				resultado.at[index,"Anotaciones"] = err
		
		#Direcciones homónimas
		for index, row in resultado.iterrows():
			anotaciones = row["Anotaciones"]
			if anotaciones == "":
				dir = row["Direccion"]
				homonimas, err = direccion.direcciones_homonimas(dir)
				resultado.at[index,"Homonimas"] = homonimas
				resultado.at[index,"Anotaciones"] = err
		
		#Direcciones similitud del 90%
		for index, row in resultado.iterrows():
			anotaciones = row["Anotaciones"]
			if anotaciones == "":
				dir = row["Direccion"]
				homo = row["Homonimas"]
				homonimas_90, err = direccion.similitud_homonimas(dir, homo)
				resultado.at[index,"Homonimas 90"] = homonimas_90
				resultado.at[index,"Anotaciones"] = err
		
		#Coordenadas direcciones
		mapa = Mapa(params["API_key_Google"],params["URL_API_staticmap"])
		mapa.conectar_maps()
		for index, row in resultado.iterrows():
			anotaciones = row["Anotaciones"]
			if anotaciones == "":
				dir = row["Homonimas 90"]
				coordenadas, err = mapa.coordenadas_direcciones(dir)
				resultado.at[index,"Coordenadas"] = coordenadas
				resultado.at[index,"Anotaciones"] = err
		
		#pintar mapa
		for index, row in resultado.iterrows():
			anotaciones = row["Anotaciones"]
			if anotaciones == "":
				coordenadas = row["Coordenadas"]
				map, err = mapa.pintar_mapa(ruta_resultado, coordenadas, index)
				resultado.at[index,"Mapa"] = map
				resultado.at[index,"Anotaciones"] = err
		
		#Exportar resultados procesamiento
		resultado.to_excel(ruta_resultado + "/resultado.xlsx",index=True)
	else:
		print("La ruta no existe")

if __name__ == '__main__':
	main()
