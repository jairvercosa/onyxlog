import json
from django.core.serializers import serialize
from django.db.models.query import QuerySet

def jsonify(object):
    if isinstance(object, QuerySet):
        return serialize('json', object)
    return json.dumps(object)