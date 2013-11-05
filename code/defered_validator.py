import colander
import deform

@colander.deferred
def deferred_csrf_default(node, kw):
    request = kw.get('request')
    csrf_token = request.session.get_csrf_token()
    return csrf_token

@colander.deferred
def deferred_csrf_validator(node, kw):
    def validate_csrf_token(node, value):
        request = kw.get('request')
        csrf_token = request.session.get_csrf_token()
        if value != csrf_token:
            raise colander.Invalid(node, 'Bad CSRF token')
    return validate_csrf_token

class CSRFSchema(colander.Schema):
    csrf = colander.SchemaNode(
        colander.String(),
        default = deferred_csrf_default,
        validator = deferred_csrf_validator,
        widget = deform.widget.HiddenWidget(),
        )

class Contact(CSRFSchema):
    email = colander.SchemaNode(colander.String(), validator=colander.Email())
    name = colander.SchemaNode(colander.String())
    message = colander.SchemaNode(colander.String(),
                                  widget=deform.widget.TextAreaWidget())

def defered_form(request):
    schema = Contact().bind(request=request)
    form = deform.Form(schema, buttons=('submit',))
    if request.POST:
        submitted = request.POST.items()
        try:
            form.validate(submitted)
        except deform.ValidationFailure, e:
            return {'form': e.render()}
        return {'form': None}
    return {'form': form.render()}

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import UnencryptedCookieSessionFactoryConfig

if __name__ == '__main__':
    import os
    path = os.path.abspath('templates/simple.pt')
    my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
    config = Configurator(session_factory = my_session_factory)
    config.add_route('simple_form', '/')
    config.add_view(defered_form, renderer=path, route_name='simple_form')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
   


