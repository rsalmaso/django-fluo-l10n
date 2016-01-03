# -*- coding: utf-8 -*-

# Copyright (C) 2007-2016, Raffaele Salmaso <raffaele@salmaso.org>
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

from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Country'
        db.create_table(u'l10n_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('fluo.db.models.fields.StatusField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('printable_name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('iso2_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2, db_index=True)),
            ('iso3_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('numcode', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('continent', self.gf('django.db.models.fields.CharField')(max_length=13)),
            ('admin_area', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=20, null=True, blank=True)),
        ))
        db.send_create_signal(u'l10n', ['Country'])

        # Adding model 'CountryTranslation'
        db.create_table(u'l10n_countrytranslation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['l10n.Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('printable_name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
        ))
        db.send_create_signal(u'l10n', ['CountryTranslation'])

        # Adding unique constraint on 'CountryTranslation', fields ['language', 'country']
        db.create_unique(u'l10n_countrytranslation', ['language', 'country_id'])

        # Adding model 'AdministrativeArea'
        db.create_table(u'l10n_administrativearea', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('fluo.db.models.fields.StatusField')()),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(related_name='administrative_areas', to=orm['l10n.Country'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60, db_index=True)),
            ('abbrev', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
        ))
        db.send_create_signal(u'l10n', ['AdministrativeArea'])


    def backwards(self, orm):
        # Removing unique constraint on 'CountryTranslation', fields ['language', 'country']
        db.delete_unique(u'l10n_countrytranslation', ['language', 'country_id'])

        # Deleting model 'Country'
        db.delete_table(u'l10n_country')

        # Deleting model 'CountryTranslation'
        db.delete_table(u'l10n_countrytranslation')

        # Deleting model 'AdministrativeArea'
        db.delete_table(u'l10n_administrativearea')


    models = {
        u'l10n.administrativearea': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AdministrativeArea'},
            'abbrev': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'administrative_areas'", 'to': u"orm['l10n.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'db_index': 'True'}),
            'status': ('fluo.db.models.fields.StatusField', [], {})
        },
        u'l10n.country': {
            'Meta': {'ordering': "('iso2_code', 'name')", 'object_name': 'Country'},
            'admin_area': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso2_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2', 'db_index': 'True'}),
            'iso3_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'numcode': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'status': ('fluo.db.models.fields.StatusField', [], {})
        },
        u'l10n.countrytranslation': {
            'Meta': {'unique_together': "(('language', 'country'),)", 'object_name': 'CountryTranslation'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': u"orm['l10n.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'})
        }
    }

    complete_apps = ['l10n']
