from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer

# Import app
from rest import app

#app.run()
WSGIServer((
    "0.0.0.0", # str(HOST)
    6000,  # int(PORT)
), app.wsgi_app).serve_forever()
