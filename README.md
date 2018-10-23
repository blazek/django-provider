# Django provider for QGIS

[Django Web framework](https://djangoproject.com) vector data provider for [QGIS](https://qgis.org)

## Supported capabilities:
  * SelectAtId
(It means that editing is not yet supported)

##Supported Django field types:
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
  
## Example in Django
```
from qgis.core import *
from djangoprovider.provider import DjangoProvider

qgs = QgsApplication([], False)
qgs.initQgis()
registry = QgsProviderRegistry.instance()
metadata = QgsProviderMetadata(DjangoProvider.providerKey(), DjangoProvider.description(), DjangoProvider.createProvider)

layer = QgsVectorLayer('myapp.mymodel', 'test', 'djangoprovider')
```
  
