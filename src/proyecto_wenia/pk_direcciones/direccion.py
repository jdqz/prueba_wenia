import PyPDF2
import re
from difflib import SequenceMatcher

class Direccion:
	def __init__(self):
		"""
		Constructor de la clase Direccion
		"""
		self.dirs = ["Calle","Carrera","CRA","Diagonal","Kra","Trasversal"]
		self.nums = ["Nro","Numero","#","Num"]
	
	def extraer_direccion_pdf(self, ruta):
		"""
		Extraer dirección del cliente en un PDF por medio de una expresión regular
		Args:	
			ruta (String): con la ruta completa del archivo PDF
		Returns:
			String: con el resultado de la extracción de la dirección
			String: descripción del error en caso de ocurrir
		"""
		try:
			pdfFileObj = open(ruta,'rb')
			pdfReader = PyPDF2.PdfReader(pdfFileObj)
			num_pages = len(pdfReader.pages)
			count = 0
			text = ""
			
			while count < num_pages:
				pageObj = pdfReader.pages[count]
				count +=1
				text += pageObj.extract_text()
			
			dirs_str = "|".join(self.dirs)
			nums_str = "|".join(self.nums)
			
			p = re.compile(r'(?:'+dirs_str+')[\s]+[\d]+(?:[\s]+|[a-z][\s]+)(?:'+nums_str+')[\s]*[\d]+(?:[\s]*[a-z][\s]*-[\s]*|[\s]*[a-z][\s]+|[\s]*-[\s]*|[\s]+)[\d]+', flags=re.IGNORECASE)
			x = p.findall(text)
			return "|".join(x), ""
		except Exception as err:
			return "Falló extracción", str(err)

	def direcciones_homonimas(self, direccion):
		"""
		Detarminar las direcciones homónimas en base a un direccion origial
		Args:	
			direccion (String): direccion origial para calcular homónimos
		Returns:
			String: con el resultado de las direcciones homónimas
			String: descripción del error en caso de ocurrir
		"""
		try:
			spli_dirs = direccion.split("|")
			homonimas = []
			for spli_dir in spli_dirs:
				
				found_dir = None
				for dir in self.dirs:
					result = spli_dir.lower().find(dir.lower())
					if result != -1:
						found_dir = spli_dir[result:result+len(dir)]
				
				found_num = None
				for num in self.nums:
					result = spli_dir.lower().find(num.lower())
					if result != -1:
						found_num = spli_dir[result:result+len(num)]
				
				for dir in self.dirs:
					for num in self.nums:
						spli_dir_copy = spli_dir
						diferente_dir = False
						if found_dir is not None and found_dir.lower() != dir.lower():
							spli_dir_copy = spli_dir.replace(found_dir,dir)
							diferente_dir = True
						if found_num is not None and found_num.lower() != num.lower():
							spli_dir_copy = spli_dir.replace(found_num,num)
							diferente_dir = True
						if diferente_dir:
							homonimas.append(spli_dir_copy)			
			homonimas_str = "|".join(homonimas)
			return homonimas_str, ""			
		except Exception as err:
			return "Falló homónimas", str(err)
			
	def similitud_homonimas(self, direccion, homonimas):
		"""
		Compara la dirección original del documento y las direcciones homónimas
		Args:	
			direccion (String): dirección origial
			homonimas (String): direcciones homónimas
		Returns:
			String: con el resultado de las direcciones homónimas con similitud mayor al 90%
			String: descripción del error en caso de ocurrir
		"""
		try:
			spli_dirs = direccion.split("|")
			spli_homo = homonimas.split("|")
			homonimas_90 = []
			for dir in spli_dirs:
				spli_dir = dir.lower().split(" ")
				len_dir = len(spli_dir)
				for homo in spli_homo:
					hom = homo.lower().split(" ")
					len_hom = len(hom)
					i = 0
					if len_hom == len_dir:
						exactas = 0
						casi_exactas = 0
						while i < len_hom:
							porcentaje = SequenceMatcher(a=hom[i], b=spli_dir[i]).ratio()
							if porcentaje == 1:
								exactas += 1
							else: 
								casi_exactas = porcentaje
							i += 1
						if exactas + 1 == len_hom and casi_exactas > 0.3:
							homonimas_90.append(homo)
					
			homonimas_90_str = "|".join(homonimas_90)
			return homonimas_90_str, ""
		except Exception as err:
			return "Falló similitud", str(err)
