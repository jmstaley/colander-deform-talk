import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import UnencryptedCookieSessionFactoryConfig

from simple import simple_form
from custom_templates import contact_form
from custom_validators import validators_form
from defered_validator import defered_form
from inheritance import inheritance_form

if __name__ == '__main__':
    path = os.path.abspath('templates/simple.pt')

    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config = Configurator(session_factory = my_session_factory)

    config.add_route('simple_form', '/1')
    config.add_route('inheritance', '/2')
    config.add_route('validators', '/3')
    config.add_route('defered', '/4')
    config.add_route('custom', '/5')

    config.add_view(simple_form, renderer=path, route_name='simple_form')
    config.add_view(inheritance_form, renderer=path, route_name='inheritance')
    config.add_view(validators_form, renderer=path, route_name='validators')
    config.add_view(defered_form, renderer=path, route_name='defered')
    config.add_view(contact_form, renderer=path, route_name='custom')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
