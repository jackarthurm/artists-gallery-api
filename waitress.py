from gallery_api.wsgi import application

waitress.serve(application, port=8000, url_scheme='https')
