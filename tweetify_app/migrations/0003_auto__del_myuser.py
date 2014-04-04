# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'MyUser'
        db.delete_table(u'tweetify_app_myuser')


    def backwards(self, orm):
        # Adding model 'MyUser'
        db.create_table(u'tweetify_app_myuser', (
            ('joined', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'tweetify_app', ['MyUser'])


    models = {
        
    }

    complete_apps = ['tweetify_app']