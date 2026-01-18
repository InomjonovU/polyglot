from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),
    
    # Courses
    path('kurslar/', views.courses_list, name='courses_list'),
    path('kurslar/<slug:slug>/', views.course_detail, name='course_detail'),
    path('kurslar/<slug:slug>/yozilish/', views.course_enroll, name='course_enroll'),
    
    # Teachers
    path('oqituvchilar/', views.teachers_list, name='teachers_list'),
    path('oqituvchilar/<slug:slug>/', views.teacher_detail, name='teacher_detail'),
    path('oqituvchi-bolish/', views.teacher_apply, name='teacher_apply'),
    path('oqituvchi-bolish/muvaffaqiyat/', views.teacher_apply_success, name='teacher_apply_success'),
    
    # News
    path('yangiliklar/', views.news_list, name='news_list'),
    path('yangiliklar/<slug:slug>/', views.news_detail, name='news_detail'),
    
    # Gallery
    path('galereya/', views.gallery, name='gallery'),
    
    # About
    path('biz-haqimizda/', views.about, name='about'),
    
    # Contact
    path('aloqa/', views.contact, name='contact'),
    
    # FAQ
    path('faq/', views.faq, name='faq'),
    
    # Certificates
    path('sertifikatlar/', views.certificates, name='certificates'),
    path('sertifikat-tekshirish/', views.certificate_verify, name='certificate_verify'),
    
    # Search
    path('qidiruv/', views.search, name='search'),
]