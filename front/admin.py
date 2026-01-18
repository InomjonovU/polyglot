"""
PolyglotLC Admin Panel
Django Unfold Theme - Professional & Complete
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from django.db.models import Count

from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import (
    RangeDateFilter, RangeDateTimeFilter, RangeNumericFilter,
)
from unfold.decorators import display, action

from import_export.admin import ImportExportModelAdmin
from import_export import resources, fields

from .models import (
    User, Subject, Teacher, Course, CourseEnrollment,
    Certificate, News, NewsGalleryImage, GalleryCategory, Gallery,
    Contact, TeacherApplication, Testimonial, FAQCategory, FAQ, SiteSettings
)


# ══════════════════════════════════════════════════════════════════
#                    IMPORT/EXPORT RESOURCES
# ══════════════════════════════════════════════════════════════════

class TeacherResource(resources.ModelResource):
    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 
                  'education', 'ielts_score', 'experience_years', 'is_active')

class CourseResource(resources.ModelResource):
    class Meta:
        model = Course
        fields = ('id', 'title', 'subject__name', 'level', 'price', 
                  'discount_price', 'duration_months', 'is_active', 'is_featured')

class CertificateResource(resources.ModelResource):
    class Meta:
        model = Certificate
        fields = ('id', 'certificate_number', 'student_name', 'course__title',
                  'teacher__first_name', 'score', 'issue_date')

class CourseEnrollmentResource(resources.ModelResource):
    class Meta:
        model = CourseEnrollment
        fields = ('id', 'full_name', 'phone', 'email', 'course__title', 'status', 'created_at')


# ══════════════════════════════════════════════════════════════════
#                         USER ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    list_display = ('avatar_display', 'username', 'full_name_display', 'email', 'phone', 
                    'is_staff', 'is_active', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('-date_joined',)
    
    fieldsets = (
        ('👤 Kirish', {'fields': ('username', 'password')}),
        ('📋 Shaxsiy', {'fields': ('first_name', 'last_name', 'email', 'phone', 'profile_image')}),
        ('🔐 Ruxsatlar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'), 'classes': ('collapse',)}),
        ('📅 Sanalar', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    )
    
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name')}),)
    
    @display(description="")
    def avatar_display(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;"/>', obj.profile_image.url)
        initials = (obj.first_name[:1] + obj.last_name[:1]).upper() if obj.first_name else obj.username[:2].upper()
        return format_html('<div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#3b82f6,#1d4ed8);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:600;">{}</div>', initials)
    
    @display(description="F.I.O")
    def full_name_display(self, obj):
        return obj.get_full_name() or format_html('<span style="color:#94a3b8;">—</span>')


# ══════════════════════════════════════════════════════════════════
#                      SITE SETTINGS ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(SiteSettings)
class SiteSettingsAdmin(ModelAdmin):
    fieldsets = (
        ('🏢 Asosiy', {'fields': ('site_name', 'site_tagline', 'logo', 'favicon')}),
        ('📞 Aloqa', {'fields': (('phone_primary', 'phone_secondary'), 'email', 'address', 'working_hours')}),
        ('🌐 Ijtimoiy tarmoqlar', {'fields': (('telegram', 'instagram'), ('facebook', 'youtube'), ('linkedin', 'twitter'), 'tiktok'), 'classes': ('collapse',)}),
        ('📝 Haqimizda', {'fields': ('about_short', 'about_full')}),
        ('🗺️ Xarita', {'fields': ('google_maps_embed', 'google_maps_link'), 'classes': ('collapse',)}),
        ('📊 Statistika', {'fields': (('students_count', 'teachers_count'), ('courses_count', 'success_rate'))}),
        ('🔍 SEO', {'fields': ('meta_description', 'meta_keywords'), 'classes': ('collapse',)}),
    )
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


# ══════════════════════════════════════════════════════════════════
#                        SUBJECT ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ('icon_display', 'name', 'slug', 'courses_count', 'teachers_count', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order', 'is_active')
    ordering = ('order', 'name')
    
    fieldsets = (
        ('📚 Fan', {'fields': ('name', 'slug', 'description')}),
        ('🎨 Ko\'rinish', {'fields': ('icon', 'image', 'order')}),
        ('⚙️ Status', {'fields': ('is_active',)}),
    )
    
    @display(description="")
    def icon_display(self, obj):
        if obj.icon:
            return format_html('<i class="{}" style="font-size:24px;color:#3b82f6;"></i>', obj.icon)
        return "📚"
    
    @display(description="Kurslar")
    def courses_count(self, obj):
        count = obj.courses.filter(is_active=True).count()
        return format_html('<span style="background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:20px;">{}</span>', count)
    
    @display(description="O'qituvchilar")
    def teachers_count(self, obj):
        count = obj.teachers.filter(is_active=True).count()
        return format_html('<span style="background:#f0fdf4;color:#166534;padding:4px 12px;border-radius:20px;">{}</span>', count)


# ══════════════════════════════════════════════════════════════════
#                        TEACHER ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(Teacher)
class TeacherAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = TeacherResource
    
    list_display = ('photo_display', 'full_name', 'phone', 'email_display', 'scores_display', 
                    'experience_badge', 'courses_count', 'is_featured', 'is_active')
    list_filter = ('is_active', 'is_featured', 'specializations', ('experience_years', RangeNumericFilter), ('created_at', RangeDateFilter))
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    prepopulated_fields = {'slug': ('first_name', 'last_name')}
    filter_horizontal = ('specializations',)
    list_editable = ('is_featured', 'is_active')
    ordering = ('-is_featured', 'order', 'first_name')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('👤 Shaxsiy', {'fields': (('first_name', 'last_name'), 'slug', 'photo')}),
        ('📞 Aloqa', {'fields': (('phone', 'email'),)}),
        ('🎓 Ta\'lim', {'fields': ('education', ('experience_years', 'cefr_level'), ('ielts_score', 'toefl_score'), 'certificates_file')}),
        ('📚 Ixtisosliklar', {'fields': ('specializations',)}),
        ('📝 Bio', {'fields': ('bio', 'full_bio', 'skills')}),
        ('🌐 Ijtimoiy', {'fields': (('telegram', 'instagram'), ('facebook', 'linkedin')), 'classes': ('collapse',)}),
        ('⚙️ Sozlamalar', {'fields': (('is_active', 'is_featured'), 'order')}),
    )
    
    @display(description="")
    def photo_display(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:50px;height:50px;border-radius:50%;object-fit:cover;"/>', obj.photo.url)
        return format_html('<div style="width:50px;height:50px;border-radius:50%;background:#3b82f6;display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;">{}</div>', obj.first_name[0].upper() if obj.first_name else '?')
    
    @display(description="Email")
    def email_display(self, obj):
        return format_html('<a href="mailto:{}" style="color:#3b82f6;">{}</a>', obj.email, obj.email) if obj.email else "—"
    
    @display(description="Ballar")
    def scores_display(self, obj):
        parts = []
        if obj.ielts_score:
            c = '#10b981' if float(obj.ielts_score) >= 7 else '#f59e0b'
            parts.append(f'<span style="background:{c}20;color:{c};padding:2px 8px;border-radius:12px;font-size:12px;">IELTS {obj.ielts_score}</span>')
        if obj.cefr_level:
            parts.append(f'<span style="background:#8b5cf620;color:#8b5cf6;padding:2px 8px;border-radius:12px;font-size:12px;">{obj.cefr_level}</span>')
        return format_html('{}',' '.join(parts)) if parts else "—"
    
    @display(description="Tajriba")
    def experience_badge(self, obj):
        c = '#10b981' if obj.experience_years >= 5 else '#f59e0b' if obj.experience_years >= 3 else '#6b7280'
        return format_html('<span style="background:{}20;color:{};padding:4px 10px;border-radius:20px;font-size:12px;">{} yil</span>', c, c, obj.experience_years)
    
    @display(description="Kurslar")
    def courses_count(self, obj):
        return format_html('<span style="background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:20px;">📚 {}</span>', obj.courses.filter(is_active=True).count())


# ══════════════════════════════════════════════════════════════════
#                         COURSE ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(Course)
class CourseAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = CourseResource
    
    list_display = ('image_display', 'title', 'subject_badge', 'level_badge', 'price_display', 
                    'duration_display', 'stats_display', 'is_featured', 'is_popular', 'is_active')
    list_filter = ('is_active', 'is_featured', 'is_popular', 'subject',
                   'level', ('price', RangeNumericFilter), ('created_at', RangeDateFilter))
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('teachers',)
    list_editable = ('is_featured', 'is_popular', 'is_active')
    ordering = ('-is_featured', '-is_popular', 'order', '-created_at')
    date_hierarchy = 'created_at'
    readonly_fields = ('views_count', 'enrollments_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('📚 Asosiy', {'fields': ('title', 'slug', 'subject')}),
        ('🖼️ Rasmlar', {'fields': ('main_image', 'thumbnail')}),
        ('📝 Tavsif', {'fields': ('short_description', 'full_description')}),
        ('⚙️ Parametrlar', {'fields': (('level', 'duration_months'), ('lessons_per_week', 'lesson_duration'), 'start_date')}),
        ('💰 Narx', {'fields': (('price', 'discount_price'),)}),
        ('👨‍🏫 O\'qituvchilar', {'fields': ('teachers',)}),
        ('📋 Tafsilotlar', {'fields': ('what_you_learn', 'requirements', 'target_audience', 'syllabus', 'expected_results', 'certificate_info'), 'classes': ('collapse',)}),
        ('⭐ Status', {'fields': (('is_active', 'is_featured', 'is_popular'), 'order')}),
        ('📊 Statistika', {'fields': (('views_count', 'enrollments_count'), ('created_at', 'updated_at')), 'classes': ('collapse',)}),
    )
    
    @display(description="")
    def image_display(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="width:80px;height:50px;border-radius:8px;object-fit:cover;"/>', obj.main_image.url)
        return "📷"
    
    @display(description="Fan")
    def subject_badge(self, obj):
        return format_html('<span style="background:#f0fdf4;color:#166534;padding:4px 10px;border-radius:8px;font-size:12px;">{}</span>', obj.subject.name)
    
    @display(description="Daraja")
    def level_badge(self, obj):
        colors = {'beginner': '#10b981', 'elementary': '#06b6d4', 'pre_intermediate': '#3b82f6', 
                  'intermediate': '#8b5cf6', 'upper_intermediate': '#f59e0b', 'advanced': '#ef4444'}
        c = colors.get(obj.level, '#6b7280')
        return format_html('<span style="background:{}15;color:{};padding:4px 10px;border-radius:20px;font-size:11px;">{}</span>', c, c, obj.get_level_display())
    
    @display(description="Narx")
    def price_display(self, obj):
        if obj.has_discount:
            return format_html('<s style="color:#94a3b8;">{}</s> <b style="color:#10b981;">{}</b>', f'{obj.price:,.0f}', f'{obj.discount_price:,.0f}')
        return format_html('<b>{}</b>', f'{obj.price:,.0f}')
    
    @display(description="Muddat")
    def duration_display(self, obj):
        return format_html('<span style="color:#64748b;">{} oy · {}x/hafta</span>', obj.duration_months, obj.lessons_per_week)
    
    @display(description="Statistika")
    def stats_display(self, obj):
        return format_html('<span style="color:#64748b;font-size:12px;">👁{} 📝{}</span>', obj.views_count, obj.enrollments_count)


# ══════════════════════════════════════════════════════════════════
#                    COURSE ENROLLMENT ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = CourseEnrollmentResource
    
    list_display = ('id_display', 'full_name', 'phone_display', 'course_display', 'status_badge', 'created_at_display')
    list_filter = ('status', 'course', ('created_at', RangeDateTimeFilter))
    search_fields = ('full_name', 'phone', 'email', 'course__title')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('👤 Shaxsiy', {'fields': ('full_name', ('phone', 'email'))}),
        ('📚 Kurs', {'fields': ('course',)}),
        ('💬 Xabar', {'fields': ('message',)}),
        ('📊 Status', {'fields': ('status', 'admin_notes')}),
        ('📅 Sanalar', {'fields': (('created_at', 'updated_at'),), 'classes': ('collapse',)}),
    )
    
    actions = ['mark_contacted', 'mark_enrolled', 'mark_rejected']
    
    @display(description="ID")
    def id_display(self, obj):
        return format_html('<span style="background:#f1f5f9;padding:4px 10px;border-radius:8px;font-family:monospace;">#{}</span>', obj.id)
    
    @display(description="Telefon")
    def phone_display(self, obj):
        return format_html('<a href="tel:{}" style="color:#3b82f6;">{}</a>', obj.phone, obj.phone)
    
    @display(description="Kurs")
    def course_display(self, obj):
        return format_html('<span style="max-width:200px;display:block;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{}</span>', obj.course.title)
    
    @display(description="Status")
    def status_badge(self, obj):
        colors = {'pending': ('#f59e0b', '⏳'), 'contacted': ('#3b82f6', '📞'), 'enrolled': ('#10b981', '✅'), 'rejected': ('#ef4444', '❌')}
        c, e = colors.get(obj.status, ('#6b7280', '?'))
        return format_html('<span style="background:{}15;color:{};padding:6px 12px;border-radius:20px;font-weight:600;font-size:12px;">{} {}</span>', c, c, e, obj.get_status_display())
    
    @display(description="Yuborilgan")
    def created_at_display(self, obj):
        diff = timezone.now() - obj.created_at
        if diff.days == 0:
            h = diff.seconds // 3600
            return f"{h} soat oldin" if h > 0 else "Hozir"
        elif diff.days == 1:
            return "Kecha"
        elif diff.days < 7:
            return f"{diff.days} kun oldin"
        return obj.created_at.strftime("%d.%m.%Y")
    
    @action(description="📞 Aloqaga chiqildi")
    def mark_contacted(self, request, queryset):
        queryset.update(status='contacted')
    
    @action(description="✅ Yozildi")
    def mark_enrolled(self, request, queryset):
        queryset.update(status='enrolled')
    
    @action(description="❌ Rad etish")
    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')


# ══════════════════════════════════════════════════════════════════
#                     CERTIFICATE ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(Certificate)
class CertificateAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = CertificateResource
    
    list_display = ('cert_preview', 'certificate_number', 'student_name', 'course_display', 
                    'teacher_display', 'score_badge', 'issue_date', 'is_featured')
    list_filter = ('is_featured', 'course', 'teacher', ('issue_date', RangeDateFilter))
    search_fields = ('certificate_number', 'student_name', 'course__title')
    list_editable = ('is_featured',)
    ordering = ('-is_featured', 'order', '-issue_date')
    date_hierarchy = 'issue_date'
    
    fieldsets = (
        ('👤 Talaba', {'fields': ('student_name', 'student_photo')}),
        ('📜 Sertifikat', {'fields': ('certificate_number', 'certificate_image')}),
        ('📚 Kurs', {'fields': (('course', 'teacher'),)}),
        ('🏆 Natija', {'fields': (('score', 'issue_date'),)}),
        ('⚙️ Sozlamalar', {'fields': (('is_featured', 'order'),)}),
    )
    
    @display(description="")
    def cert_preview(self, obj):
        if obj.certificate_image:
            return format_html('<img src="{}" style="width:60px;height:45px;border-radius:6px;object-fit:cover;"/>', obj.certificate_image.url)
        return "📜"
    
    @display(description="Kurs")
    def course_display(self, obj):
        return obj.course.title if obj.course else "—"
    
    @display(description="O'qituvchi")
    def teacher_display(self, obj):
        return obj.teacher.full_name if obj.teacher else "—"
    
    @display(description="Ball")
    def score_badge(self, obj):
        if obj.score:
            return format_html('<span style="background:#10b98120;color:#10b981;padding:4px 12px;border-radius:20px;font-weight:700;">{}</span>', obj.score)
        return "—"


# ══════════════════════════════════════════════════════════════════
#                         NEWS ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(NewsGalleryImage)
class NewsGalleryImageAdmin(ModelAdmin):
    list_display = ('image_preview', 'caption', 'order')
    list_editable = ('order',)
    
    @display(description="Rasm")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:80px;height:60px;object-fit:cover;border-radius:8px;"/>', obj.image.url)
        return "📷"


@admin.register(News)
class NewsAdmin(ModelAdmin):
    list_display = ('image_display', 'title', 'author_display', 'views_count', 'publish_date', 'is_published', 'is_featured')
    list_filter = ('is_published', 'is_featured', ('publish_date', RangeDateTimeFilter))
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('gallery_images',)
    list_editable = ('is_published', 'is_featured')
    ordering = ('-publish_date', '-created_at')
    date_hierarchy = 'publish_date'
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    
    fieldsets = (
        ('📰 Asosiy', {'fields': ('title', 'slug', 'author')}),
        ('🖼️ Rasmlar', {'fields': ('main_image', 'thumbnail')}),
        ('📝 Kontent', {'fields': ('short_description', 'content')}),
        ('🖼️ Galereya', {'fields': ('gallery_images',), 'classes': ('collapse',)}),
        ('🔍 SEO', {'fields': ('meta_keywords',), 'classes': ('collapse',)}),
        ('⚙️ Sozlamalar', {'fields': (('is_published', 'is_featured'), 'publish_date')}),
        ('📊 Statistika', {'fields': ('views_count', ('created_at', 'updated_at')), 'classes': ('collapse',)}),
    )
    
    @display(description="")
    def image_display(self, obj):
        if obj.main_image:
            return format_html('<img src="{}" style="width:80px;height:50px;border-radius:8px;object-fit:cover;"/>', obj.main_image.url)
        return "📷"
    
    @display(description="Muallif")
    def author_display(self, obj):
        return obj.author.get_full_name() if obj.author else "—"


# ══════════════════════════════════════════════════════════════════
#                        GALLERY ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'images_count', 'order')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('order',)
    
    @display(description="Rasmlar")
    def images_count(self, obj):
        return format_html('<span style="background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:20px;">{}</span>', obj.images.count())


@admin.register(Gallery)
class GalleryAdmin(ModelAdmin):
    list_display = ('image_preview', 'title', 'category_badge', 'is_featured', 'order')
    list_filter = ('is_featured', 'category')
    search_fields = ('title', 'description')
    list_editable = ('is_featured', 'order')
    
    fieldsets = (
        ('🖼️ Rasm', {'fields': ('title', 'image', 'category')}),
        ('📝 Tavsif', {'fields': ('description',)}),
        ('⚙️ Sozlamalar', {'fields': (('is_featured', 'order'),)}),
    )
    
    @display(description="")
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:80px;height:60px;border-radius:8px;object-fit:cover;"/>', obj.image.url)
        return "📷"
    
    @display(description="Kategoriya")
    def category_badge(self, obj):
        if obj.category:
            return format_html('<span style="background:#f1f5f9;color:#475569;padding:4px 10px;border-radius:8px;font-size:12px;">{}</span>', obj.category.name)
        return "—"


# ══════════════════════════════════════════════════════════════════
#                        CONTACT ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(Contact)
class ContactAdmin(ModelAdmin):
    list_display = ('id_display', 'full_name', 'phone_display', 'subject_display', 'status_badge', 'is_read', 'created_at_display')
    list_filter = ('status', 'is_read', ('created_at', RangeDateTimeFilter))
    search_fields = ('full_name', 'phone', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('👤 Ma\'lumotlar', {'fields': ('full_name', ('phone', 'email'))}),
        ('💬 Xabar', {'fields': ('subject', 'message')}),
        ('📊 Status', {'fields': (('status', 'is_read'), 'admin_notes')}),
        ('📅 Sana', {'fields': ('created_at',)}),
    )
    
    actions = ['mark_as_read', 'mark_completed']
    
    @display(description="ID")
    def id_display(self, obj):
        return format_html('<span style="background:#f1f5f9;padding:4px 10px;border-radius:8px;font-family:monospace;">#{}</span>', obj.id)
    
    @display(description="Telefon")
    def phone_display(self, obj):
        return format_html('<a href="tel:{}" style="color:#3b82f6;">{}</a>', obj.phone, obj.phone)
    
    @display(description="Mavzu")
    def subject_display(self, obj):
        return obj.subject[:50] + "..." if obj.subject and len(obj.subject) > 50 else (obj.subject or "—")
    
    @display(description="Status")
    def status_badge(self, obj):
        colors = {'new': ('#ef4444', '🔴'), 'in_progress': ('#f59e0b', '🟡'), 'completed': ('#10b981', '🟢')}
        c, e = colors.get(obj.status, ('#6b7280', '⚪'))
        return format_html('<span style="background:{}15;color:{};padding:6px 12px;border-radius:20px;font-size:12px;">{} {}</span>', c, c, e, obj.get_status_display())
    
    @display(description="Yuborilgan")
    def created_at_display(self, obj):
        diff = timezone.now() - obj.created_at
        if diff.days == 0:
            return "Bugun"
        elif diff.days == 1:
            return "Kecha"
        return obj.created_at.strftime("%d.%m.%Y")
    
    @action(description="📖 O'qilgan deb belgilash")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    
    @action(description="✅ Tugallangan deb belgilash")
    def mark_completed(self, request, queryset):
        queryset.update(status='completed', is_read=True)


# ══════════════════════════════════════════════════════════════════
#                   TEACHER APPLICATION ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(TeacherApplication)
class TeacherApplicationAdmin(ModelAdmin):
    list_display = ('photo_display', 'full_name_display', 'phone_display', 'subject_badge', 
                    'experience_badge', 'status_badge', 'created_at')
    list_filter = ('status', 'subject', ('experience_years', RangeNumericFilter), ('created_at', RangeDateTimeFilter))
    search_fields = ('first_name', 'last_name', 'phone', 'email')
    readonly_fields = ('created_at', 'reviewed_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('👤 Shaxsiy', {'fields': (('first_name', 'last_name'), ('phone', 'email'), 'photo')}),
        ('🎓 Ta\'lim', {'fields': ('education', ('experience_years', 'subject'))}),
        ('📎 Fayllar', {'fields': ('cv_file', 'certificates')}),
        ('📝 Motivatsiya', {'fields': ('about_me', 'why_teach')}),
        ('📊 Status', {'fields': ('status', 'admin_notes')}),
        ('📅 Sanalar', {'fields': (('created_at', 'reviewed_at'),), 'classes': ('collapse',)}),
    )
    
    actions = ['mark_reviewed', 'mark_accepted', 'mark_rejected', 'create_teacher']
    
    @display(description="")
    def photo_display(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width:45px;height:45px;border-radius:50%;object-fit:cover;"/>', obj.photo.url)
        return "👤"
    
    @display(description="F.I.O")
    def full_name_display(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    @display(description="Telefon")
    def phone_display(self, obj):
        return format_html('<a href="tel:{}" style="color:#3b82f6;">{}</a>', obj.phone, obj.phone)
    
    @display(description="Ixtisoslik")
    def subject_badge(self, obj):
        if obj.subject:
            return format_html('<span style="background:#f0fdf4;color:#166534;padding:4px 10px;border-radius:8px;font-size:12px;">{}</span>', obj.subject.name)
        return "—"
    
    @display(description="Tajriba")
    def experience_badge(self, obj):
        c = '#10b981' if obj.experience_years >= 5 else '#f59e0b' if obj.experience_years >= 3 else '#6b7280'
        return format_html('<span style="background:{}20;color:{};padding:4px 10px;border-radius:20px;font-size:12px;">{} yil</span>', c, c, obj.experience_years)
    
    @display(description="Status")
    def status_badge(self, obj):
        colors = {'pending': ('#f59e0b', '⏳'), 'reviewed': ('#3b82f6', '🔍'), 'accepted': ('#10b981', '✅'), 'rejected': ('#ef4444', '❌')}
        c, e = colors.get(obj.status, ('#6b7280', '?'))
        return format_html('<span style="background:{}15;color:{};padding:6px 12px;border-radius:20px;font-size:12px;">{} {}</span>', c, c, e, obj.get_status_display())
    
    @action(description="🔍 Ko'rildi")
    def mark_reviewed(self, request, queryset):
        queryset.update(status='reviewed', reviewed_at=timezone.now())
    
    @action(description="✅ Qabul qilish")
    def mark_accepted(self, request, queryset):
        queryset.update(status='accepted', reviewed_at=timezone.now())
    
    @action(description="❌ Rad etish")
    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected', reviewed_at=timezone.now())
    
    @action(description="👨‍🏫 O'qituvchi yaratish")
    def create_teacher(self, request, queryset):
        created = 0
        for app in queryset.filter(status='accepted'):
            teacher, is_new = Teacher.objects.get_or_create(
                first_name=app.first_name, last_name=app.last_name,
                defaults={'phone': app.phone, 'email': app.email, 'education': app.education,
                         'experience_years': app.experience_years, 'bio': app.about_me[:500],
                         'full_bio': app.about_me + '\n\n' + app.why_teach, 'photo': app.photo}
            )
            if is_new and app.subject:
                teacher.specializations.add(app.subject)
                created += 1
        self.message_user(request, f'{created} ta o\'qituvchi yaratildi.')


# ══════════════════════════════════════════════════════════════════
#                      TESTIMONIAL ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ('photo_display', 'student_name', 'course_display', 'rating_display', 
                    'achievement_badge', 'is_approved', 'is_featured')
    list_filter = ('is_approved', 'is_featured', 'rating', 'course')
    search_fields = ('student_name', 'comment', 'achievement')
    list_editable = ('is_approved', 'is_featured')
    ordering = ('-is_featured', 'order', '-created_at')
    
    fieldsets = (
        ('👤 Talaba', {'fields': ('student_name', 'student_photo', 'course')}),
        ('⭐ Baho', {'fields': ('rating', 'comment')}),
        ('🏆 Yutuq', {'fields': ('achievement',)}),
        ('⚙️ Sozlamalar', {'fields': (('is_approved', 'is_featured'), 'order')}),
    )
    
    actions = ['approve', 'unapprove']
    
    @display(description="")
    def photo_display(self, obj):
        if obj.student_photo:
            return format_html('<img src="{}" style="width:45px;height:45px;border-radius:50%;object-fit:cover;"/>', obj.student_photo.url)
        return format_html('<div style="width:45px;height:45px;border-radius:50%;background:#3b82f6;display:flex;align-items:center;justify-content:center;color:#fff;">{}</div>', obj.student_name[0].upper())
    
    @display(description="Kurs")
    def course_display(self, obj):
        return obj.course.title if obj.course else "—"
    
    @display(description="Reyting")
    def rating_display(self, obj):
        return format_html('<span style="font-size:14px;">{}</span>', '⭐' * obj.rating + '☆' * (5 - obj.rating))
    
    @display(description="Yutuq")
    def achievement_badge(self, obj):
        if obj.achievement:
            return format_html('<span style="background:#10b98120;color:#10b981;padding:4px 10px;border-radius:8px;font-size:12px;">🏆 {}</span>', obj.achievement)
        return "—"
    
    @action(description="✅ Tasdiqlash")
    def approve(self, request, queryset):
        queryset.update(is_approved=True)
    
    @action(description="❌ Bekor qilish")
    def unapprove(self, request, queryset):
        queryset.update(is_approved=False)


# ══════════════════════════════════════════════════════════════════
#                          FAQ ADMIN
# ══════════════════════════════════════════════════════════════════

@admin.register(FAQCategory)
class FAQCategoryAdmin(ModelAdmin):
    list_display = ('name', 'faqs_count', 'order')
    list_editable = ('order',)
    
    @display(description="Savollar")
    def faqs_count(self, obj):
        return format_html('<span style="background:#dbeafe;color:#1d4ed8;padding:4px 12px;border-radius:20px;">{}</span>', obj.faqs.filter(is_active=True).count())


@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ('question_display', 'category_badge', 'order', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_active')
    ordering = ('category', 'order')
    
    fieldsets = (
        ('❓ Savol-javob', {'fields': ('question', 'answer')}),
        ('📁 Kategoriya', {'fields': (('category', 'order'),)}),
        ('⚙️ Status', {'fields': ('is_active',)}),
    )
    
    @display(description="Savol")
    def question_display(self, obj):
        return obj.question[:80] + '...' if len(obj.question) > 80 else obj.question
    
    @display(description="Kategoriya")
    def category_badge(self, obj):
        if obj.category:
            return format_html('<span style="background:#f1f5f9;color:#475569;padding:4px 10px;border-radius:8px;font-size:12px;">{}</span>', obj.category.name)
        return "Umumiy"


# ══════════════════════════════════════════════════════════════════
#                    ADMIN SITE CUSTOMIZATION
# ══════════════════════════════════════════════════════════════════

admin.site.site_header = "🎓 PolyglotLC Admin"
admin.site.site_title = "PolyglotLC"
admin.site.index_title = "Boshqaruv paneli"