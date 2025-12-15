from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'  # allows ?page_size=20
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('all_page', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('current', self.page.number),
            ('has_next', self.page.has_next()),
            ('has_previous', self.page.has_previous()),
            ('results', data)
        ]))
