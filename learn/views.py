from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages 
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail, EmailMessage, send_mass_mail # plan to use mass mail later.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.encoding import force_bytes, force_str
from .models import *
from .form import UserForm
from e_learn import settings
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    tags = Tag.objects.all()
    blogs = Blog.objects.all()
    courses = Course.objects.all()[:6]
    Instructors = Instructor.objects.all()[:4]
    counts = {
        'tags':tags.count(),
        'blogs':Blog.objects.count(),
        'instructors':Instructor.objects.count(),
        'courses':Course.objects.count(),
    }
    context = {'tags':tags,
               'blogs':blogs,
                'courses':courses,
                'instructors':Instructors,
                'counts':counts
               }
    return render(request, "learn/landing_page.html", context)


def about(request):  
    blogs = Blog.objects.all()
    counts = {
        'tags':Tag.objects.count(),
        'blogs':Blog.objects.count(),
        'instructors':Instructor.objects.count(),
        'courses':Course.objects.count(),
    }
    context = {
               'blogs':blogs,
                'counts':counts,
               }
    return render(request, "learn/about.html", context)

def courses(request):  
    tag_id = request.GET.get('tag')
    courses = Course.objects.all()
    if tag_id:
        courses = Course.objects.filter(tags__id=tag_id)
    paginator = Paginator(courses, 6)

    page_num = request.GET.get('page', 1)
    page_courses = paginator.get_page(page_num)
    
    context = {
               'page_courses':page_courses,
               'selected_tag' : tag_id,
    }
    return render(request, "learn/courses.html", context)

def course_detail(request, id):  
    enrolled = False
    course = Course.objects.get(id=id)
    related_courses = Course.objects.filter(tags__in=course.tags.all()).exclude(id=id)
    recent_courses = Course.objects.filter(skill_level='beginner').exclude(id=id)[:8]
    tags = Tag.objects.all()
    if request.user.is_authenticated:
        enrolled = PurchasedCourse.objects.filter(user=request.user, course=course).exists()
    context = {
               'course':course,
               'course_details':CourseDetail.objects.get(course_id=id),
                #'course_details':CourseDetail.objects.filter(course_id=id), 
                # returns a list or QuerySet and not a single object
               'enrolled' : enrolled,
               'related_courses':related_courses,
               'recent_courses':recent_courses,
               'tags':tags,
    }
    return render(request, "learn/course_detail.html", context)

def features(request):  
    return render(request, "learn/features.html")

def team(request):
    instructors = Instructor.objects.all()[:10]  
    return render(request, "learn/team.html", {'instructors':instructors})

def testimonial(request):  
    return render(request, "learn/testimonial.html")

def contact(request):  
    return render(request, "learn/contact.html")
def test(request):  
    return render(request, "learn/test.html")


def signup(request):
    return render(request, 'learn/signup.html')

def signup_check(request):
    if request.method == 'POST':

        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        password = request.POST['password'].strip()
        password_confirmation = request.POST['password_confirmation'].strip()
        first_name = request.POST['firstname'].strip()
        last_name = request.POST['lastname'].strip()

        if not (username and email and password and password_confirmation and first_name and last_name):
            messages.error(request, 'Please fill all the fields')
            return redirect('learn:signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('learn:signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('learn:signup')

        if password != password_confirmation:
            messages.error(request, 'Passwords do not match')
            return redirect('learn:signup')

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'Invalid email')
            return redirect('learn:signup')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = True
        user.is_active = False
        user.save()
        
        # welcome email
        subject = 'Welcome to E Learn'
        message = f'Hello {user.username}!\nWelcome to E Learn.\nThank you for considering us.\nPlease check your email {user.email} to confirm your registration.\nThank you.\n- Raihan Rony'

        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # confirmation email

        current_site = get_current_site(request)
        subject = 'Confirm your email to E-Learn '
        message = render_to_string('learn/confirm_email.html', {
            'name': user.first_name,
            'domain': current_site.domain,
            'uid' : urlsafe_base64_encode(str(user.id).encode()),
            'token' :  token_generator.make_token(user),
        })
        email = EmailMessage(subject, message, from_email, [user.email])        
        email.send(fail_silently=True)
        
        messages.success(request, 'Account created successfully. Please Check your email to confirm account. ')
        
        return HttpResponseRedirect(reverse('learn:signup'))

    return render(request, 'learn/signup.html')

def check_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username = username, password = password) 
            return  user
        else:
            messages.error(request, 'Invalid Credentials')
    return  None
def activate_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user =  get_user_model().objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None 
    
    if user and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('learn:home')
    else:
        return render(request, 'learn/activation_failed.html')
    

def signin(request):
    return render(request, 'learn/signin.html')

def signin_check(request):
   
    user = check_user(request)
    
    if user:
        login(request, user)
        return HttpResponseRedirect(reverse('learn:home'))
    else:
        return redirect('learn:login')


@login_required
def profile(request):
    
    user = request.user

    if user.is_superuser:
        return redirect( '/admin/')
    elif user.is_staff:
        return render(request, 'learn/profile.html')
    else :
        return render(request, 'learn/profile.html')

@login_required
def edit_profile(request):
    if(request.user.is_superuser):
        redirect('/admin/')
    else:
        
        return render(request, 'learn/edit_profile.html',{'form':UserForm(instance=request.user)})
    
@login_required
def update_profile(request):
    if(request.method == 'POST'):
        user = request.user
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('learn:profile')

    return redirect('learn:edit_profile')


@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if the user is already enrolled
    if PurchasedCourse.objects.filter(user=request.user, course=course).exists():
        return redirect('learn:course_detail', id=course_id)
    order = Order.objects.create(user=request.user, course=course, status='pending')
    return redirect('learn:payment', order_id=order.id)

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == "POST":
        # Process payment (e.g., through a payment gateway)
        order.status = 'completed'
        order.save()
        PurchasedCourse.objects.create(
            user=request.user,
            course=order.course,
           
            purchase_date= timezone.now(),  # Add any additional fields as needed
            
        )
        return redirect('learn:course_detail', id=order.course.id)

    return render(request, 'payment.html', {'order': order})

@csrf_protect
def submit_mail(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        text = request.POST.get('text')
        from_email = request.POST.get('from_email')
        to_email = 'wwwronyraihan123@gmail.com'

        # Format email content
        text = f"Subject: {subject}\n\n{text}\n\nFrom: {name} - {from_email}"

        try:
            send_mail(subject, text, from_email, [to_email])
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False})
