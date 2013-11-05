import colander
import deform

class AddressSchema(colander.MappingSchema):
    line1 = colander.SchemaNode(colander.String(), title='Address line 1')
    line2 = colander.SchemaNode(colander.String(), title='Address line 2', missing=None)
    line3 = colander.SchemaNode(colander.String(), title='Address line 3', missing=None)
    town = colander.SchemaNode(colander.String(), title='Town')
    postcode = colander.SchemaNode(colander.String(), title = 'Postcode')

class Business(AddressSchema):
    business_name = colander.SchemaNode(colander.String(), title='Business Name', insert_before='line1')

def inheritance_form(request):
    form = deform.Form(Business(), buttons=('submit',))
    if request.POST:
        submitted = request.POST.items()
        try:
            form.validate(submitted)
        except deform.ValidationFailure, e:
            return {'form': e.render()}
    return {'form': form.render()}
