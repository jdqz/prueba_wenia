from proyecto_wenia.pk_aws.nube import Nube
from proyecto_wenia.pk_direcciones.direccion import Direccion
from proyecto_wenia.pk_google.mapa import Mapa
import os
import unittest

class Test(unittest.TestCase):
  
	def test_carga_aws(self):
		"""
		Validar que se pueda cargar un archivo a WAS S3.
		"""
		archivo = open("./insumos/Documento 1.pdf")
		archivo =  os.path.realpath(archivo.name)
		nube = Nube("AKIAT45AYBYW5K23QZUE","IVwUyW+gsLHskqQpdI8REK6egPZABzytA1StzrEh")
		nube.conectar_aws()
		key = os.path.basename(archivo).split('/')[-1]
		re, err = nube.cagar_archivo(archivo, key, "bucketjdqzwenia")
		self.assertEqual(re, "Exitosa")
		
	
	def test_encontar_direccion_pdf(self):
		"""
		Validar que se pueda extraer la dirección de un archivo .PDF.
		"""
		archivo = open("./insumos/Documento 1.pdf")
		archivo =  os.path.realpath(archivo.name)
		dir_compara = "Carrera 33 # 21 - 5"
		direccion = Direccion()
		dir, err = direccion.extraer_direccion_pdf(archivo)
		self.assertEqual(dir, dir_compara)	
	
	
	def test_coordenadas(self):
		"""
		Validar que se pueda encontrar las coordenadas de una dirección.
		"""
		dir = "Carrera 33 # 21 - 5"
		coor_compara = "10.9705291,-74.7765483"
		mapa = Mapa("AIzaSyDPfPx_Sz1SkZyKJxZTZ0vEfTvjrWXA7mY","")
		mapa.conectar_maps()		
		coordenadas, err = mapa.coordenadas_direcciones(dir)
		self.assertEqual(coordenadas, coor_compara)

if __name__ == '__main__':
	unittest.main()

	