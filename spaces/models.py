from django.db import models
from django.conf import settings


class Space(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class SpaceMember(models.Model):

    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('editor', 'Editor'),
        ('viewer', 'Viewer'),
    ]

    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        related_name='members'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='viewer'
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('space', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.space.name}"

class SpaceActivity(models.Model):

    ACTION_CHOICES = [
        ("SPACE_CREATED", "Space Created"),
        ("DOCUMENT_ADDED", "Document Added"),
        ("DOCUMENT_UPDATED", "Document Updated"),
        ("DOCUMENT_DELETED", "Document Deleted"),
        ("MEMBER_JOINED", "Member Joined"),
        ("MEMBER_REMOVED", "Member Removed"),
    ]

    space = models.ForeignKey(
        Space,
        on_delete=models.CASCADE,
        related_name="activities"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    action = models.CharField(
        max_length=30,
        choices=ACTION_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.action}"