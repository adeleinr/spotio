from django.db import models
from django import forms
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from sorl.thumbnail.fields import ImageWithThumbnailsField
import os

class UserProfileLookupTables:
    OCCUPATION_CHOICES = (
        (0, 'Tech Industry'),
        (1, 'Student'),
        (2, 'My own business'),
        (3, 'At home'),
        (3, 'At home'),
    )
    
    GENDER_CHOICES = (
        (0, 'Male'),
        (1, 'Female'),
    )
    
    SELF_DESC_CHOICES = (
        (0, 'Techie'),
        (1, 'College Life'),
        (2, 'Artsie'),
        (3, 'Nerd'),
        (4, 'Normal Human Being'),
         (5, 'Professional Traveler'),
        (6, 'Mystic'),
        (7, 'Health Sapient'),
        (8, 'Unknown'),
    )
    
    ETHNICITY_CHOICES = (
        (0, 'Hispanic'),
        (1, 'Asian'),
        (2, 'African American'),
        (3, 'Caucasian'),
    )
    

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, editable=False)
    home_zipcode = models.CharField(max_length=5, blank=True)
    picture_url = models.URLField(max_length=200, blank=True)
    picture_thumbnail = models.URLField(max_length=200, blank=True)
    tags = TaggableManager()    

    def get_home_zipcode(self):
        return self.home_zipcode
      
    #def get_pictures(self, num_pictures):
    #    return self.pictures.all().order_by('-id')[num_pictures]
    
    def get_pictures(self, num_pictures):
        return self.pictures.all().order_by('-id')[:num_pictures]
    
    def __unicode__(self):
        return self.user.username

    def get_absolute_url(self):
        return "/colorific/user_detail/%s" % (self.user.username)
      
    def get_absolute_public_url(self):
        return "/colorific/people/%s" % (self.user.username)
    
    def absolute_url(self):
        return "/colorific/user_detail/%s" % (self.user.username)
      
    def absolute_public_url(self):
        return "/colorific/people/%s" % (self.user.username)


    
'''
   This class is used only for a profile (avatar) image
   If not a Social User (Ie. Facebook user) the
   ProfileImage class will upload the image in different
   sizes, so we use the large thumbnail format which is 200x200 pixels
   If a a Social User then his/her picture will
   be pulled from facebook and will be equivalent to this
   200x200 pixels picture               
'''
class ProfileImage(models.Model):
    def get_image_path(instance, filename):
      print "create path"
      val="uploads/images/avatars/" + str(instance.user.id)+"_"+filename
      print val
      return val 
    user = models.ForeignKey(UserProfile, editable=False, related_name='profile_picture')
    #picture = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    picture = ImageWithThumbnailsField(upload_to='uploads/images/avatars/',
                                       null=True, blank=True,
                                       thumbnail={'size': (50, 50), 'options': ('crop',)},
                                       extra_thumbnails={
                                       'medium': {'size': (100, 100),
                                                  'options': ['crop', 'upscale']},
                                                  'large': {'size': (200, 400)},
                                       },)


class Adventure(models.Model):
    name = models.CharField(max_length=60, help_text="Eg. Golden Gate Park Museum")
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    currency_type = models.CharField(max_length=60, default=("USD"), editable=False,)
    user = models.ForeignKey(UserProfile)
    pub_date = models.DateTimeField(auto_now_add=True)
    tips = models.TextField(blank=True, max_length=250,)
    location_formatted_address = models.CharField(max_length=60,)
    location_lat = models.DecimalField(max_digits=30,decimal_places=10)
    location_lon = models.DecimalField(max_digits=30,decimal_places=15)
    
    class Meta:
        get_latest_by = 'pub_date'
        
    def __unicode__(self):
        return self.name + " " +str(self.cost)

    def get_absolute_url(self):
        return "/bfunweb/adventures/%s" % (self.id)

    def get_picture(self, num_pictures):
        return self.pictures.all().order_by('-id')[:num_pictures][0]

    def get_pictures(self, num_pictures):
        return self.pictures.all().order_by('-id')[:num_pictures]
        
'''
  This class is used for all pictures associated with
  a user, except the profile picture
'''
class Image(models.Model):
    def get_image_path(instance, filename):
      print "create path"
      val="uploads/images/adventures/" + str(instance.user.id)+"_"+filename
      print val
      return val 
    adventure = models.ForeignKey(Adventure, editable=False, related_name='pictures')
    #picture = models.ImageField(upload_to=get_image_path, null=True, blank=True)
    picture = ImageWithThumbnailsField(upload_to='uploads/images/adventures/',
                                       null=True, blank=True,
                                       thumbnail={'size': (80, 80),
                                                  'options': ('crop',)},
                                       extra_thumbnails={
                                          'medium': {'size': (200, 110),
                                          'options': ['crop', 'upscale']},
                                          'large': {'size': (300, 300)},
                                       },)

    def __unicode__(self):
        return self.picture.extra_thumbnails['medium']
   
