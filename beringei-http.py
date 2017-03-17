from bottle import Bottle,run, route, request, default_app, HTTPResponse, response
from ConfigParser import SafeConfigParser
from common import Beringei 
import logging
from json import dumps
import os,sys,time

# logger
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logging.debug("logging started")
logger = logging.getLogger(__name__)
# current working directory
here = os.path.dirname(__file__)
# Config Parsing
config = SafeConfigParser()
config.read('config.ini')
# uWSGI
app = application = Bottle()
beringe = Beringei(config)

#/ping
@route('/ping',method='GET')
def ping():
	return 'pong@%d' %(int(time.time()))

#/get?KEY=keyname&SORTED=1&ASC=1
@route('/get',method='GET')
def get_key():
    key=request.query.get('KEY',None)
    options=request.query.get('OPTIONS','')
    sort=bool(int(request.query.get('SORTED',0)))
    asc=bool(int(request.query.get('ASC',0)))
    if not key: return HTTPResponse(status=400,body=dumps({'status' : 'error : key is null'}))
    data = beringe.get_key(OPTIONS=options,KEY=key,sort=sort,asc=asc)
    if data : return HTTPResponse(status=200,body=data)
    else : return HTTPResponse(status=500,body=dumps({'status' : 'error : internal server error'}))        

#/put?KEY=keyname&VALUE=80808&
@route('/put',method='POST')
def set_key():
    key=request.forms.get('KEY',None)
    value=request.forms.get('VALUE',None)
    options=request.forms.get('OPTIONS','')
    if not key or not value: 
        return HTTPResponse(status=400,body=dumps({'status' : 'error : key or value is null'}))    
    if beringe.put_key(OPTIONS=options,KEY=key,VALUE=value):
        return HTTPResponse(status=200,body={'status' : 'ok'})
    else:
        return HTTPResponse(status=500,body=dumps({'status' : 'error : internal server error'}))

if __name__ == "__main__" :
    run(host=config.get('bottle','host'), port=config.get('bottle','port'))
else:
    application = default_app()