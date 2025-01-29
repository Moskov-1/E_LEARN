from django.contrib import admin
from .models import *
# Register your models here.
class CourseAdmin(admin.ModelAdmin):
    # Ensure tags aren't pre-selected
    filter_horizontal = ('tags','instructors')

class TagsAdmin(admin.ModelAdmin):
    # Ensure tags aren't pre-selected
    filter_horizontal = ('tags',)

admin.site.register(Course,CourseAdmin)
admin.site.register(Video)
admin.site.register(CourseDetail)
admin.site.register(Blog,TagsAdmin)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(PurchasedCourse)
admin.site.register(Testimonial)
admin.site.register(Tag)
admin.site.register(Mail)
admin.site.register(Instructor)
