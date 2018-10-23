# Django provider for QGIS

This is currently proof of concept / work in progress!

[Django Web framework](https://djangoproject.com) vector data provider for [QGIS](https://qgis.org)

## Supported capabilities:
  * SelectAtId
(It means that editing is not yet supported)

## Supported Django field types:
  * BooleanField
  * NullBooleanField
  * SmallIntegerField
  * IntegerField
  * BigIntegerField
  * FloatField
  * DecimalField
  * CharField
  * TextField
  * DateField
  * Time
  * DateTime
  
## Example in QGIS Python console
Django provider and Django project must be in PYTHONPATH
```python
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
import django
from djangoprovider import register_django_provider

register_django_provider()
django.setup(set_prefix=False)
layer = QgsVectorLayer('basic.point', 'test', 'django')
QgsProject.instance().addMapLayer(layer)
```

  
## Example in Django view
Simple wms server
```python
from qgis.core import QgsApplication
from qgis.server import QgsServer, QgsBufferServerRequest, QgsBufferServerResponse
from django.http import HttpResponse
from djangoprovider import register_django_provider
# TODO: how to manage QgsApplication?
qgs = QgsApplication([], False)
qgs.initQgis()


def ows_server(request):
    register_django_provider()
    query_string = request.build_absolute_uri() + '&MAP=/path/to/map.qgs'
    qgis_request = QgsBufferServerRequest(query_string)
    qgis_response = QgsBufferServerResponse()
    server = QgsServer()
    server.handleRequest(qgis_request, qgis_response)
    # TODO: missing content type
    return HttpResponse(bytes(qgis_response.body()))
```
  
