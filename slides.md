!SLIDE
# 'king Forms 

!SLIDE
## Overview
* What is Deform?
* What is Colander?
* A simple form

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

class Contact(colander.Schema):
    """ A simple colander schema """
    email = colander.SchemaNode(colander.String())
    name = colander.SchemaNode(colander.String())
    message = colander.SchemaNode(colander.String())

def simple_form(request):
    """ view callable """
    form = deform.Form(Contact(), buttons=('submit',)) # deform form
    return {'form': form.render()}
~~~~

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
## References

* http://docs.pylonsproject.org/projects/deform
* http://docs.pylonsproject.org/projects/colander
