from django.db import models
from django.contrib.auth.models import User
import cv2
import numpy as np
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import *
from cloudinary.models import CloudinaryField

#from django.db.models import DurationField
#from datetime import timedelta

# User Model (default Django User is used)

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
    @property
    def course_count(self):
        return self.tagged_courses.count()

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='instructor')
   
    name = models.CharField(max_length=500, blank=True, null=True)
    image = CloudinaryField(folder='instructors/images/', blank=True, null=True)
    profession = models.CharField(max_length=200, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    fb = models.CharField(max_length=500, null=True, blank=True)
    yt = models.CharField(max_length=500, null=True, blank=True)
    linkedin = models.CharField(max_length=500, null=True, blank=True)   
    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #     if not self.name and self.user:
    #         self.name = f"{self.user.first_name} {self.user.last_name}"
    #     # Check if an image is uploaded
    #     if self.image:
    #         # PIL format
    #         img = Image.open(self.image)
    #         original_format = img.format
    #         img_array = np.array(img)
    #         # resizing with openCV (width x height) 
    #         # potrait 
    #         processed_img = cv2.resize(img_array, (120, 100))
    #         # Convert back to PIL format
    #         processed_img = Image.fromarray(processed_img)
    #         # Save the processed image back to the image field
    #         buffer = BytesIO()
    #         processed_img.save(buffer, format=original_format)  # Save as original format
    #         buffer.seek(0)
    #         self.image.save(self.image.name, ContentFile(buffer.read()), save=False)

    #     super().save(*args, **kwargs)
    
# Course Model
class Course(models.Model):
    choices = [
        ('beginner', 'beginner'),
        ('intermediate', 'intermediate'),
        ('advanced', 'advanced'),    
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = CloudinaryField(folder='courses/images/',blank=True, null=True)
    instructors = models.ManyToManyField(Instructor, related_name='instructor_courses')
    tags = models.ManyToManyField(Tag, related_name='tagged_courses')
    rating = models.FloatField(default=3.5)  # Default rating for courses
    lectures = models.PositiveIntegerField(default=0)
    lang = models.CharField(max_length=100, null=True, blank=True)
    skill_level = models.CharField(max_length=100, null=True, blank=True, choices=choices)
    price = models.DecimalField(max_digits=10, null=True, blank=True,decimal_places=2)
    def __str__(self):
        return self.title

    '''
        @property
        def total_duration(self):
            # Aggregate the total duration from related videos
            total_microseconds = self.videos.aggregate(total_duration=models.Sum('duration'))['total_duration']
            
            if total_microseconds  is not None:
                # Convert microseconds into a timedelta object
                return timedelta(microseconds=total_microseconds)
            return timedelta(0)  # Return 0 if no videos exist  
    '''
    @property
    def instructor_names(self):
        return ', '.join([str(instructor.user) for instructor in self.instructors.all()])

    @property
    def first_instructor(self):
        return self.instructors.first()
    

# Video Model
class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=200)
    video_file = CloudinaryField(folder='courses/videos/', resource_type='video',blank=True, null=True)
    is_watched = models.BooleanField(default=False)
    #duration = DurationField()  # Field to store video duration.... wow :v
    def __str__(self):
        return f"{self.course.title} - {self.title}"

# Course Details Model
class CourseDetail(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='details')
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    image = CloudinaryField(folder='courses/details/images/',blank=True, null=True)

    def __str__(self):
        return f"{self.course.title} - {self.title} -{self.image.url}"

# Testimonial Model
class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='testimonials')
    content = models.TextField()
    image = CloudinaryField(folder='testimonials/images/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Testimonial"

# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = CloudinaryField(folder='blogs/images/',blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tagged_blogs')
    
    def __str__(self):
        return self.title

# Order Model
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order #{self.id} by {self.user.username} - {self.status}"

# Payment Model
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    payment_date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Payment for Order #{self.order.id}"

# Mail Model
class Mail(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='mails')
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mail from {self.email}"

# Purchased Courses Model
class PurchasedCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='purchased_by')
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} purchased {self.course.title}"
