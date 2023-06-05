import boto3


class Nube:
	def __init__(self, access_key_id, secret_access_key, session_token=None):
		"""
		Constructor de la clase Nube
		Args:
			access_key_id (String): Access key ID del usuario de conexión en AWS S3
			secret_access_key (String): Secret access key del usuario de conexión en AWS S3
			session_token (String): Session token del usuario de conexión en AWS S3
		"""
		try:
			self.access_key_id = access_key_id
			self.secret_access_key = secret_access_key
			self.session_token = session_token
			self.client = None
		except Exception as e:
			raise Exception("Error función Nube.__init__: " + str(e))
	
	def conectar_aws(self):
		"""
		Conectar cliente AWS S3
		"""
		try:
			self.client = boto3.client(
				service_name='s3',
				aws_access_key_id = self.access_key_id,
				aws_secret_access_key = self.secret_access_key,
				aws_session_token= self.session_token
			)
		except Exception as err:
			raise Exception("Error función Nube.conectar_aws: " + str(err))
	
	def cagar_archivo(self, ruta, llave, bucket):
		"""		
		Cargar un documento a AWS S3
		Args:
			ruta (String): con la ruta completa del archivo a cargar
			llave (String): llave del documento a cargar a AWS S3
			bucket (String): nombre del bucket donde se cargará el documento
		Returns:
			String: con el resultado de la carga
			String: descripción del error en caso de ocurrir
		"""
		try:
			if self.client is None:
				return "Falló", "No existe una conexión AWS"
			self.client.upload_file(ruta, bucket, llave)
			return "Exitosa", ""
		except Exception as err:
			return "Falló", str(err)