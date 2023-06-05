import googlemaps
import requests

class Mapa:
	def __init__(self, API_key, url_staticmap):
		"""
		Constructor de la clase Direccion
		"""
		self.API_key = API_key
		self.url_staticmap = url_staticmap
		self.gmaps = None
	
	def conectar_maps(self):
		"""
		Conectar cliente Google maps
		"""
		self.gmaps = googlemaps.Client(key=self.API_key)
	
	def coordenadas_direcciones(self, direcciones):
		"""
		Determina las coordenadas de latitud y longitud una dirección
		Args:	
			direcciones (String): lista de direcciones para buscar las coordenadas
		Returns:
			String: con el resultado de las coordenadas de las direcciones
			String: descripción del error en caso de ocurrir
		"""
		try:
			coordenadas = []
			spli_dirs = direcciones.split("|")
			for dir in spli_dirs:
				geocode_result = self.gmaps.geocode(dir + ", Colombia")				
				if len(geocode_result) > 0:
					lat = geocode_result[0]['geometry']['location']['lat']
					lng = geocode_result[0]['geometry']['location']['lng']
					coordenada = str(lat) + "," + str(lng)
					coordenadas.append(coordenada)					
			coordenadas_str = "|".join(coordenadas)
			return coordenadas_str, ""
		except Exception as err:
			return "Falló coordenadas", str(err)
	
	def pintar_mapa(self, ruta, coordenadas, index):
		"""
		Determina las coordenadas de latitud y longitud una dirección
		Args:
			ruta (String): Carpeta donde se guardará el mapa
			coordenadas (String): lista de coordenadas a pintar
			index (int): index de la fila del dataframe resultado
		Returns:
			String: con la ruta del mapa
			String: descripción del error en caso de ocurrir
		"""
		try:
			spli_coordenadas = coordenadas.split("|")
			if len(spli_coordenadas) > 0:
				i = 1
				url = self.url_staticmap
				for coordenada in spli_coordenadas:
					marker = "&markers=label:" + str(i) + "|" + coordenada
					url = url + marker
					i = i + 1
				url = url + "&key=" + self.API_key
				f = open(ruta + '/static'+str(index)+'.png','wb')
				f.write(requests.get(url).content)
				f.close()
				return f.name, ""
		except Exception as err:
			return "Falló Mapa", str(err)
