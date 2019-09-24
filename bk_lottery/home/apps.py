# -*- coding: utf-8 -*-

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def app_ready_handler(sender, **kwargs):
    print 'add admin'
    from django.contrib.auth.models import User
    try:
        if not User.objects.filter(username='admin').exists():
            new_user = User.objects.create(username='admin', is_superuser=True, is_staff=True)
            new_user.set_password("admin")
            new_user.save()
    except Exception as e:
        print 'add admin %s' % e


class HomeConfig(AppConfig):
    name = 'home'

    def ready(self):
        post_migrate.connect(app_ready_handler, sender=self)
