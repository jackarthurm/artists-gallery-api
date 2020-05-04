from waitress import serve
from gallery_api.wsgi import application

serve(application, port=8000, url_scheme='https')
