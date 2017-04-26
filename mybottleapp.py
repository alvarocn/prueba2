from bottle import route, default_app, get, post, run, template, error, request, static_file, response
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

key="5e540fc0e14e6863f1d69c5a15880c4a"
url_base="https://api.flickr.com/services/rest"

#ruta index
@route('/')
def index():
	return template('index')

#ruta busqueda
@route('/busqueda',method='POST')
def busqueda():

#Request de url de fotos
	nombre=request.forms.get('foto')
	payload={'method':'flickr.photos.search','api_key':key,'text':nombre,'extras':'url_o,url_s','format':'json'}
#EJEMPLO DE URL:
# https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=3e43ddf68638ce426d5e4aae08250ea4&text=arbol&extras=url_o&format=json
	r=requests.get(url_base,params=payload)
	lista=[]
	lista1=[]
	
	print r.url
	if r.status_code==200:
		doc = json.loads(r.text[14:-1])
		#print doc
#Obtener URL de fotos:
		for x in doc["photos"]["photo"]:
			if x.has_key("url_o"):
				lista.append([x['url_s'],x["url_o"]])
#Obtener IDS de fotos:
		for i in doc["photos"]["photo"]:
			if i.has_key("id"):
				lista1.append(i['id'])
				
#		print lista
		return template("busqueda.tpl",info=lista,ids=lista1)

#ruta detalles
@route ('/detalles/<id>')
def detalles(id):
#Obtener ids geolocalizacion	
	tienemapa=False
	payload3={'method':'flickr.photos.geo.getLocation','api_key':key,'photo_id':id,'format':'json'}
	#EJEMPLO URL:
	#https://api.flickr.com/services/rest/?method=flickr.photos.geo.getLocation&api_key=77e3791687c77867f657da988a6637ef&photo_id=3231279723&format=json
	r3=requests.get(url_base,params=payload3)
	
	if r3.status_code==200:
		doc3 = json.loads(r3.text[14:-1])
		if doc3.has_key('photo'):
			if doc3['photo'].has_key('location'):
				tienemapa=True
	
	payload1={'method':'flickr.photos.getExif','api_key':key,'photo_id':id,'format':'json'}
#EJEMPLO URL:
#https://api.flickr.com/services/rest/?method=flickr.photos.getExif&api_key=01480c276d9e03abc8cb4e2273450144&photo_id=26952354992&format=json
	r1=requests.get(url_base,params=payload1)
	lista2=[]
	lista_info=[]
	lista_label=["Orientation","Software","Exposure","Aperture","ISO Speed","Date and Time (Original)","Flash","Saturation"]
	lista_label_esp=["Orientacion","Software","Exposure","Apertura","ISO","Fecha","Flash","Saturacion"]
	
	if r1.status_code==200:
		doc1 = json.loads(r1.text[14:-1])

		if doc1.has_key('photo'):

		#print doc1
#Obtener detalles camara
			if doc1['photo'].has_key('camera'):
				if not len(doc1['photo']['camera']) <= 2:
					fich = doc1['photo']['camera']
				else:
					fich = 'La imagen no contiene informacion de la camara'
		
#Obtener caracteristicas de fotos
			for info in doc1['photo']['exif']:
				if info['label'] in lista_label:
					lista_info.append(info['raw']['_content'])

		else:
			fich = 'No hay informacion'

	return template('detalles.tpl',camara=fich,labels=lista_label_esp,info=lista_info,mapa=tienemapa,id=id)

#ruta mapa geografico
@route("/mapa/<id>")
def mapa(id):
	payload2={'method':'flickr.photos.geo.getLocation','api_key':key,'photo_id':id,'format':'json'}
#EJEMPLO URL:
#https://api.flickr.com/services/rest/?method=flickr.photos.geo.getLocation&api_key=77e3791687c77867f657da988a6637ef&photo_id=3231279723&format=json
	r2=requests.get(url_base,params=payload2)
	lista3=[]
	id_geo=[]
	print r2.url
	if r2.status_code==200:
		doc2 = json.loads(r2.text[14:-1])
		#print doc2

#Obtener latitud y longitud
		if doc2.has_key('photo'):
			if doc2['photo'].has_key('location'):

				lista3.append([float(doc2["photo"]["location"]["latitude"]),float(doc2["photo"]["location"]["longitude"])])

	return template("mapa.tpl",ubicaciones=lista3)

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.environ['OPENSHIFT_REPO_DIR']+"static")

# This must be added in order to do correct path lookups for the views
import os
from bottle import TEMPLATE_PATH
TEMPLATE_PATH.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi/views/')) 

application=default_app()