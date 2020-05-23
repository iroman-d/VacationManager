from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from enum import Enum
from django.forms.models import model_to_dict


class UserProfileManager(models.Manager):
    def get_queryset(self):
        return super(UserProfileManager, self).get_queryset().filter(city='London')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    phone = models.CharField(max_length=100, default='')
    is_manager = models.BooleanField('manager status', default=False)
    is_employee = models.BooleanField('employee status', default=True)

    def __str__(self):
        return self.user.username


class StatusChoice(Enum):
    REQUESTED = "Requested"
    APPROVED = "Approved"
    Denied = "Denied"


class VacationRequest(models.Model):
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    reviewed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    title = models.CharField(max_length=100, default='')
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.CharField(max_length=100, default='')
    status = models.CharField(
      max_length=5,
      choices=[(tag, tag.value) for tag in StatusChoice]  # Choices is a list of Tuple
    )
    category = models.CharField(max_length=100, default='')


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


def create_request(user_id, start_date, end_date, title, description, category):
    vacation = VacationRequest.objects.create(requested_by=user_id, title=title, start_date=start_date, end_date=end_date, description=description, category=category, status=StatusChoice.REQUESTED.value, reviewed_by=user_id)
    vacation.save()


def approve_request(request_id, reviewer_id):
    vacation = VacationRequest.objects.get(id=request_id)
    vacation.status = StatusChoice.APPROVED.value
    vacation.reviewed_by = reviewer_id
    vacation.save()


def denied_request(request_id, reviewer_id):
    vacation = VacationRequest.objects.get(id=request_id)
    vacation.status = StatusChoice.Denied.value
    vacation.reviewed_by = reviewer_id
    vacation.save()


def get_all_users():
    return {user.id : model_to_dict(user) for user in User.objects.all()}


def get_all_requests():
    result = []
    users = get_all_users()
    for request in VacationRequest.objects.filter(status=StatusChoice.REQUESTED.value).all():
        user = users[request.requested_by_id]
        result.append(dict(model_to_dict(request),**{'requested_by': request.requested_by_id,'first_name':user['first_name'],'last_name':user['last_name'],'email':user['email']}))
    return result


def get_my_requests(user_id):
    result = []
    user = model_to_dict(User.objects.get(id=user_id))
    for request in VacationRequest.objects.filter(requested_by=user_id).all():
        result.append(dict(model_to_dict(request),**{'requested_by': request.requested_by_id,'first_name':user['first_name'],'last_name':user['last_name'],'email':user['email']}))
    return result

post_save.connect(create_profile, sender=User)
