import os
from pkg_resources import resource_filename

import colander
import deform

deform_path = os.path.abspath('templates/deform')
deform_templates = resource_filename('deform', 'templates')
search_path = (deform_path, deform_templates)
deform.Form.set_zpt_renderer(search_path)

class Contact(colander.MappingSchema):
    email = colander.SchemaNode(colander.String(), validator=colander.Email())
    name = colander.SchemaNode(colander.String())
    message = colander.SchemaNode(colander.String(),
                                  widget=deform.widget.TextAreaWidget())

def simple_form(request):
    form = deform.Form(Contact(), buttons=('submit',))
    if request.POST:
        submitted = request.POST.items()
        try:
            form.validate(submitted)
        except deform.ValidationFailure, e:
            return {'form': e.render()}
    data = {'email': 'jon.staley@fundingoptions.com',
             'name': 'Jon',
             'message': 'Hello World'}
    return {'form': form.render(data)}

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

if __name__ == '__main__':
    path = os.path.abspath('templates/simple.pt')

    config = Configurator()
    config.add_route('simple_form', '/')
    config.add_view(simple_form, renderer=path, route_name='simple_form')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
   


