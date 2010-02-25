
from south.db import db
from django.db import models
from edesia.core.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Tag'
        db.create_table('core_tag', (
            ('id', orm['core.Tag:id']),
            ('name', orm['core.Tag:name']),
        ))
        db.send_create_signal('core', ['Tag'])
        
        # Adding model 'Recipe'
        db.create_table('core_recipe', (
            ('id', orm['core.Recipe:id']),
            ('name', orm['core.Recipe:name']),
            ('ingredients', orm['core.Recipe:ingredients']),
            ('directions', orm['core.Recipe:directions']),
            ('primary_photo', orm['core.Recipe:primary_photo']),
            ('inserted', orm['core.Recipe:inserted']),
            ('servings', orm['core.Recipe:servings']),
            ('preparation_time', orm['core.Recipe:preparation_time']),
            ('inserted_by', orm['core.Recipe:inserted_by']),
            ('slug', orm['core.Recipe:slug']),
        ))
        db.send_create_signal('core', ['Recipe'])
        
        # Adding ManyToManyField 'Tag.recipes'
        db.create_table('core_tag_recipes', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm.Tag, null=False)),
            ('recipe', models.ForeignKey(orm.Recipe, null=False))
        ))
        
        # Adding ManyToManyField 'Recipe.tags'
        db.create_table('core_recipe_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('recipe', models.ForeignKey(orm.Recipe, null=False)),
            ('tag', models.ForeignKey(orm.Tag, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Tag'
        db.delete_table('core_tag')
        
        # Deleting model 'Recipe'
        db.delete_table('core_recipe')
        
        # Dropping ManyToManyField 'Tag.recipes'
        db.delete_table('core_tag_recipes')
        
        # Dropping ManyToManyField 'Recipe.tags'
        db.delete_table('core_recipe_tags')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'core.recipe': {
            'directions': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {}),
            'inserted': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'inserted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'preparation_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'primary_photo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'servings': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Tag']", 'blank': 'True'})
        },
        'core.tag': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'recipes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Recipe']", 'blank': 'True'})
        }
    }
    
    complete_apps = ['core']
