from tastypie.resources import ModelResource
from tastypie.authorization import Authorization

from .models import AuthUser, User, UserEvent, Event


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()


class AuthUserResource(ModelResource):
    class Meta:
        queryset = AuthUser.objects.all()
        resource_name = 'auth_user'
        authorization = Authorization


class EventResource(ModelResource):
    class Meta:
        queryset = Event.objects.all()
        resource_name = 'event'
        authorization = Authorization


class UserEventResource(ModelResource):
    class Meta:
        queryset = UserEvent.objects.all()
        resource_name = 'user_event'
        authorization = Authorization
