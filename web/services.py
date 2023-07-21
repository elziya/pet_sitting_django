def filter_posts(posts_qs, filters: dict):
    if filters['search']:
        posts_qs = posts_qs.filter(title__icontains=filters['search'])

    if filters['opened'] is not None:
        posts_qs = posts_qs.filter(opened=filters['opened'])

    if filters['start_date']:
        posts_qs = posts_qs.filter(start_date__gte=filters['start_date'])

    if filters['end_date']:
        posts_qs = posts_qs.filter(end_date__lte=filters['end_date'])

    return posts_qs
