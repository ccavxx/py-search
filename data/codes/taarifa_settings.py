"""Global API configuration."""
from os import environfrom urlparse import urlparse
# This module is both imported from and executed. In the former case only# relative imports are supported, in the latter only absolute.try: from schemas import facility_schema, request_schema, resource_schema, \        service_schemaexcept ImportError: from taarifa_api.schemas import facility_schema, request_schema, \        resource_schema, service_schema
API_NAME = 'TaarifaAPI'URL_PREFIX = environ.get('API_URL_PREFIX', 'api')if 'EVE_DEBUG' in environ: DEBUG = True TRAP_HTTP_EXCEPTIONS = True TRAP_BAD_REQUEST_KEY_ERRORS = True
if 'MONGOLAB_URI' in environ:    url = urlparse(environ['MONGOLAB_URI']) MONGO_HOST = url.hostname MONGO_PORT = url.port MONGO_USERNAME = url.username MONGO_PASSWORD = url.password MONGO_DBNAME = url.path[1:]else: MONGO_DBNAME = environ.get('MONGO_DBNAME', API_NAME)
# Enable reads (GET), inserts (POST) and DELETE for resources/collections# (if you omit this line, the API will default to ['GET'] and provide# read-only access to the endpoint).RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
# Enable reads (GET), edits (PATCH) and deletes of individual items# (defaults to read-only item access).ITEM_METHODS = ['GET', 'PUT', 'PATCH', 'DELETE']
services = { "schema": service_schema, "transparent_schema_rules": True,}
requests = { "schema": request_schema, "source": "requests", "key": "service_code",}
facilities = { "item_title": "facility", "schema": facility_schema, "transparent_schema_rules": True,}
resources = { "schema": resource_schema, "source": "resources", "key": "facility_code",}
DOMAIN = { 'services': services, 'requests': requests, 'facilities': facilities, 'resources': resources,}
# Allow requesting up to 100 results per pagePAGINATION_LIMIT = 100# FIXME: Temporarily allow CORS requests for development purposesX_DOMAINS = "*"# Enable Flask-Compress in debug modeCOMPRESS_DEBUG = True# gzip compression levelCOMPRESS_LEVEL = 9# Enable document version controlVERSIONING = True# For debugging# TRAP_HTTP_EXCEPTIONS = True# TRAP_BAD_REQUEST_KEY_ERRORS = True