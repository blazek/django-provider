import os, sys
from qgis.core import QgsApplication, QgsProject
from qgis.server import QgsServer, QgsBufferServerRequest, QgsBufferServerResponse
from django.http import HttpResponse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../'))
from djangoprovider import register_django_provider

# TODO: How QgsApplication should be managed? There should be single instance
qgs = QgsApplication([], False)
qgs.initQgis()


def ows_server(request):
    register_django_provider()

    query_string = request.build_absolute_uri()
    project_path = os.path.join(os.path.dirname(__file__), 'test.qgs')
    qgis_project = QgsProject()
    qgis_project.read(project_path)

    qgis_request = QgsBufferServerRequest(query_string)
    qgis_response = QgsBufferServerResponse()
    server = QgsServer()
    server.handleRequest(qgis_request, qgis_response, qgis_project)

    body = bytes(qgis_response.body())

    response = HttpResponse(body)
    for k, v in qgis_response.headers().items():
        response[k] = v

    return response