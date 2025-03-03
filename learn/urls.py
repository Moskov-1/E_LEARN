from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "learn"

urlpatterns = [
    path('', views.index, name="home"),
    path('blogs/', views.about, name="about"),
    path('test_blogs/', views.tb, name="tblogs"),
    path('test_blog_full/<int:id>/', views.tbf, name="tblog_full"),
    
    path('courses/', views.courses, name="courses"),
    path('course_detail/<int:id>/', views.course_detail, name="course_detail"),
    path('features/', views.features, name="features"),
    path('team/', views.team, name="team"),
    path('testimonial/', views.testimonial, name="testimonial"),
    path('contact/', views.contact, name="contact"),
    path('signup/', views.signup, name='signup'),
    path("signup_check/", views.signup_check, name="signup_check"),
    path('activate_email/<uidb64>/<token>/', views.activate_email, name='activate_email'),

    path('login/', views.signin, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='learn:home'), name='logout'),
    path('log_verify/', views.signin_check, name='signin_check'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name= 'edit_profile'),
    path('update_profile/', views.update_profile, name= 'update_profile'),
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
     path('payment/<int:order_id>/', views.payment, name='payment'),
     path('submit_mail/', views.submit_mail, name='submit_mail'),

    path('test/', views.test, name="test"),
]

