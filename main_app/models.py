from django.db import models

class Service(models.Model):
    """نموذج الخدمة"""
    name = models.CharField(max_length=200, verbose_name="اسم الخدمة")
    description = models.TextField(verbose_name="وصف الخدمة")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="السعر")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="السعر بعد الخصم")
    category = models.CharField(max_length=200, verbose_name="الفئة")
    is_featured = models.BooleanField(default=False, verbose_name="خدمة مميزة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التحديث")

    class Meta:
        verbose_name = "الخدمة"
        verbose_name_plural = "الخدمات"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    """نموذج الشهادات"""
    name = models.CharField(max_length=100, verbose_name="الاسم")
    message = models.TextField(verbose_name="الرسالة")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="التقييم")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "الشهادة"
        verbose_name_plural = "الشهادات"
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ServiceRequest(models.Model):
    """نموذج طلب الخدمة"""
    name = models.CharField(max_length=100, verbose_name="الاسم")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    service = models.CharField(max_length=200, verbose_name="الخدمة المطلوبة")
    message = models.TextField(verbose_name="الرسالة")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الطلب")

    class Meta:
        verbose_name = "طلب الخدمة"
        verbose_name_plural = "طلبات الخدمات"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.service}"


class FAQ(models.Model):
    """نموذج الأسئلة الشائعة"""
    question = models.CharField(max_length=500, verbose_name="السؤال")
    answer = models.TextField(verbose_name="الإجابة")
    order = models.IntegerField(default=0, verbose_name="الترتيب")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإنشاء")

    class Meta:
        verbose_name = "السؤال الشائع"
        verbose_name_plural = "الأسئلة الشائعة"
        ordering = ['order']

    def __str__(self):
        return self.question
