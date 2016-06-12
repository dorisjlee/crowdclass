from __future__ import unicode_literals

import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.contrib.auth.models import User



@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class PrePostTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index = True)

    pre_scheme = models.CharField(max_length=200, default = "empty")
    pre_elliptical = models.CharField(max_length=200, default = "empty")
    pre_mergers = models.CharField(max_length=200, default = "empty")
    pre_tidal = models.CharField(max_length=200, default = "empty")
    pre_lens = models.CharField(max_length=200, default = "empty")
    pre_dust = models.CharField(max_length=200, default = "empty")
    pre_properties = models.CharField(max_length=200, default = "empty")
    pre_bulges = models.CharField(max_length=200, default = "empty")
    pre_not = models.CharField(max_length=200, default = "empty")
    pre_formation = models.CharField(max_length=200, default = "empty")

    pre_scheme_time = models.DateTimeField(blank=True,null=True)
    pre_elliptical_time = models.DateTimeField(blank=True,null=True)
    pre_mergers_time = models.DateTimeField(blank=True,null=True)
    pre_tidal_time = models.DateTimeField(blank=True,null=True)
    pre_lens_time = models.DateTimeField(blank=True,null=True)
    pre_dust_time = models.DateTimeField(blank=True,null=True)
    pre_properties_time = models.DateTimeField(blank=True,null=True)
    pre_bulges_time = models.DateTimeField(blank=True,null=True)
    pre_not_time = models.DateTimeField(blank=True,null=True)
    pre_formation_time = models.DateTimeField(blank=True,null=True)

    pre_count = models.IntegerField(default = 0)

    post_scheme = models.CharField(max_length=200, default = "empty")
    post_elliptical = models.CharField(max_length=200, default = "empty")
    post_mergers = models.CharField(max_length=200, default = "empty")
    post_tidal = models.CharField(max_length=200, default = "empty")
    post_lens = models.CharField(max_length=200, default = "empty")
    post_dust = models.CharField(max_length=200, default = "empty")
    post_properties = models.CharField(max_length=200, default = "empty")
    post_bulges = models.CharField(max_length=200, default = "empty")
    post_not = models.CharField(max_length=200, default = "empty")
    post_formation = models.CharField(max_length=200, default = "empty")

    post_count = models.IntegerField(default = 0)

    post_scheme_time = models.DateTimeField(blank=True,null=True)
    post_elliptical_time = models.DateTimeField(blank=True,null=True)
    post_mergers_time = models.DateTimeField(blank=True,null=True)
    post_tidal_time = models.DateTimeField(blank=True,null=True)
    post_lens_time = models.DateTimeField(blank=True,null=True)
    post_dust_time = models.DateTimeField(blank=True,null=True)
    post_properties_time = models.DateTimeField(blank=True,null=True)
    post_bulges_time = models.DateTimeField(blank=True,null=True)
    post_not_time = models.DateTimeField(blank=True,null=True)
    post_formation_time = models.DateTimeField(blank=True,null=True)
    
    end_time = models.DateTimeField(blank=True,null=True) 

# Participant oversees all UserSessions for a user.
# Keeps track of total score, difficulty, and the number of UserSessions created.
# Also keeps track of if the user has previously seen the question
class Participant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index = True)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    score = models.IntegerField(default=0)
    # Easy:0, Medium:1, Hard:2
    level = models.IntegerField(default=0)
    count = models.IntegerField(default=0)


    elliptical_count = models.IntegerField(default=0)
    spiral_count = models.IntegerField(default=0)
    edge_count = models.IntegerField(default=0)
    bulge_count = models.IntegerField(default=0)
    bar_count = models.IntegerField(default=0)
    merging_count = models.IntegerField(default=0)
    dust_count = models.IntegerField(default=0)
    lens_count = models.IntegerField(default=0)
    tidal_count = models.IntegerField(default=0)

    introduction_count = models.IntegerField(default=0)
    

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index = True)
    pub_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    image = models.IntegerField(blank=True, null=True)

    difficulty = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    introduction_description_time = models.DateTimeField(blank=True,null=True)

    # elliptical 
    elliptical_choice = models.CharField(max_length=200, blank=True)
    elliptical_question_id = models.IntegerField(blank=True, null=True)
    elliptical_time = models.DateTimeField(blank=True,null=True)
    elliptical_example = models.BooleanField(default=False)
    elliptical_description_time = models.DateTimeField(blank=True,null=True)
    elliptical_hint = models.BooleanField(default=False)
    elliptical_correct = models.IntegerField(default=0)
    # bulge 
    bulge_choice = models.CharField(max_length=200, blank=True)
    bulge_question_id = models.IntegerField(blank=True, null=True)
    bulge_time = models.DateTimeField(blank=True,null=True)
    bulge_example = models.BooleanField(default=False)
    bulge_description_time = models.DateTimeField(blank=True,null=True)
    bulge_hint = models.BooleanField(default=False)
    bulge_correct = models.IntegerField(default=0)
    # edge 
    edge_choice = models.CharField(max_length=200, blank=True)
    edge_question_id = models.IntegerField(blank=True, null=True)
    edge_time = models.DateTimeField(blank=True,null=True)
    edge_example = models.BooleanField(default=False)
    edge_description_time = models.DateTimeField(blank=True,null=True)
    edge_hint = models.BooleanField(default=False)
    edge_correct = models.IntegerField(default=0)
    # bar 
    bar_choice = models.CharField(max_length=200, blank=True)
    bar_question_id = models.IntegerField(blank=True, null=True)
    bar_time = models.DateTimeField(blank=True,null=True)
    bar_example = models.BooleanField(default=False)
    bar_description_time = models.DateTimeField(blank=True,null=True)
    bar_hint = models.BooleanField(default=False)
    bar_correct = models.IntegerField(default=0)
    # spiral 
    spiral_choice = models.CharField(max_length=200, blank=True)
    spiral_question_id = models.IntegerField(blank=True, null=True)
    spiral_time = models.DateTimeField(blank=True,null=True)
    spiral_example = models.BooleanField(default=False)
    spiral_description_time = models.DateTimeField(blank=True,null=True)
    spiral_hint = models.BooleanField(default=False)
    spiral_correct = models.IntegerField(default=0)
    # tidal 
    tidal_choice = models.CharField(max_length=200, blank=True)
    tidal_question_id = models.IntegerField(blank=True, null=True)
    tidal_time = models.DateTimeField(blank=True,null=True)
    tidal_example = models.BooleanField(default=False)
    tidal_description_time = models.DateTimeField(blank=True,null=True)
    tidal_hint = models.BooleanField(default=False)
    tidal_correct = models.IntegerField(default=0)
    # merging 
    merging_choice = models.CharField(max_length=200, blank=True)
    merging_question_id = models.IntegerField(blank=True, null=True)
    merging_time = models.DateTimeField(blank=True,null=True)
    merging_example = models.BooleanField(default=False)
    merging_description_time = models.DateTimeField(blank=True,null=True)
    merging_hint = models.BooleanField(default=False)
    merging_correct = models.IntegerField(default=0)
    # dust 
    dust_choice = models.CharField(max_length=200, blank=True)
    dust_question_id = models.IntegerField(blank=True, null=True)
    dust_time = models.DateTimeField(blank=True,null=True)
    dust_example = models.BooleanField(default=False)
    dust_description_time = models.DateTimeField(blank=True,null=True)
    dust_hint = models.BooleanField(default=False)
    dust_correct = models.IntegerField(default=0)
    # lens 
    lens_choice = models.CharField(max_length=200, blank=True)
    lens_question_id = models.IntegerField(blank=True, null=True)
    lens_time = models.DateTimeField(blank=True,null=True)
    lens_example = models.BooleanField(default=False)
    lens_description_time = models.DateTimeField(blank=True,null=True)
    lens_hint = models.BooleanField(default=False)
    lens_correct = models.IntegerField(default=0)
    restart = models.DateTimeField(blank=True, null=True)
    restart_count = models.IntegerField(default=0)

    end_time = models.DateTimeField(blank=True,null=True)

# Easy:0, Medium:1, Hard:2
# Decription page only shows up in the level denoted by difficulty
# All the class below holds the description text.

class Introduction(models.Model):
    heading = models.CharField(max_length=10000, null=True)
    description_text_1 = models.CharField(max_length=10000)
    description_text_2 = models.CharField(max_length=10000,null=True)
    description_text_3 = models.CharField(max_length=10000,null=True)
    difficulty = models.IntegerField(blank=True,null=True)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class EllipticalDescription(models.Model):
    description_text = models.CharField(max_length=5000)
    difficulty = 0
    score = models.IntegerField(default=0)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class SpiralDescription(models.Model):
    description_text = models.CharField(max_length=5000)
    difficulty = 0
    score = models.IntegerField(default=4)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class EdgeDescription(models.Model):
    description_text = models.CharField(max_length=5000)
    difficulty = 0
    score = models.IntegerField(default=2)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class BarDescription(models.Model):
    description_text = models.CharField(max_length=5000)
    difficulty = 0
    score = models.IntegerField(default=4)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class BulgeDescription(models.Model):
    description_text = models.CharField(max_length=5000)
    difficulty = 2
    score = models.IntegerField(default=2)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class MergingDescription(models.Model):
    description_text = models.CharField(max_length=5000)
    difficulty = 1
    score = models.IntegerField(default=4)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class TidalDescription(models.Model):
    description_text = models.CharField(max_length=5000)
    difficulty = 1
    score = models.IntegerField(default=4)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class DustDescription(models.Model):
    description_text = models.CharField(max_length=5000)
    difficulty = 2
    score = models.IntegerField(default=2)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class LensDescription(models.Model):
    description_text = models.CharField(max_length=5000)
    difficulty = 2
    score = models.IntegerField(default=2)
    image = models.IntegerField(blank=True, null=True)
    caption = models.CharField(max_length=500,blank=True)

class Elliptical(models.Model):
    question_text = models.CharField(max_length=500)
    hint = models.CharField(max_length=500,blank=True)
    difficulty = models.IntegerField(default=0)
    answer = models.BooleanField()
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Spiral(models.Model):
    question_text = models.CharField(max_length=500)
    hint = models.CharField(max_length=500,blank=True)
    difficulty = models.IntegerField(default=0)
    answer = models.BooleanField()
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Edge(models.Model):
    question_text = models.CharField(max_length=500)
    hint = models.CharField(max_length=500,blank=True)
    difficulty = models.IntegerField(default=0)
    answer = models.BooleanField()
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Bulge(models.Model):
    question_text = models.CharField(max_length=500)
    hint = models.CharField(max_length=500,blank=True)
    difficulty = models.IntegerField(default=0)
    answer = models.BooleanField()
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Bar(models.Model):
    question_text = models.CharField(max_length=500)
    hint = models.CharField(max_length=500,blank=True)
    difficulty = models.IntegerField(default=0)
    answer = models.BooleanField()
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Merging(models.Model):
    question_text = models.CharField(max_length=500)
    hint = models.CharField(max_length=500,blank=True)
    difficulty = models.IntegerField(default=0)
    answer = models.BooleanField()
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Dust(models.Model):
    question_text = models.CharField(max_length=500)
    hint = models.CharField(max_length=500,blank=True)
    difficulty = models.IntegerField(default=0)
    answer = models.BooleanField()
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Lens(models.Model):
    question_text = models.CharField(max_length=500)
    hint = models.CharField(max_length=500,blank=True)
    difficulty = models.IntegerField(default=0)
    answer = models.BooleanField()
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Tidal(models.Model):
    question_text = models.CharField(max_length=500)
    hint = models.CharField(max_length=500,blank=True)
    difficulty = models.IntegerField(default=0)
    answer = models.BooleanField()
    pub_date = models.DateTimeField('date published',blank=True,null=True)
    def __str__(self):
        return self.question_text
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.question_text

