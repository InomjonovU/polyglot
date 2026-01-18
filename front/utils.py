"""
PolyglotLC - Utility Functions
Admin panel badges va boshqa yordamchi funksiyalar
"""

def get_courses_count(request):
    """Faol kurslar sonini qaytaradi"""
    from front.models import Course
    count = Course.objects.filter(is_active=True).count()
    return count if count > 0 else None


def get_pending_enrollments(request):
    """Kutilayotgan ro'yxatdan o'tishlar sonini qaytaradi"""
    from front.models import CourseEnrollment
    count = CourseEnrollment.objects.filter(status='pending').count()
    return count if count > 0 else None


def get_pending_applications(request):
    """Kutilayotgan o'qituvchi arizalari sonini qaytaradi"""
    from front.models import TeacherApplication
    count = TeacherApplication.objects.filter(status='pending').count()
    return count if count > 0 else None


def get_new_messages(request):
    """Yangi xabarlar sonini qaytaradi"""
    from front.models import Contact
    count = Contact.objects.filter(status='new').count()
    return count if count > 0 else None


def generate_certificate_number():
    """Yangi sertifikat raqamini generatsiya qiladi"""
    import datetime
    from front.models import Certificate
    
    year = datetime.date.today().year
    last_cert = Certificate.objects.filter(
        certificate_number__startswith=f'PLC-{year}'
    ).order_by('-certificate_number').first()
    
    if last_cert:
        try:
            last_num = int(last_cert.certificate_number.split('-')[-1])
            new_num = last_num + 1
        except:
            new_num = 1
    else:
        new_num = 1
    
    return f'PLC-{year}-{new_num:04d}'


def format_phone_number(phone):
    """Telefon raqamini formatlaydi"""
    import re
    phone = re.sub(r'\D', '', phone)
    
    if len(phone) == 12 and phone.startswith('998'):
        return f'+{phone[:3]} {phone[3:5]} {phone[5:8]} {phone[8:10]} {phone[10:]}'
    elif len(phone) == 9:
        return f'+998 {phone[:2]} {phone[2:5]} {phone[5:7]} {phone[7:]}'
    
    return phone


def get_site_settings():
    """Sayt sozlamalarini oladi (cached)"""
    from django.core.cache import cache
    from front.models import SiteSettings
    
    settings = cache.get('site_settings')
    if not settings:
        settings = SiteSettings.objects.first()
        if settings:
            cache.set('site_settings', settings, 3600)  # 1 soat cache
    return settings