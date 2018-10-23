# Loads basic.points model as layer in QGIS.
# This should be executed in QGIS Python console

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
import django
from djangoprovider import DjangoProvider, register_django_provider

#register_django_provider()
django.setup(set_prefix=False)
layer = QgsVectorLayer('basic.point', 'test', 'django')
QgsProject.instance().addMapLayer(layer)





