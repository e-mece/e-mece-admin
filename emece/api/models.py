from django.db import models

class EmeceBaseModel(models.Model):
    id = models.IntegerField(primary_key=True)
    created = models.DateTimeField(verbose_name='Oluşturulma Zamanı')
    modified = models.DateTimeField(verbose_name='Son Değiştirilme Zamanı')

    class Meta:
        managed = False
        abstract = True


class EmeceBaseRelation(models.Model):
    created = models.DateTimeField()
    modified = models.DateTimeField()

    class Meta:
        managed = False
        abstract = True


class User(EmeceBaseModel):
    username = models.CharField(max_length=255, verbose_name='Kullanıcı Adı')
    password_hash = models.TextField(db_column='passwordHash')
    email = models.CharField(max_length=255, verbose_name='Email Adresi')
    first_name = models.TextField(db_column='firstName', verbose_name='İsim')
    last_name = models.TextField(db_column='lastName', verbose_name='Soyisim')
    middle_name = models.TextField(db_column='middleName', default='', verbose_name='İkinci İsim')
    image = models.TextField(null=True, verbose_name='Fotoğraf')
    is_verified = models.BooleanField(db_column='emailVerified', verbose_name='Onaylandı mı?')
    birth_date = models.DateField(db_column='birthDate', null=True, verbose_name='Doğum Tarihi')
    tckn = models.CharField(db_column='TCKN', max_length=11, verbose_name='TC Kimlik No')
    city = models.CharField(max_length=255, verbose_name='Şehir')
    phone = models.TextField(verbose_name='Telefon Numarası')

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        managed = False
        db_table = 'user'

    def __str__(self):
        return f'TCKN<{self.tckn}>'


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_user'


class Event(EmeceBaseModel):
    title = models.CharField(max_length=255, null=False)
    description = models.CharField(max_length=4095, null=False)
    city = models.CharField(max_length=255, null=False)
    address = models.CharField(max_length=255, null=False)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    start_date = models.DateTimeField(db_column='startDate', null=False)
    end_date = models.DateTimeField(db_column='endDate', null=False)
    quota = models.IntegerField(null=False)
    image = models.CharField(max_length=511, null=True)
    approved = models.BooleanField(null=False, default=False)
    point = models.IntegerField(null=True)
    creator_id = models.ForeignKey('User',
                                  on_delete=models.DO_NOTHING,
                                  db_column='creatorId')
    approver_id = models.IntegerField(db_column='approverId')

    # approver_id = models.ForeignKey('AuthUser',
    #                                on_delete=models.DO_NOTHING,
    #                                 db_column='approverId')

    class Meta:
        verbose_name = 'Etkinlik'
        verbose_name_plural = 'Etkinlikler'
        managed = False
        db_table = 'event'

    def __str__(self):
        return "[%d] %s" % (self.id, self.title)


class UserEvent(EmeceBaseRelation):
    user_id = models.OneToOneField('User',
                                on_delete=models.CASCADE,
                                db_column='userId',
                                verbose_name='Kullanici ID')
    event_id = models.OneToOneField('Event',
                                 on_delete=models.DO_NOTHING,
                                 db_column='eventId',
                                 verbose_name='Etkinlik ID',
                                primary_key=True)
    active = models.BooleanField(verbose_name='Aktif')

    class Meta:
        managed = False
        db_table = 'user-event'
        unique_together = (('user_id', 'event_id'),)
