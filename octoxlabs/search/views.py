from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from core.helpers import elasticsearch_connection

class SearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        es = elasticsearch_connection()
        data = []
        page = 0
        page_size = 10

        while True:
            res = es.search(
                index="logs",
                body={"query": {"match_all": {}}},
                from_=page * page_size,
                size=page_size
            )
            hits = res['hits']['hits']
            if not hits:
                break
            data.extend([hit['_source'] for hit in hits])
            page += 1

        return Response(data)
