import os
from pkg_resources import resource_filename

import colander
import deform

deform_path = os.path.abspath('templates/deform')
deform_templates = resource_filename('deform', 'templates')
search_path = (deform_path, deform_templates)
renderer = deform.ZPTRendererFactory(search_path)

class Contact(colander.MappingSchema):
    email = colander.SchemaNode(colander.String(), validator=colander.Email())
    name = colander.SchemaNode(colander.String())
    message = colander.SchemaNode(colander.String(),
                                  widget=deform.widget.TextAreaWidget())

def contact_form(request):
    form = deform.Form(Contact(), buttons=('submit',), renderer=renderer)
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
