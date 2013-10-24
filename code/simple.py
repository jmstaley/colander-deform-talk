import colander
import deform

class Contact(colander.Schema):
    email = colander.SchemaNode(colander.String())
    name = colander.SchemaNode(colander.String())
    message = colander.SchemaNode(colander.String())

def simple_form(request):
    form = deform.Form(Contact(), buttons=('submit',))
    return {'form': form.render()}

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

if __name__ == '__main__':
    import os
    path = os.path.abspath('templates/simple.pt')
    config = Configurator()
    config.add_route('simple_form', '/')
    config.add_view(simple_form, renderer=path, route_name='simple_form')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
   


