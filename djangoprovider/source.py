from qgis.core import QgsAbstractFeatureSource
from .iterator import DjangoFeatureIterator


class DjangoFeatureSource(QgsAbstractFeatureSource):

    def __init__(self, model, qgs_fields, dj_fields, dj_geo_field, crs):
        super(DjangoFeatureSource, self).__init__()
        self.model = model
        self.qgs_fields = qgs_fields
        self.dj_fields = dj_fields
        self.dj_geo_field = dj_geo_field
        self.crs = crs

    def getFeatures(self, request):
        return QgsFeatureIterator(DjangoFeatureIterator(self, request))
