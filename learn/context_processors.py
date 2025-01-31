from django.conf import settings
from django.db.models import Count
from .models import Tag, Course

def site_info(request):
    return {
        'site_info': settings.SITE_INFO
    }


def tag_context_processor(request):
    # Annotate tags with the count of related courses
    tags_count = Tag.objects.annotate(
        # property called course_count exits in model
        # it conflicts with annotation so name changed to
        # course_counts
        course_counts=Count('tagged_courses')
    ).filter(
        course_counts__gt=0  # Exclude tags with zero courses
    ).order_by('-course_counts')[:6]  
    for tag in tags_count:
        print(f"{tag.name}: {tag.course_count} courses")
    return {
        'tags_count': tags_count,
    }