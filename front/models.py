from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.text import slugify
from django.urls import reverse


# ==================== USER ====================
class User(AbstractUser):
    """Foydalanuvchi - admin va boshqalar"""
    phone = models.CharField('Telefon', max_length=20, blank=True, null=True)
    profile_image = models.ImageField('Profil rasmi', upload_to='users/%Y/%m/', blank=True, null=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='front_user_set',
        related_query_name='front_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='front_user_set',
        related_query_name='front_user',
    )

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return self.get_full_name() or self.username


# ==================== FAN / SUBJECT ====================
class Subject(models.Model):
    """Fanlar - IELTS, English, Matematika va h.k."""
    name = models.CharField('Fan nomi', max_length=100, unique=True)
    slug = models.SlugField('Slug', max_length=120, unique=True, blank=True)
    description = models.TextField('Tavsif', blank=True)
    icon = models.CharField('Icon (FontAwesome)', max_length=50, blank=True, help_text='Masalan: fa-book, fa-language')
    image = models.ImageField('Rasm', upload_to='subjects/', blank=True, null=True)
    order = models.IntegerField('Tartib', default=0)
    is_active = models.BooleanField('Faolmi?', default=True)
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Fan'
        verbose_name_plural = 'Fanlar'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# ==================== O'QITUVCHI ====================
class Teacher(models.Model):
    """O'qituvchilar"""
    first_name = models.CharField('Ism', max_length=100)
    last_name = models.CharField('Familiya', max_length=100)
    slug = models.SlugField('Slug', max_length=220, unique=True, blank=True)
    photo = models.ImageField('Rasmi', upload_to='teachers/%Y/%m/')
    
    # Aloqa
    phone = models.CharField('Telefon', max_length=20)
    email = models.EmailField('Email', blank=True, null=True)
    
    # Malaka
    education = models.CharField('Ta\'lim', max_length=200, help_text='Masalan: TSUL, Oxford University')
    ielts_score = models.DecimalField('IELTS ball', max_digits=2, decimal_places=1, 
                                      validators=[MinValueValidator(0), MaxValueValidator(9)],
                                      blank=True, null=True)
    toefl_score = models.IntegerField('TOEFL ball', blank=True, null=True)
    cefr_level = models.CharField('CEFR daraja', max_length=2, blank=True, null=True, 
                                   help_text='A1, A2, B1, B2, C1, C2')
    experience_years = models.IntegerField('Tajriba (yillar)', validators=[MinValueValidator(0)])
    
    # Sertifikatlar
    certificates_file = models.FileField('Sertifikatlar', upload_to='teacher_certificates/%Y/%m/',
                                         blank=True, null=True,
                                         help_text='Bir nechta sertifikat bo\'lsa ZIP file yuklang')
    
    # Bio
    bio = models.TextField('Qisqacha ma\'lumot', max_length=500)
    full_bio = models.TextField('To\'liq biografiya')
    
    # Ixtisoslashuvlar
    specializations = models.ManyToManyField(Subject, verbose_name='Ixtisoslashuv', related_name='teachers')
    
    # Skills
    skills = models.TextField('Ko\'nikmalar', blank=True, 
                             help_text='Har bir ko\'nikmani yangi qatorga yozing')
    
    # Ijtimoiy tarmoqlar
    facebook = models.URLField('Facebook', blank=True, null=True)
    instagram = models.URLField('Instagram', blank=True, null=True)
    telegram = models.URLField('Telegram', blank=True, null=True)
    linkedin = models.URLField('LinkedIn', blank=True, null=True)
    
    # Sozlamalar
    is_active = models.BooleanField('Faolmi?', default=True)
    is_featured = models.BooleanField('Asosiy sahifada ko\'rsatish?', default=False)
    order = models.IntegerField('Tartib', default=0)
    created_at = models.DateTimeField('Qo\'shilgan', auto_now_add=True)
    
    class Meta:
        verbose_name = 'O\'qituvchi'
        verbose_name_plural = 'O\'qituvchilar'
        ordering = ['order', 'first_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.first_name}-{self.last_name}")
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('teacher_detail', kwargs={'slug': self.slug})


# ==================== KURS ====================
class Course(models.Model):
    """Kurslar"""
    
    LEVEL_CHOICES = [
        ('beginner', 'Beginner (Boshlang\'ich)'),
        ('elementary', 'Elementary'),
        ('pre_intermediate', 'Pre-Intermediate'),
        ('intermediate', 'Intermediate (O\'rta)'),
        ('upper_intermediate', 'Upper-Intermediate'),
        ('advanced', 'Advanced (Yuqori)'),
    ]
    
    # Asosiy ma'lumotlar
    title = models.CharField('Kurs nomi', max_length=200)
    slug = models.SlugField('Slug', max_length=220, unique=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name='Fan', related_name='courses')
    
    # Rasmlar
    main_image = models.ImageField('Asosiy rasm', upload_to='courses/%Y/%m/')
    thumbnail = models.ImageField('Kichik rasm (thumbnail)', upload_to='courses/thumbs/%Y/%m/', blank=True, null=True)
    
    # Tavsif
    short_description = models.CharField('Qisqacha tavsif', max_length=300)
    full_description = models.TextField('To\'liq tavsif')
    
    # Kurs ma'lumotlari
    level = models.CharField('Daraja', max_length=20, choices=LEVEL_CHOICES, default='beginner')
    duration_months = models.IntegerField('Davomiyligi (oylar)', validators=[MinValueValidator(1)])
    lessons_per_week = models.IntegerField('Haftada darslar soni', default=3)
    lesson_duration = models.IntegerField('Bir dars davomiyligi (daqiqa)', default=90)
    
    # Narx
    price = models.DecimalField('Narx (so\'m)', max_digits=10, decimal_places=2, 
                                validators=[MinValueValidator(0)])
    discount_price = models.DecimalField('Chegirma narxi', max_digits=10, decimal_places=2, 
                                        blank=True, null=True)
    
    # O'qituvchilar
    teachers = models.ManyToManyField(Teacher, verbose_name='O\'qituvchilar', related_name='courses', blank=True)
    
    # O'rgatilishi
    what_you_learn = models.TextField('Nimalar o\'rgatiladi?', 
                                      help_text='Har bir nuqtani yangi qatorga yozing')
    
    # Talablar
    requirements = models.TextField('Talablar', blank=True,
                                   help_text='Kursga kirish uchun talablar. Har birini yangi qatorga yozing')
    
    # Kimlar uchun?
    target_audience = models.TextField('Kimlar uchun mo\'ljallangan?', 
                                      help_text='Har bir nuqtani yangi qatorga yozing')
    
    # Kurs rejasi (syllabus)
    syllabus = models.TextField('Kurs rejasi / O\'quv dasturi', blank=True,
                               help_text='Nima-nima o\'rganiladi, mavzular')
    
    # Natija
    expected_results = models.TextField('Kutilayotgan natijalar', blank=True,
                                       help_text='Kurs tugagandan keyin nimaga erishasiz')
    
    # Sertifikat
    certificate_info = models.TextField('Sertifikat haqida', blank=True,
                                       help_text='Qanday sertifikat beriladi?')
    
    # Sozlamalar
    is_active = models.BooleanField('Faolmi?', default=True)
    is_featured = models.BooleanField('Asosiy sahifada?', default=False)
    is_popular = models.BooleanField('Mashhurmi?', default=False)
    order = models.IntegerField('Tartib', default=0)
    
    # Statistika
    views_count = models.IntegerField('Ko\'rishlar soni', default=0, editable=False)
    enrollments_count = models.IntegerField('Yozilganlar soni', default=0, editable=False)
    
    # Sanalar
    start_date = models.DateField('Boshlanish sanasi', blank=True, null=True)
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)
    updated_at = models.DateTimeField('Yangilangan', auto_now=True)
    
    class Meta:
        verbose_name = 'Kurs'
        verbose_name_plural = 'Kurslar'
        ordering = ['-is_featured', 'order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})
    
    @property
    def has_discount(self):
        return self.discount_price and self.discount_price < self.price
    
    @property
    def final_price(self):
        return self.discount_price if self.has_discount else self.price


# ==================== KURSGA YOZILISH SO'ROVI ====================
class CourseEnrollment(models.Model):
    """Kursga yozilish uchun so'rovlar"""
    
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('contacted', 'Aloqaga chiqildi'),
        ('enrolled', 'Yozildi'),
        ('rejected', 'Rad etildi'),
    ]
    
    # Shaxsiy ma'lumotlar
    full_name = models.CharField('To\'liq ism', max_length=200)
    phone = models.CharField('Telefon raqam', max_length=20)
    email = models.EmailField('Email', blank=True, null=True)
    
    # Kurs
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Kurs', 
                               related_name='enrollments')
    
    # Qo'shimcha
    message = models.TextField('Xabar / Savol', blank=True)
    
    # Status
    status = models.CharField('Holat', max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField('Admin eslatmasi', blank=True)
    
    # Sanalar
    created_at = models.DateTimeField('Yuborilgan', auto_now_add=True)
    updated_at = models.DateTimeField('Yangilangan', auto_now=True)
    
    class Meta:
        verbose_name = 'Kursga yozilish so\'rovi'
        verbose_name_plural = 'Kursga yozilish so\'rovlari'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.course.title}"


# ==================== SERTIFIKATLAR ====================
class Certificate(models.Model):
    """Berilgan sertifikatlar"""
    
    student_name = models.CharField('Talaba ismi', max_length=200)
    student_photo = models.ImageField('Talaba rasmi', upload_to='certificates/students/%Y/%m/', 
                                     blank=True, null=True)
    
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, 
                              verbose_name='Kurs', related_name='certificates')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True,
                               verbose_name='O\'qituvchi', related_name='certificates')
    
    # Sertifikat
    certificate_image = models.ImageField('Sertifikat rasmi', upload_to='certificates/%Y/%m/')
    certificate_number = models.CharField('Sertifikat raqami', max_length=50, unique=True)
    
    # Ball / Natija
    score = models.CharField('Ball / Natija', max_length=50, blank=True, 
                            help_text='Masalan: IELTS 7.5, 95/100')
    
    # Sana
    issue_date = models.DateField('Berilgan sana')
    
    # Saytda ko'rsatish
    is_featured = models.BooleanField('Asosiy sahifada ko\'rsatish?', default=False)
    order = models.IntegerField('Tartib', default=0)
    
    created_at = models.DateTimeField('Qo\'shilgan', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Sertifikat'
        verbose_name_plural = 'Sertifikatlar'
        ordering = ['-is_featured', 'order', '-issue_date']
    
    def __str__(self):
        return f"{self.student_name} - {self.certificate_number}"


# ==================== YANGILIKLAR ====================
class News(models.Model):
    """Yangiliklar va blog"""
    
    title = models.CharField('Sarlavha', max_length=200)
    slug = models.SlugField('Slug', max_length=220, unique=True, blank=True)
    
    # Rasmlar
    main_image = models.ImageField('Asosiy rasm', upload_to='news/%Y/%m/')
    thumbnail = models.ImageField('Kichik rasm', upload_to='news/thumbs/%Y/%m/', blank=True, null=True)
    
    # Kontent
    short_description = models.CharField('Qisqacha', max_length=300)
    content = models.TextField('To\'liq kontent')
    
    # Qo'shimcha rasmlar (ichki sahifada)
    gallery_images = models.ManyToManyField('NewsGalleryImage', verbose_name='Galereya rasmlari', 
                                           blank=True, related_name='news_items')
    
    # Muallif
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                              verbose_name='Muallif', related_name='news', blank=True)
    
    # SEO
    meta_keywords = models.CharField('Kalit so\'zlar (SEO)', max_length=255, blank=True)
    
    # Sozlamalar
    is_published = models.BooleanField('Nashr qilingan?', default=False)
    is_featured = models.BooleanField('Asosiy sahifada?', default=False)
    
    # Statistika
    views_count = models.IntegerField('Ko\'rishlar', default=0, editable=False)
    
    # Sanalar
    publish_date = models.DateTimeField('Nashr sanasi', blank=True, null=True)
    created_at = models.DateTimeField('Yaratilgan', auto_now_add=True)
    updated_at = models.DateTimeField('Yangilangan', auto_now=True)
    
    class Meta:
        verbose_name = 'Yangilik'
        verbose_name_plural = 'Yangiliklar'
        ordering = ['-publish_date', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})


class NewsGalleryImage(models.Model):
    """Yangilik ichidagi qo'shimcha rasmlar"""
    image = models.ImageField('Rasm', upload_to='news/gallery/%Y/%m/')
    caption = models.CharField('Izoh', max_length=200, blank=True)
    order = models.IntegerField('Tartib', default=0)
    
    class Meta:
        verbose_name = 'Yangilik galereya rasmi'
        verbose_name_plural = 'Yangilik galereya rasmlari'
        ordering = ['order']
    
    def __str__(self):
        return f"Rasm #{self.id}"


# ==================== GALEREYA ====================
class GalleryCategory(models.Model):
    """Galereya kategoriyalari"""
    name = models.CharField('Kategoriya nomi', max_length=100)
    slug = models.SlugField('Slug', unique=True, blank=True)
    description = models.TextField('Tavsif', blank=True)
    order = models.IntegerField('Tartib', default=0)
    
    class Meta:
        verbose_name = 'Galereya kategoriyasi'
        verbose_name_plural = 'Galereya kategoriyalari'
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Gallery(models.Model):
    """Galereya rasmlari"""
    
    title = models.CharField('Sarlavha', max_length=200, blank=True)
    image = models.ImageField('Rasm', upload_to='gallery/%Y/%m/')
    category = models.ForeignKey(GalleryCategory, on_delete=models.SET_NULL, 
                                 null=True, blank=True, verbose_name='Kategoriya',
                                 related_name='images')
    
    description = models.TextField('Tavsif', blank=True)
    
    # Sozlamalar
    is_featured = models.BooleanField('Asosiy sahifada?', default=False)
    order = models.IntegerField('Tartib', default=0)
    
    created_at = models.DateTimeField('Qo\'shilgan', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Galereya rasmi'
        verbose_name_plural = 'Galereya rasmlari'
        ordering = ['-is_featured', 'order', '-created_at']
    
    def __str__(self):
        return self.title or f"Rasm #{self.id}"

    @property
    def display_title(self):
        if self.title:
            return self.title
        if self.category:
            return self.category.name
        return "Galereya rasmi"


# ==================== ALOQA / KONTAKT ====================
class Contact(models.Model):
    """Umumiy aloqa so'rovlari"""
    
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('in_progress', 'Ko\'rib chiqilmoqda'),
        ('completed', 'Tugallangan'),
    ]
    
    # Ma'lumotlar
    full_name = models.CharField('To\'liq ism', max_length=200)
    phone = models.CharField('Telefon', max_length=20)
    email = models.EmailField('Email', blank=True, null=True)
    
    # Xabar
    subject = models.CharField('Mavzu', max_length=200, blank=True)
    message = models.TextField('Xabar')
    
    # Status
    status = models.CharField('Holat', max_length=20, choices=STATUS_CHOICES, default='new')
    is_read = models.BooleanField('O\'qilgan?', default=False)
    admin_notes = models.TextField('Admin eslatmasi', blank=True)
    
    # Sana
    created_at = models.DateTimeField('Yuborilgan', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Aloqa so\'rovi'
        verbose_name_plural = 'Aloqa so\'rovlari'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.phone}"


# ==================== O'QITUVCHI BO'LISH SO'ROVI ====================
class TeacherApplication(models.Model):
    """O'qituvchi bo'lish uchun arizalar"""
    
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('reviewed', 'Ko\'rib chiqildi'),
        ('accepted', 'Qabul qilindi'),
        ('rejected', 'Rad etildi'),
    ]
    
    # Shaxsiy ma'lumotlar
    first_name = models.CharField('Ism', max_length=100)
    last_name = models.CharField('Familiya', max_length=100)
    phone = models.CharField('Telefon', max_length=20)
    email = models.EmailField('Email')
    
    # Ta'lim
    education = models.CharField('Ta\'lim', max_length=200)
    experience_years = models.IntegerField('Tajriba (yillar)')
    
    # Ixtisoslik
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True,
                               verbose_name='Ixtisoslik')
    
    # Sertifikatlar va CV
    certificates = models.FileField('Sertifikatlar', upload_to='teacher_applications/certs/%Y/%m/', 
                                    blank=True, null=True)
    cv_file = models.FileField('CV / Resume', upload_to='teacher_applications/cv/%Y/%m/')
    photo = models.ImageField('Rasm', upload_to='teacher_applications/photos/%Y/%m/', 
                             blank=True, null=True)
    
    # Qo'shimcha
    about_me = models.TextField('Men haqimda')
    why_teach = models.TextField('Nega o\'qituvchi bo\'lishni istayman?')
    
    # Status
    status = models.CharField('Holat', max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField('Admin izohi', blank=True)
    
    # Sanalar
    created_at = models.DateTimeField('Yuborilgan', auto_now_add=True)
    reviewed_at = models.DateTimeField('Ko\'rilgan', blank=True, null=True)
    
    class Meta:
        verbose_name = 'O\'qituvchilikka ariza'
        verbose_name_plural = 'O\'qituvchilikka arizalar'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_status_display()}"


# ==================== SHARHLAR / TESTIMONIAL ====================
class Testimonial(models.Model):
    """Talabalar sharhlari"""
    
    student_name = models.CharField('Talaba ismi', max_length=200)
    student_photo = models.ImageField('Talaba rasmi', upload_to='testimonials/%Y/%m/', 
                                     blank=True, null=True)
    
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Kurs', related_name='testimonials')
    
    rating = models.IntegerField('Reyting', choices=[(i, f'{i} yulduz') for i in range(1, 6)],
                                default=5)
    
    comment = models.TextField('Sharh')
    
    # Qo'shimcha
    achievement = models.CharField('Erishilgan natija', max_length=200, blank=True,
                                  help_text='Masalan: IELTS 7.5 oldi')
    
    # Sozlamalar
    is_approved = models.BooleanField('Tasdiqlangan?', default=False)
    is_featured = models.BooleanField('Asosiy sahifada?', default=False)
    order = models.IntegerField('Tartib', default=0)
    
    created_at = models.DateTimeField('Qo\'shilgan', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Sharh'
        verbose_name_plural = 'Sharhlar'
        ordering = ['-is_featured', 'order', '-created_at']
    
    def __str__(self):
        return f"{self.student_name} - {self.rating} yulduz"


# ==================== FAQ ====================
class FAQCategory(models.Model):
    """FAQ kategoriyalari"""
    name = models.CharField('Kategoriya', max_length=100)
    order = models.IntegerField('Tartib', default=0)
    
    class Meta:
        verbose_name = 'FAQ kategoriyasi'
        verbose_name_plural = 'FAQ kategoriyalari'
        ordering = ['order']
    
    def __str__(self):
        return self.name


class FAQ(models.Model):
    """Ko'p beriladigan savollar"""
    
    category = models.ForeignKey(FAQCategory, on_delete=models.SET_NULL, null=True, blank=True,
                                 verbose_name='Kategoriya', related_name='faqs')
    
    question = models.CharField('Savol', max_length=300)
    answer = models.TextField('Javob')
    
    order = models.IntegerField('Tartib', default=0)
    is_active = models.BooleanField('Faolmi?', default=True)
    
    created_at = models.DateTimeField('Qo\'shilgan', auto_now_add=True)
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order']
    
    def __str__(self):
        return self.question


# ==================== SAYT SOZLAMALARI ====================
class SiteSettings(models.Model):
    """Sayt umumiy sozlamalari (Singleton)"""
    
    # Asosiy
    site_name = models.CharField('Sayt nomi', max_length=200, default='O\'quv Markazi')
    site_tagline = models.CharField('Slogan', max_length=300, blank=True)
    logo = models.ImageField('Logo', upload_to='site/', blank=True, null=True)
    favicon = models.ImageField('Favicon', upload_to='site/', blank=True, null=True)
    
    # Aloqa
    phone_primary = models.CharField('Asosiy telefon', max_length=20)
    phone_secondary = models.CharField('Qo\'shimcha telefon', max_length=20, blank=True)
    email = models.EmailField('Email')
    address = models.TextField('Manzil')
    
    # Ish vaqti
    working_hours = models.CharField('Ish vaqti', max_length=200, 
                                     default='Dushanba-Shanba: 9:00 - 18:00')
    
    # Haqida
    about_short = models.TextField('Qisqacha haqimizda', max_length=500, blank=True,
                                   help_text='Asosiy sahifa uchun')
    about_full = models.TextField('To\'liq haqimizda', blank=True,
                                  help_text='Haqimizda sahifasi uchun')
    
    # Ijtimoiy tarmoqlar
    facebook = models.URLField('Facebook', blank=True)
    instagram = models.URLField('Instagram', blank=True)
    telegram = models.URLField('Telegram', blank=True)
    youtube = models.URLField('YouTube', blank=True)
    linkedin = models.URLField('LinkedIn', blank=True)
    twitter = models.URLField('Twitter', blank=True)
    tiktok = models.URLField('TikTok', blank=True)
    
    # Xarita
    google_maps_embed = models.TextField('Google Maps embed kodi', blank=True)
    google_maps_link = models.URLField('Google Maps link', blank=True)
    
    # SEO
    meta_description = models.CharField('Meta tavsif', max_length=160, blank=True)
    meta_keywords = models.CharField('Meta kalit so\'zlar', max_length=255, blank=True)
    
    # Statistika (ko'rsatish uchun)
    students_count = models.IntegerField('Talabalar soni', default=0, 
                                        help_text='Saytda ko\'rsatish uchun')
    teachers_count = models.IntegerField('O\'qituvchilar soni', default=0)
    courses_count = models.IntegerField('Kurslar soni', default=0)
    success_rate = models.IntegerField('Muvaffaqiyat foizi', default=95,
                                      validators=[MinValueValidator(0), MaxValueValidator(100)])
    
    updated_at = models.DateTimeField('Yangilangan', auto_now=True)
    
    class Meta:
        verbose_name = 'Sayt sozlamalari'
        verbose_name_plural = 'Sayt sozlamalari'
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj