from bottle import route, default_app, get, post, run, template, error, request, static_file, response
import requests
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#key de la aplicacion flickr
key="3d81dc5d3e3b814c444aedf077d52c1a"
url_base="https://api.flickr.com/services/rest"
@route('/')
def index():
	return template('index')

#ruta busqueda
@route('/busqueda',method='POST')
def busqueda():
#variables de busqueda de la aplicacion
	nombre=requests.forms.get('foto')
	payload={"method":"flickr.tags.getListPhoto","api_key":key,"text":nombre,"extras":"url_o,url_s","format":"json"}
	r=requests.get(url_base,params=payload)
	lista_url=[]
	codigo_foto=[]
	print r.url
#como empieza por "jsonFlickrApi(" y termina en "( " tenemos que empezar a contar desde despues del parentesis
	if r.status_code==200:
		doc = json.loads(r.text[14:-1])
		for f in doc["photos"]["photo"]:
			if f.has_key("url_o"):
				lista_url.append([f['url_s'],x["url_o"]])
#Obtener IDS de fotos:
		for p in doc["photos"]["photo"]:
			if p.has_key("id"):
				codigo_foto.append(p['id'])
		
				
#		print lista
		return template("buscado.tpl",info=lista_url,ids=codigo_foto)

#ruta detalles
@route ('/informacion/<id>')
def informacion(id):
#Obtener ids de foto
	nombre=request.forms.get('tag')
	payload2={'method':'flickr.tags.getListPhoto','api_key':key,'photo_id':id,'format':'json'}
	r2=requests.get(url_base,params=payload)
	codigo_foto2=[]
	tag_foto=[]
##tag https://api.flickr.com/services/rest/?method=flickr.tags.getListPhoto&api_key=3d81dc5d3e3b814c444aedf077d52c1a&photo_id=3231279723&format=json
	if r.status_code==200:
		doc = json.loads(r.text[14:-1])
		for c in doc["photos"]["photo"]:
			if c.has_key("id"):
				
				codigo_foto2.append(c["id"])
#Obtener tag de fotos:
		for q in doc["photos"]["tags"]:
			if q.has_key("tag"):
				tag_foto.append(q['raw'])
@route ('/comentario/<content')
def comentario(content):
	nombre3=request.forms.get('lista')
	payload3={'method':'flickr.photos.comments.getList','api_key':key,'photo_id':id, 'format':'json'}
	r2=requests.get(url_base,params=payload)
	codigo_foto3=[]
	comentarios_foto=[]
	if r.status_code==200:
		doc = json.loads(r.text[14:-1])
		for m in doc["comments"]["comment"]:
			if m.has_key("id"):
				codigo_foto3.append(m["id"])
		for t in doc["comments"]["comment"]:
			if t.has_key("content"):
				comentario.append(t['content'])
		return template("comentado.tpl",info=codigo_foto3,contendio=comentario)


#localizar
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

