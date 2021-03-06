from __future__ import unicode_literals

import datetime
from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from autoslug import AutoSlugField

from nfn_user.models import C_Owner
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField('Name', max_length=30, blank=False, null=False)
	slug = AutoSlugField(populate_from='name', blank=False, null=False)
	description = models.CharField('Description', max_length=100)
	hex_code = models.CharField('Color Code', max_length=7, default="#212121")
	hex_code_2 = models.CharField('Second Color Code (For Gradients)', max_length=7, default="#212121")

	def __unicode__(self):
		return self.name

class Contest(models.Model):
	owner = models.ForeignKey(C_Owner, on_delete=models.CASCADE)
	title = models.CharField(max_length=60, blank=False, null=False)
	slug = AutoSlugField(populate_from='title', unique_with=['title', 'owner__company_name', 'date_started'])
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	description = models.CharField(max_length=100, blank=False, null=False)
	details = models.TextField()
	image = models.ImageField(upload_to='contests', default='deneme')
	award = models.CharField(max_length=60)
	date_started = models.DateField('Start Date', blank=False, null=False, default=datetime.date.today) 
	date_deadline = models.DateField('Deadline', blank=False, null=False, default=datetime.date.today)
	is_approved = models.BooleanField('Approved', default=True)

	def get_absolute_url(self):
		return reverse('contests:view_contest', kwargs={'slug': self.slug})

	def clean(self):
		if self.date_started > self.date_deadline:
			raise ValidationError('Start date cannot precede deadline, please check the dates!')

	@property
	def is_ongoing(self):
		if self.date_deadline > datetime.date.today():
			return "Ongoing"
		return "Finished"

	def __unicode__(self):
		return self.title


class Submission(models.Model):
	applicant = models.ForeignKey(User, on_delete=models.CASCADE)
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
	a_names = models.CharField('Applicant Name(s)', max_length=200)
	a_details = models.TextField('Applicant Details')
	s_details = models.TextField('Submission Details')
	s_file = models.FileField('Submission File', upload_to='submissions', null=True, blank=True)
	feedback = models.TextField('Contest Owner\'s Feedback', blank=True, null=True)
	date_posted = models.DateTimeField('Submission Date', auto_now_add=True)

	def get_absolute_url(self):
		return reverse('contests:view_submission', kwargs={'contest_slug': self.contest.slug, 'pk': self.pk})

	def __unicode__(self):
		return '%s' % (self.a_names)


class Winner(models.Model):
	contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
	winner = models.ForeignKey(Submission, on_delete=models.CASCADE)

	def get_absolute_url(self):
		return reverse('contests:view_contest', kwargs={'slug': self.contest.slug})

	def __unicode__(self):
		return 'Contest: %s, Winner: %s' % (self.contest, self.winner)