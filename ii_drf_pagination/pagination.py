from ii_drf_pagination.settings import pagination_settings as ps
from rest_framework.pagination import (
    PageNumberPagination, _get_displayed_page_numbers, _get_page_links
)
from rest_framework.response import Response
from rest_framework.utils.urls import remove_query_param, replace_query_param


class IIDRFPagination(PageNumberPagination):
    page_size_query_param = ps.PAGE_SIZE_QUERY_PARAM

    def get_paginated_response(self, data):
        base_url = self.request.build_absolute_uri()

        def page_number_to_url(page_number):
            if page_number == 1:
                return remove_query_param(base_url, self.page_query_param)
            else:
                return replace_query_param(
                    base_url, self.page_query_param, page_number)

        response = {}

        if ps.INCLUDE_COUNT:
            response[ps.LABEL_COUNT] = self.page.paginator.count

        if ps.INCLUDE_NEXT:
            response[ps.LABEL_NEXT] = self.get_next_link()

        if ps.INCLUDE_PREVIOUS:
            response[ps.LABEL_PREVIOUS] = self.get_previous_link()

        if ps.INCLUDE_NEXT_PAGE_NUMBER:
            response[ps.LABEL_NEXT_PAGE_NUMBER] = (
                self.page.next_page_number() if self.page.has_next() else None)

        if ps.INCLUDE_PREVIOUS_PAGE_NUMBER:
            response[ps.LABEL_PREVIOUS_PAGE_NUMBER] = (
                self.page.previous_page_number()
                if self.page.has_previous() else None)

        if ps.INCLUDE_PAGE_SIZE:
            response[ps.LABEL_PAGE_SIZE] = self.get_page_size(self.request)

        if ps.INCLUDE_RESULTS:
            response[ps.LABEL_RESULTS] = data

        if ps.INCLUDE_PAGE_LINKS:
            current = self.page.number
            final = self.page.paginator.num_pages
            page_numbers = _get_displayed_page_numbers(current, final)
            page_links = _get_page_links(
                page_numbers, current, page_number_to_url)
            response[ps.LABEL_PAGE_LINKS] = page_links

        if ps.INCLUDE_CURRENT_PAGE_NUMBER:
            response[ps.LABEL_CURRENT_PAGE_NUMBER] = self.page.number

        return Response(response)
