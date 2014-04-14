
# -*- coding: UTF-8 -*-

from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Patient(models.Model):
    cpf_id = models.CharField(max_length=15, primary_key=True)
    name_txt = models.CharField(max_length=50)
    nr_record = models.AutoField(primary_key=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name_txt


class PaymentOption(models.Model):
    payment_txt = models.CharField(max_length=50)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.payment_txt


class GenderOption(models.Model):
    gender_txt = models.CharField(max_length=50)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.gender_txt


class FleshToneOption(models.Model):
    flesh_tone_txt = models.CharField(max_length=50)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.flesh_tone_txt


class MaritalStatusOption(models.Model):
    marital_status_txt = models.CharField(max_length=50)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.marital_status_txt


class ReligionOption(models.Model):
    religion_txt = models.CharField(max_length=50)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.religion_txt


class SchoolingOption(models.Model):
    schooling_txt = models.CharField(max_length=50)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.schooling_txt


class PersonalData(models.Model):
    id_patient = models.OneToOneField(Patient)
    dt_birth_txt = models.DateField()
    # city_birth_txt = models.CharField(max_length=50)
    benefit_gov_bool = models.BooleanField()
    payment_opt = models.OneToOneField(PaymentOption)
    gender_opt = models.OneToOneField(GenderOption)
    flesh_tone_opt = models.OneToOneField(FleshToneOption)
    profession_txt = models.CharField(null=True, blank=True, max_length=50)
    occupation_txt = models.CharField(max_length=50)
    marital_status_opt = models.OneToOneField(MaritalStatusOption)
    religion_opt = models.OneToOneField(ReligionOption)
    schooling_opt = models.OneToOneField(SchoolingOption)
    years_studying_int = models.IntegerField()

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.id_patient, self.dt_birth_txt, self.city_birth_txt, self.benefit_gov_bool, self.flesh_tone_opt, self.gender_opt, self.marital_status_opt, self.occupation_txt, self.payment_opt, self.profession_txt, self.religion_opt, self.schooling_opt, self.years_studying_int
