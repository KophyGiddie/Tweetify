# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'tweetify_app_userprofile')

        # Removing M2M table for field follows on 'UserProfile'
        db.delete_table(db.shorten_name(u'tweetify_app_userprofile_follows'))

        # Adding M2M table for field follows on 'MyUser'
        m2m_table_name = db.shorten_name(u'tweetify_app_myuser_follows')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_myuser', models.ForeignKey(orm[u'tweetify_app.myuser'], null=False)),
            ('to_myuser', models.ForeignKey(orm[u'tweetify_app.myuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_myuser_id', 'to_myuser_id'])


    def backwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'tweetify_app_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['tweetify_app.MyUser'], unique=True)),
        ))
        db.send_create_signal(u'tweetify_app', ['UserProfile'])

        # Adding M2M table for field follows on 'UserProfile'
        m2m_table_name = db.shorten_name(u'tweetify_app_userprofile_follows')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_userprofile', models.ForeignKey(orm[u'tweetify_app.userprofile'], null=False)),
            ('to_userprofile', models.ForeignKey(orm[u'tweetify_app.userprofile'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_userprofile_id', 'to_userprofile_id'])

        # Removing M2M table for field follows on 'MyUser'
        db.delete_table(db.shorten_name(u'tweetify_app_myuser_follows'))


    models = {
        u'tweetify_app.myuser': {
            'Meta': {'object_name': 'MyUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'follows': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followed_by'", 'symmetrical': 'False', 'to': u"orm['tweetify_app.MyUser']"}),
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