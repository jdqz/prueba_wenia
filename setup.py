from setuptools import setup
from setuptools import find_packages
from glob import glob
from os.path import splitext
from os.path import basename

setup(
    name = 'proyecto-wenia',
    description = 'Prueba técnica Operaciones Wenia',
	version = '0.0.1',
    author = 'John Dairo Quintero Zuluaga',
    author_email = 'jdquinte@bancolombia.com.co',
    url = 'https://github.com/jdqz/prueba_wenia.git',
    license = '...',
    packages = find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    install_requires = [
        'boto3',
		'pandas',
		'openpyxl',
		'pandas',
		'PyPDF2',
		'googlemaps'
    ],
    include_package_data = True   
)
