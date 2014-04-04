# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MyUser.first_name'
        db.add_column(u'tweetify_app_myuser', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 4, 3, 0, 0), max_length=30),
                      keep_default=False)

        # Adding field 'MyUser.last_name'
        db.add_column(u'tweetify_app_myuser', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2014, 4, 3, 0, 0), max_length=30),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MyUser.first_name'
        db.delete_column(u'tweetify_app_myuser', 'first_name')

        # Deleting field 'MyUser.last_name'
        db.delete_column(u'tweetify_app_myuser', 'last_name')


    models = {
        u'tweetify_app.myuser': {
            'Meta': {'object_name': 'MyUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'tweetify_app.tweet': {
            'Meta': {'object_name': 'Tweet'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tweetify_app.MyUser']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tweet_text': ('django.db.models.fields.CharField', [], {'max_length': '140'})
        }
    }

    complete_apps = ['tweetify_app']