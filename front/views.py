from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import *


# ==================== HOME ====================
def home(request):
    """Bosh sahifa"""
    context = {
        'popular_courses': Course.objects.filter(
            is_active=True, 
            is_popular=True
        ).select_related('subject').prefetch_related('teachers')[:6],
        
        'featured_teachers': Teacher.objects.filter(
            is_active=True, 
            is_featured=True
        ).prefetch_related('specializations')[:4],
        
        'testimonials': Testimonial.objects.filter(
            is_approved=True, 
            is_featured=True
        )[:6],
        
        'latest_news': News.objects.filter(
            is_published=True
        ).order_by('-publish_date')[:3],
        
        'settings': SiteSettings.load(),
    }
    return render(request, 'index.html', context)


# ==================== COURSES ====================
def courses_list(request):
    """Barcha kurslar"""
    courses = Course.objects.filter(is_active=True).select_related('subject').prefetch_related('teachers')
    
    # Search
    search = request.GET.get('search', '')
    if search:
        courses = courses.filter(
            Q(title__icontains=search) | 
            Q(short_description__icontains=search) |
            Q(full_description__icontains=search)
        )
    
    # Filter by subject
    subject_slug = request.GET.get('subject', '')
    if subject_slug:
        courses = courses.filter(subject__slug=subject_slug)
    
    # Filter by level
    level = request.GET.get('level', '')
    if level:
        courses = courses.filter(level=level)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    courses = courses.order_by(sort)
    
    # Pagination
    paginator = Paginator(courses, 12)
    page = request.GET.get('page')
    courses = paginator.get_page(page)
    
    context = {
        'courses': courses,
        'subjects': Subject.objects.filter(is_active=True),
        'search': search,
        'selected_subject': subject_slug,
        'selected_level': level,
        'settings': SiteSettings.load(),
    }
    return render(request, 'courses_list.html', context)


def course_detail(request, slug):
    """Kurs detallari"""
    course = get_object_or_404(
        Course.objects.select_related('subject').prefetch_related('teachers'),
        slug=slug,
        is_active=True
    )
    
    # Views count
    course.views_count += 1
    course.save(update_fields=['views_count'])
    
    # Related courses
    related_courses = Course.objects.filter(
        subject=course.subject,
        is_active=True
    ).exclude(id=course.id)[:3]
    
    # Testimonials for this course
    testimonials = Testimonial.objects.filter(
        course=course,
        is_approved=True
    )[:6]
    
    context = {
        'course': course,
        'related_courses': related_courses,
        'testimonials': testimonials,
        'settings': SiteSettings.load(),
    }
    return render(request, 'course_detail.html', context)


def course_enroll(request, slug):
    """Kursga yozilish"""
    course = get_object_or_404(Course, slug=slug, is_active=True)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        
        # Create enrollment
        enrollment = CourseEnrollment.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            course=course,
            message=message
        )
        
        # Update course enrollments count
        course.enrollments_count += 1
        course.save(update_fields=['enrollments_count'])
        
        messages.success(request, 'Arizangiz qabul qilindi! Tez orada siz bilan bog\'lanamiz.')
        return redirect('course_detail', slug=course.slug)
    
    return redirect('course_detail', slug=course.slug)


# ==================== TEACHERS ====================
def teachers_list(request):
    """Barcha o'qituvchilar"""
    teachers = Teacher.objects.filter(is_active=True).prefetch_related('specializations')
    
    # Search
    search = request.GET.get('search', '')
    if search:
        teachers = teachers.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(education__icontains=search)
        )
    
    # Filter by specialization
    subject_slug = request.GET.get('subject', '')
    if subject_slug:
        teachers = teachers.filter(specializations__slug=subject_slug)
    
    # Pagination
    paginator = Paginator(teachers, 12)
    page = request.GET.get('page')
    teachers = paginator.get_page(page)
    
    context = {
        'teachers': teachers,
        'subjects': Subject.objects.filter(is_active=True),
        'search': search,
        'selected_subject': subject_slug,
        'settings': SiteSettings.load(),
    }
    return render(request, 'teachers_list.html', context)


def teacher_detail(request, slug):
    """O'qituvchi detallari"""
    teacher = get_object_or_404(
        Teacher.objects.prefetch_related('specializations'),
        slug=slug,
        is_active=True
    )
    
    # Teacher courses
    courses = Course.objects.filter(
        teachers=teacher,
        is_active=True
    )[:6]
    
    context = {
        'teacher': teacher,
        'courses': courses,
        'settings': SiteSettings.load(),
    }
    return render(request, 'teacher_detail.html', context)


def teacher_apply(request):
    """O'qituvchi bo'lish uchun ariza"""
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        education = request.POST.get('education')
        experience_years = request.POST.get('experience_years')
        subject_id = request.POST.get('subject')
        about_me = request.POST.get('about_me')
        why_teach = request.POST.get('why_teach')
        
        # Create application
        application = TeacherApplication.objects.create(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            email=email,
            education=education,
            experience_years=experience_years,
            subject_id=subject_id,
            about_me=about_me,
            why_teach=why_teach
        )
        
        # Handle file uploads
        if 'cv_file' in request.FILES:
            application.cv_file = request.FILES['cv_file']
        
        if 'certificates' in request.FILES:
            application.certificates = request.FILES['certificates']
        
        if 'photo' in request.FILES:
            application.photo = request.FILES['photo']
        
        application.save()
        
        messages.success(request, 'Arizangiz muvaffaqiyatli yuborildi! Tez orada siz bilan bog\'lanamiz.')
        return redirect('teacher_apply_success')
    
    context = {
        'subjects': Subject.objects.filter(is_active=True),
        'settings': SiteSettings.load(),
    }
    return render(request, 'teacher_apply.html', context)


def teacher_apply_success(request):
    """Ariza muvaffaqiyatli yuborildi"""
    context = {
        'settings': SiteSettings.load(),
    }
    return render(request, 'teacher_apply_success.html', context)


# ==================== NEWS ====================
def news_list(request):
    """Barcha yangiliklar"""
    news = News.objects.filter(is_published=True).order_by('-publish_date')
    
    # Search
    search = request.GET.get('search', '')
    if search:
        news = news.filter(
            Q(title__icontains=search) |
            Q(short_description__icontains=search) |
            Q(content__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(news, 9)
    page = request.GET.get('page')
    news = paginator.get_page(page)
    
    # Featured news
    featured_news = News.objects.filter(
        is_published=True,
        is_featured=True
    )[:3]
    
    context = {
        'news': news,
        'featured_news': featured_news,
        'search': search,
        'settings': SiteSettings.load(),
    }
    return render(request, 'news_list.html', context)


def news_detail(request, slug):
    """Yangilik detallari"""
    news = get_object_or_404(
        News.objects.prefetch_related('gallery_images'),
        slug=slug,
        is_published=True
    )
    
    # Views count
    news.views_count += 1
    news.save(update_fields=['views_count'])
    
    # Related news
    related_news = News.objects.filter(
        is_published=True
    ).exclude(id=news.id).order_by('-publish_date')[:3]
    
    context = {
        'news': news,
        'related_news': related_news,
        'settings': SiteSettings.load(),
    }
    return render(request, 'news_detail.html', context)


# ==================== GALLERY ====================
def gallery(request):
    """Galereya"""
    images = Gallery.objects.select_related('category').order_by('-created_at')
    
    # Filter by category
    category_slug = request.GET.get('category', '')
    if category_slug:
        images = images.filter(category__slug=category_slug)
    
    # Pagination
    paginator = Paginator(images, 24)
    page = request.GET.get('page')
    images = paginator.get_page(page)
    
    context = {
        'images': images,
        'categories': GalleryCategory.objects.all(),
        'selected_category': category_slug,
        'settings': SiteSettings.load(),
    }
    return render(request, 'gallery.html', context)


# ==================== ABOUT ====================
def about(request):
    """Biz haqimizda"""
    context = {
        'teachers_count': Teacher.objects.filter(is_active=True).count(),
        'courses_count': Course.objects.filter(is_active=True).count(),
        'students_count': 500,  # or from settings
        'testimonials': Testimonial.objects.filter(
            is_approved=True,
            is_featured=True
        )[:4],
        'settings': SiteSettings.load(),
    }
    return render(request, 'about.html', context)


# ==================== CONTACT ====================
def contact(request):
    """Aloqa sahifasi"""
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')
        
        # Create contact
        Contact.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Xabaringiz yuborildi! Tez orada javob beramiz.')
        return redirect('contact')
    
    context = {
        'settings': SiteSettings.load(),
    }
    return render(request, 'contact.html', context)


# ==================== FAQ ====================
def faq(request):
    """FAQ sahifasi"""
    faqs = FAQ.objects.filter(is_active=True).select_related('category')
    
    # Group by category
    categories = FAQCategory.objects.all()
    
    context = {
        'faqs': faqs,
        'categories': categories,
        'settings': SiteSettings.load(),
    }
    return render(request, 'faq.html', context)


# ==================== CERTIFICATES ====================
def certificates(request):
    """Sertifikatlar"""
    certificates = Certificate.objects.select_related(
        'course', 'teacher'
    ).order_by('-issue_date')
    
    # Filter by course
    course_slug = request.GET.get('course', '')
    if course_slug:
        certificates = certificates.filter(course__slug=course_slug)
    
    # Search by name or certificate number
    search = request.GET.get('search', '')
    if search:
        certificates = certificates.filter(
            Q(student_name__icontains=search) |
            Q(certificate_number__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(certificates, 12)
    page = request.GET.get('page')
    certificates = paginator.get_page(page)
    
    context = {
        'certificates': certificates,
        'courses': Course.objects.filter(is_active=True),
        'search': search,
        'settings': SiteSettings.load(),
    }
    return render(request, 'certificates.html', context)


def certificate_verify(request):
    """Sertifikat tekshirish"""
    certificate = None
    
    if request.method == 'POST':
        certificate_number = request.POST.get('certificate_number')
        try:
            certificate = Certificate.objects.get(certificate_number=certificate_number)
        except Certificate.DoesNotExist:
            messages.error(request, 'Sertifikat topilmadi!')
    
    context = {
        'certificate': certificate,
        'settings': SiteSettings.load(),
    }
    return render(request, 'certificate_verify.html', context)


# ==================== SEARCH ====================
def search(request):
    """Global qidiruv"""
    query = request.GET.get('q', '')
    
    if query:
        # Search in courses
        courses = Course.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query),
            is_active=True
        )[:5]
        
        # Search in teachers
        teachers = Teacher.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query),
            is_active=True
        )[:5]
        
        # Search in news
        news = News.objects.filter(
            Q(title__icontains=query) |
            Q(short_description__icontains=query),
            is_published=True
        )[:5]
    else:
        courses = []
        teachers = []
        news = []
    
    context = {
        'query': query,
        'courses': courses,
        'teachers': teachers,
        'news': news,
        'settings': SiteSettings.load(),
    }
    return render(request, 'search.html', context)