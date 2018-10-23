import os, sys
from qgis.core import QgsApplication
from qgis.server import QgsServer, QgsServerRequest, QgsBufferServerRequest, QgsBufferServerResponse
from django.http import HttpResponse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from djangoprovider import register_django_provider

# TODO: How QgsApplication should be managed? There should be single instance
qgs = QgsApplication([], False)
qgs.initQgis()


def ows_server(request):
    register_django_provider()

    query_string = request.build_absolute_uri()
    query_string += '&MAP=' + os.path.join(os.path.dirname(__file__), 'test.qgs')

    qgis_request = QgsBufferServerRequest(query_string)
    qgis_response = QgsBufferServerResponse()
    server = QgsServer()
    server.handleRequest(qgis_request, qgis_response)

    response_headers = ['%s: %s' for h in qgis_response.headers().items()]
    body = bytes(qgis_response.body())

    # How to get content type from QgsBufferServerResponse?
    if 'GetCapabilities' in request.get_full_path() or 'GetFeatureInfo' in request.get_full_path():
        content_type = 'text/xml'
    else:
        content_type = 'image/png'

    return HttpResponse(body, content_type=content_type)