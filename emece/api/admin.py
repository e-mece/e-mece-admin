from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from api.models import User, UserEvent, Event

from api.resources import UserResource


class EmeceAdmin(admin. ModelAdmin):
    empty_value_display = '-empty-'

    def has_delete_permission(self, request, obj=None):
        return False


class UserEventInline(admin.TabularInline):
    model = UserEvent
    readonly_fields = ('user_id', 'event_id', 'active', 'approved', 'created', 'modified')

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if db_field.name == 'user':
            self.verbose_name = 'Kullanıcının Kayıtlı Olduğu Etkinlikler'
            kwargs['queryset'] = Event.objects.filter(userevent__user_id=request.id)
            return super().formfield_for_manytomany(db_field, request, **kwargs)
        elif db_field.name == 'event':
            self.verbose_name = 'Etkinliğe Kayıtlı Kullanıcılar'
            kwargs['queryset'] = User.objects.filter(userevent__event_id=request.id)
            return super().formfield_for_manytomany(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(User)
class UserAdmin(EmeceAdmin, ImportExportModelAdmin):
    resource_class = UserResource

    readonly_fields = [
        'id',
        'username',
        'first_name',
        'middle_name',
        'last_name',
        'tckn',
        'phone',
        'email'
    ]

    fieldsets = (
        ('Kisisel Bilgiler', {
            'fields':
                (
                    'id',
                    'username',
                    'first_name',
                    'middle_name',
                    'last_name',
                    'tckn',
                    'phone',
                    'email',
                )
        }),
        ('Duzenleme', {
            'fields': ('is_verified', 'type')
        }),
    )

    inlines = (UserEventInline,)


@admin.register(Event)
class EventAdmin(EmeceAdmin):
    readonly_fields = ['creator_id', 'approver_id', 'created', 'modified']

    fieldsets = (
        (None, {
            'fields': (
                'is_cancelled',
                'approved',
                'approver_id',
                'creator_id',
                'created',
                'modified'
            )
        }),
        ('Genel Bilgiler', {
            'fields': (
                'title',
                'description',
                'quota',
                'start_date',
                'end_date',
                'image',
                'point'
            )
        }),
        ('Yer Bilgisi', {
            'fields': (
                'city',
                'address',
                'latitude',
                'longitude',
            )
        }),
    )

    inlines = (UserEventInline,)

