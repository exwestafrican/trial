from django.db import models
from django.contrib.auth.models import User as UserModel


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CompanyModel(TimeStampMixin):
    name = models.CharField(max_length=225)
    address = models.CharField(max_length=225)
    city = models.CharField(max_length=225)
    domain = models.CharField(max_length=225, unique=True)  # add index to this
    country_iso = models.CharField(max_length=3)
    industry = models.CharField(max_length=225)

    def __str__(self):
        return "{} ({})".format(self.name, self.domain)


class CompanyMessagePromptModel(TimeStampMixin):
    content = models.CharField(max_length=500)
    company = models.ForeignKey(to=CompanyModel, on_delete=models.CASCADE)


class EmployeeModel(TimeStampMixin):
    user = models.ForeignKey(to=UserModel, on_delete=models.CASCADE)
    company = models.ForeignKey(to=CompanyModel, on_delete=models.CASCADE)
    is_author = models.BooleanField(default=False, help_text="user setup organzation")


class ConversationModel(TimeStampMixin):
    rating = models.PositiveIntegerField(null=True, blank=True)
    open = models.BooleanField(default=True)
    in_conversation_with = models.ForeignKey(to=CompanyModel, on_delete=models.CASCADE)
    user_role = models.CharField(max_length=20)


class MessageModel(TimeStampMixin):
    content = models.CharField(max_length=800)
    conversation = models.ForeignKey(to=ConversationModel, on_delete=models.CASCADE, related_name='conversation')
    from_organisation = models.BooleanField()
    seen = models.BooleanField(default=False)
    sender = models.ForeignKey(
        to=EmployeeModel, null=True, blank=True, on_delete=models.CASCADE
    )
