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
