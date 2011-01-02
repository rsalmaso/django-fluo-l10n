# -*- coding: utf-8 -*-

# Copyright (C) 2007-2011, Raffaele Salmaso <raffaele@salmaso.org>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from south.db import db
from fluo import models
from l10n.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'AdministrativeArea'
        db.create_table('l10n_administrativearea', (
            ('id', orm['l10n.AdministrativeArea:id']),
            ('status', orm['l10n.AdministrativeArea:status']),
            ('country', orm['l10n.AdministrativeArea:country']),
            ('name', orm['l10n.AdministrativeArea:name']),
            ('abbrev', orm['l10n.AdministrativeArea:abbrev']),
        ))
        db.send_create_signal('l10n', ['AdministrativeArea'])
        
        # Adding model 'CountryTranslation'
        db.create_table('l10n_countrytranslation', (
            ('id', orm['l10n.CountryTranslation:id']),
            ('language', orm['l10n.CountryTranslation:language']),
            ('country', orm['l10n.CountryTranslation:country']),
            ('name', orm['l10n.CountryTranslation:name']),
            ('printable_name', orm['l10n.CountryTranslation:printable_name']),
        ))
        db.send_create_signal('l10n', ['CountryTranslation'])
        
        # Adding model 'Country'
        db.create_table('l10n_country', (
            ('id', orm['l10n.Country:id']),
            ('status', orm['l10n.Country:status']),
            ('name', orm['l10n.Country:name']),
            ('printable_name', orm['l10n.Country:printable_name']),
            ('iso2_code', orm['l10n.Country:iso2_code']),
            ('iso3_code', orm['l10n.Country:iso3_code']),
            ('numcode', orm['l10n.Country:numcode']),
            ('continent', orm['l10n.Country:continent']),
            ('admin_area', orm['l10n.Country:admin_area']),
        ))
        db.send_create_signal('l10n', ['Country'])
        
        # Creating unique_together for [language, country] on CountryTranslation.
        db.create_unique('l10n_countrytranslation', ['language', 'country_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [language, country] on CountryTranslation.
        db.delete_unique('l10n_countrytranslation', ['language', 'country_id'])
        
        # Deleting model 'AdministrativeArea'
        db.delete_table('l10n_administrativearea')
        
        # Deleting model 'CountryTranslation'
        db.delete_table('l10n_countrytranslation')
        
        # Deleting model 'Country'
        db.delete_table('l10n_country')
        
    
    
    models = {
        'l10n.administrativearea': {
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'administrative_areas'", 'to': "orm['l10n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'db_index': 'True'}),
            'status': ('models.StatusField', [], {})
        },
        'l10n.country': {
            'admin_area': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'db_index': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'numcode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'status': ('models.StatusField', [], {})
        },
        'l10n.countrytranslation': {
            'Meta': {'unique_together': "(('language', 'country'),)"},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['l10n.Country']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        }
    }
    
    complete_apps = ['l10n']
