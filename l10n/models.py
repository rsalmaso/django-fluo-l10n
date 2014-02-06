# -*- coding: utf-8 -*-

# Copyright (C) 2007-2014, Raffaele Salmaso <raffaele@salmaso.org>
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

# Country and AdministrativeArea models and data are taken from satchmo
# (http://www.satchmoproject.com) released as
# Copyright (c) 2009, Satchmo Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the Satchmo Project  nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

from __future__ import absolute_import, division, print_function, unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from fluo.db import models

CONTINENTS = (
    ('africa', _('Africa')),
    ('north-america', _('North America')),
    ('europe',  _('Europe')),
    ('asia', _('Asia')),
    ('oceania',  _('Oceania')),
    ('south-america', _('South America')),
    ('antarctica', _('Antarctica'))
)

AREAS = (
    ('another', _('Another')),
    ('island', _('Island')),
    ('arrondissement', _('Arrondissement')),
    ('atoll', _('Atoll')),
    ('autonomous-island', _('Autonomous island')),
    ('canton', _('Canton')),
    ('commune', _('Commune')),
    ('country', _('County')),
    ('departement', _('Department')),
    ('dependency', _('Dependency')),
    ('district', _('District')),
    ('division', _('Division')),
    ('emirate', _('Emirate')),
    ('governorate', _('Governorate')),
    ('island-council', _('Island council')),
    ('island-group', _('Island group')),
    ('island-region', _('Island region')),
    ('kingdom', _('Kingdom')),
    ('municipality', _('Municipality')),
    ('parish', _('Parish')),
    ('prefecture', _('Prefecture')),
    ('province', _('Province')),
    ('region', _('Region')),
    ('republic', _('Republic')),
    ('sheading', _('Sheading')),
    ('state', _('State')),
    ('subdivision', _('Subdivision')),
    ('subject', _('Subject')),
    ('territory', _('Territory')),
)


@python_2_unicode_compatible
class Country(models.I18NModel):
    """
    International Organization for Standardization (ISO) 3166-1 Country list
    """
    status = models.StatusField(
        verbose_name=_('Country is active'),
    )
    name = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('Official name (CAPS)'),
    )
    printable_name = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('Country name'),
    )
    iso2_code = models.CharField(
        max_length=2,
        unique=True,
        db_index=True,
        verbose_name=_('ISO alpha-2'),
    )
    iso3_code = models.CharField(
        max_length=3,
        unique=True,
        verbose_name=_('ISO alpha-3'),
    )
    numcode = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_('ISO numeric'),
    )
    continent = models.CharField(
        choices=CONTINENTS,
        max_length=13,
        verbose_name=_('Continent'),
    )
    admin_area = models.CharField(
        choices=AREAS,
        max_length=20,
        blank=True,
        null=True,
        db_index=True,
        verbose_name=_('Administrative Area'),
    )

    class Meta:
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')
        ordering = ('iso2_code', 'name',)

    def __str__(self):
        return self.printable_name


@python_2_unicode_compatible
class CountryTranslation(models.TranslationModel):
    country = models.ForeignKey(
        Country,
        related_name='translations',
    )
    name = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('Official name (CAPS)'),
    )
    printable_name = models.CharField(
        max_length=128,
        db_index=True,
        verbose_name=_('Country name'),
    )

    class Meta:
        verbose_name = _('Country Name Translation')
        verbose_name_plural = _('Country Name Translations')
        unique_together = (('language', 'country',),)

    def __str__(self):
        return '%s %s' % (self.country.printable_name, self.printable_name,)


@python_2_unicode_compatible
class AdministrativeArea(models.Model):
    """
    Administrative Area level 1 for a country.
    For the US, this would be the states.
    """
    status = models.StatusField(
        verbose_name=_('Area is active'),
    )
    country = models.ForeignKey(
        Country,
        related_name='administrative_areas',
    )
    name = models.CharField(
        max_length=60,
        db_index=True,
        verbose_name=_('Admin Area name'),
    )
    abbrev = models.CharField(
        max_length=3,
        blank=True,
        null=True,
        verbose_name=_('Postal Abbreviation'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Administrative Area')
        verbose_name_plural = _('Administrative Areas')
        ordering = ('name',)
