from django import template
from django.utils.timezone import now

register = template.Library()

@register.filter
def last_seen_format(value):
    if not value:
        return ""

    diff = now() - value
    seconds = diff.total_seconds()

    if seconds < 3600:
        minutes = int(seconds // 60)
        return f"{minutes} min ago"
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return f"{hours} hour ago"
    else:
        days = int(seconds // 86400)
        return f"{days} day ago"