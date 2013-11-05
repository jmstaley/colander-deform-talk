!SLIDE
# 'king Forms 

!SLIDE
## Overview
* What is Deform?
* What is Colander?
* A simple form
* In production

!SLIDE
## What is Deform?

* Form generation
{: .slide }
* Form widgets
{: .slide }
* Ajax forms
{: .slide }
* Uses Colander for schemas
{: .slide }
* Uses Chameleon for templating\*
{: .slide }

\* you can use other templating systems
{: .slide }

!SLIDE
## What is Colander?  

<div class="slide" markdown="1">
>Colander is useful as a system for validating and deserializing data 
>obtained via XML, JSON, an HTML form post or any other equally simple 
>data serialization.
</div>

What does this mean for forms?
{: .slide }

* Defining form schemas
{: .slide }
* Validating form content
{: .slide }

!SLIDE
## A simple form

To build a simple form we need:

* A colander Schema
{: .slide }
* A deform form object
{: .slide }
* A view callable
{: .slide }
* A template
{: .slide }

!SLIDE
## simple.py

~~~~{python}
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
~~~~

!SLIDE
## Default widgets
* colander.String
    * deform.widget.TextInputWidget
* colander.Integer
    * deform.widget.TextInputWidget
* colander.Float
    * deform.widget.TextInputWidget
* colander.Decimal
    * deform.widget.TextInputWidget
* colander.Boolean
    * deform.widget.CheckboxWidget
* colander.Date
    * deform.widget.DateInputWidget
* colander.DateTime
    * deform.widget.DateTimeInputWidget

!SLIDE
## simple.pt
~~~~{html}
<html>
  <body>
    <span tal:replace="structure form">
  </body>
</html>
~~~~

!SLIDE
## How do we use deform and colander in production?
* Schema inheritance
{: .slide }
* Custom validators
{: .slide }
* Defered validators (Schema Binding)
{: .slide }
* Custom templates
{: .slide }

!SLIDE
## Schema inheritance
~~~~{python}
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
~~~~

!SLIDE
## Custom validators
~~~~{python}
def month_validator(node, month):
    if month.isdigit():
        int_month = int(month)
        if not 0 < int_month < 13:
            raise colander.Invalid(node, 'Please enter a number between 1 and 12')
    else:
        raise colander.Invalid(node, 'Please enter a number')
~~~~

!SLIDE
## Custom validators
~~~~{python}
class AddressSchema(colander.MappingSchema):
    line1 = colander.SchemaNode(colander.String(), title='Address line 1')
    line2 = colander.SchemaNode(colander.String(), title='Address line 2', missing=None)
    line3 = colander.SchemaNode(colander.String(), title='Address line 3', missing=None)
    town = colander.SchemaNode(colander.String(), title='Town')
    postcode = colander.SchemaNode(colander.String(), title = 'Postcode')

class Business(AddressSchema):
    name = colander.SchemaNode(colander.String(), title='Business Name', insert_before='line1')
    month = colander.SchemaNode(colander.String(), title='Start month', validator=month_validator)

def inheritance_form(request):
    form = deform.Form(Business(), buttons=('submit',))
    if request.POST:
        submitted = request.POST.items()
        try:
            form.validate(submitted)
        except deform.ValidationFailure, e:
            return {'form': e.render()}
    return {'form': form.render()}
~~~~

!SLIDE
## Defered validators (Schema binding)
* For when you don't have enough information
{: .slide }
* Keyword arguments resolved later
{: .slide }

!SLIDE
## defered_validator.py
~~~~{python}
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
~~~~

!SLIDE
## defered_validator.py
~~~~{python}
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
~~~~

For CSRF to work it needs a session
~~~~{python}
from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig

my_session_factory = UnencryptedCookieSessionFactoryConfig('itsaseekreet')
config = Configurator(session_factory = my_session_factory)
~~~~

!SLIDE
## Custom templates
* The default templates are functional
{: .slide }
* In version 0.9.9 templates are crap they use `<ul>`
{: .slide }
* In version 2.* templates are better they use `<div>`
{: .slide }
* deform needs to know where to find the templates
{: .slide }

!SLIDE
## Where to find the templates
~~~~{python}
from pkg_resources import resource_filename
from deform import Form

deform_templates = resource_filename('deform', 'templates')
search_path = ('/path/to/your/templates', deform_templates)
Form.set_zpt_renderer(search_path)
~~~~

!SLIDE
## Overridden templates
Minimum of two templates are needed to be overridden to change the structure

* form.pt
{: .slide }
* mapping.pt
{: .slide }

!SLIDE
## Other tricks
* Override individual widget templates
{: .slide }
* Arbitrary keyword arguments in widgets
{: .slide }
* Custom widgets
{: .slide }
* Validate multiple conditions with `colander.All`
{: .slide }

!SLIDE
## References

* [https://github.com/jmstaley/colander-deform-talk](https://github.com/jmstaley/colander-deform-talk)
* [http://jmstaley.github.io/colander-deform-talk](http://jmstaley.github.io/colander-deform-talk)
* [http://docs.pylonsproject.org/projects/deform](http://docs.pylonsproject.org/projects/deform)
* [http://docs.pylonsproject.org/projects/colander](http://docs.pylonsproject.org/projects/colander)
