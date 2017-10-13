# ideallical django-restframework pagination

## Requirements

* Python (3.5)

## Installation

Install using `pip`...

    pip install ii-drf-pagination


## Example

Let's take a look at a quick example of using ii-drf-pagination's pagination
class in your django restframework setup:

```python

    REST_FRAMEWORK = {
        [...]
        'DEFAULT_PAGINATION_CLASS': (
            'ii_drf_pagination.pagination.IIDRFPagination'),
        'PAGE_SIZE': 20,
        [...]
    }

    II_DRF_PAGINATION = {
        'PAGE_SIZE_QUERY_PARAM': 'page_size',
        'INCLUDE_PAGE_LINKS': False,
        'LABEL_CURRENT_PAGE_NUMBER': 'current_page'
    }
```

Setting II_DRF_PAGINATION['PAGE_SIZE_QUERY_PARAM'] to 'page_size' will enable
the user to specify a custom page_size other than REST_FRAMEWORK['PAGE_SIZE'].
By default this is set to None; meaning the user can't alter the page_size.

Setting II_DRF_PAGINATION['INCLUDE_PAGE_LINKS'] to False, will exclude
page-links from showing up in the pagination JSON.

Setting II_DRF_PAGINATION['LABEL_CURRENT_PAGE_NUMBER'] to 'current_page' will
label te current page number of the pagination to 'current_page' (instead of
the default label, which is 'current_page_number').
