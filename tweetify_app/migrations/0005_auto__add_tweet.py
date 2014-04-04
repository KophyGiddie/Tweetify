# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tweet'
        db.create_table(u'tweetify_app_tweet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tweet_text', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tweetify_app.MyUser'])),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'tweetify_app', ['Tweet'])


    def backwards(self, orm):
        # Deleting model 'Tweet'
        db.delete_table(u'tweetify_app_tweet')


    models = {
        u'tweetify_app.myuser': {
            'Meta': {'object_name': 'MyUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
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