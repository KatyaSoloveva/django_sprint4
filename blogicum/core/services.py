from django.db.models import Count
from django.utils.timezone import now


def get_optimized_posts(posts_manager):
    return posts_manager.select_related(
        'category',
        'location',
        'author',
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


def get_optimized_published_posts(posts_manager):
    return posts_manager.filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True
    )
