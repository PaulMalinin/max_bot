from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Status(models.TextChoices):
        AUTO_CHECK = "auto_check", "Автопроверка"
        ON_REVIEW = "on_review", "У модератора"
        APPROVED = "approved", "Опубликовано"
        REJECTED = "rejected", "Отклонено"

    file = models.ImageField(upload_to="photos/%Y/%m/")
    caption = models.CharField(max_length=256, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="photos")

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="photos",
    )
    consent_at = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AUTO_CHECK,
    )
    comment = models.TextField(blank=True)
    moderated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="moderated_photos",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    moderated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.caption or 'Без подписи'} ({self.get_status_display()})"
