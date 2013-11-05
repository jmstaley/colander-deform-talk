import colander
import deform

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
