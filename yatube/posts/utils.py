from django.core.paginator import Paginator, Page
from django.db.models import QuerySet


POSTS_LIMIT: int = 10


def paginate(
    page_number: int, records: QuerySet, posts_limit: int = POSTS_LIMIT
) -> Page:
    paginator = Paginator(records, posts_limit)
    return paginator.get_page(page_number)
