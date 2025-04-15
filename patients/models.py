from django.db import models
from django.contrib import admin
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _


# تعریف گزینه‌های انتخابی برای نوع عمل و پزشک
SURGERY_TYPES = [
    ('intertro', _('جراحی اینترتروکانتریک')),
    ('brain', _('جراحی مغز')),

]

DOCTORS = [
    ('dr_zandi',_('دکتر زندی')),

]
DEFAULT_INSTRUCTIONS = {
    'intertro': {
        'warning_signs': _('تب، درد قفسه سینه، تنگی نفس'),
        'medication_instructions': _('روزانه داروهای رقیق‌کننده خون مصرف کنید.'),
        'next_visit': _('بعد از 1 ماه.'),
        'outpatient_services': _('بررسی‌های منظم ECG.'),
        'self_care_recommendations': _('از استرس دوری کنید و غذای کم چرب مصرف کنید.'),
        'nutrition': _('مصرف امگا ۳ را افزایش دهید.')
    },
    'brain': {
        'warning_signs': _('سرگیجه، سردرد شدید، حالت تهوع'),
        'medication_instructions': _('داروهای تجویزی مسکن مصرف کنید.'),
        'next_visit': _('بعد از ۲ هفته.'),
        'outpatient_services': _('MRI در صورت ادامه علائم.'),
        'self_care_recommendations': _('از استفاده بیش از حد از صفحه نمایش خودداری کنید.'),
        'nutrition': _('غذاهای مغزی مانند گردو و ماهی مصرف کنید.')}
}


# مدیریت کاربران
class UserManager(BaseUserManager):
    def create_user(self, national_id, phone_number, surgery_type=None, doctor=None, password=None):
        if not national_id:
            raise ValueError(_('کاربران باید کد ملی داشته باشند'))
        user = self.model(national_id=national_id, phone_number=phone_number, surgery_type=surgery_type, doctor=doctor)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, national_id, phone_number, surgery_type=None, doctor=None, password=None):
        user = self.create_user(national_id, phone_number, surgery_type, doctor, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# مدل کاربر
class User(AbstractBaseUser):
    age = models.PositiveIntegerField(_('سن'),blank=True, null=True)
    daronum = models.PositiveIntegerField(_('کد رهگیری دارو'),blank=True, null=True)
    first_name = models.CharField(_('نام'),max_length=30 , blank=True, null=True)
    last_name = models.CharField(_('نام خانوادگی'),max_length=30 , blank=True, null=True)
    national_id = models.CharField(_('کد ملی'), max_length=10, unique=True)
    phone_number = models.CharField(_('شماره تلفن'), max_length=15, unique=True)
    surgery_type = models.CharField(_('نوع عمل'), max_length=20, choices=SURGERY_TYPES, null=True, blank=True)
    doctor = models.CharField(_('دکتر معالج'), max_length=20, choices=DOCTORS, null=True, blank=True)
    warning_signs = models.TextField(_('علائم هشدار'), blank=True, default='')
    medication_instructions = models.TextField(_('دستورات دارویی'), blank=True, default='')
    next_visit = models.CharField(_('تاریخ ویزیت بعدی'), max_length=100, blank=True, default='')
    outpatient_services = models.TextField(_('خدمات سرپایی'), blank=True, default='')
    self_care_recommendations = models.TextField(_('توصیه‌های خود مراقبتی'), blank=True, default='')
    nutrition = models.TextField(_('توصیه‌های تغذیه‌ای'), blank=True, default='')
    is_active = models.BooleanField(_('فعال'), default=True)
    is_admin = models.BooleanField(_('مدیر'), default=False)
    password = models.CharField(_('رمز عبور'), max_length=128, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'national_id'
    REQUIRED_FIELDS = ['phone_number']

    def save(self, *args, **kwargs):
        if self._state.adding and self.surgery_type:  # مقداردهی پیش‌فرض فقط هنگام ایجاد کاربر جدید
            defaults = DEFAULT_INSTRUCTIONS.get(self.surgery_type, {})
            if not self.warning_signs:
                self.warning_signs = defaults.get('warning_signs', '')
            if not self.medication_instructions:
                self.medication_instructions = defaults.get('medication_instructions', '')
            if not self.next_visit:
                self.next_visit = defaults.get('next_visit', '')
            if not self.outpatient_services:
                self.outpatient_services = defaults.get('outpatient_services', '')
            if not self.self_care_recommendations:
                self.self_care_recommendations = defaults.get('self_care_recommendations', '')
            if not self.nutrition:
                self.nutrition = defaults.get('nutrition', '')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.national_id

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


# تنظیمات پنل ادمین
class UserAdmin(admin.ModelAdmin):
    list_display = ('national_id', 'phone_number' ,  'first_name', 'last_name','daronum', 'age', 'phone_number', 'surgery_type',)
    search_fields = ['national_id', 'phone_number']
    list_filter = ('surgery_type', 'doctor')
    exclude = ('password', 'last_login','is_admin')
    fieldsets = (
        (_('اطلاعات شخصی'), {'fields': ('national_id', 'phone_number')}),
        (_('اطلاعات پزشکی'), {'fields': ('surgery_type', 'doctor')}),
        (_('دستورات و توصیه‌ها'), {'fields': (
        'warning_signs', 'medication_instructions', 'next_visit', 'outpatient_services', 'self_care_recommendations',
        'nutrition')}),
    )


# ثبت مدل در ادمین
admin.site.register(User, UserAdmin)


