from django.forms import ModelForm
from django import forms
from bfunweb.models import UserProfile, Adventure, Image, ProfileImage
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label='Username')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput(render_value=False))

# Note that a ModelForm includes a save()
class RegistrationForm(ModelForm):
  username = forms.CharField(max_length=30, label='Username')
  password = forms.CharField(max_length=20,
                             widget=forms.PasswordInput(render_value=False))
  first_name =  forms.CharField( max_length=30) 
  email = forms.EmailField()
  
  def save(self):
    new_user = User.objects.create_user(username=self.cleaned_data['username'],
                                        password=self.cleaned_data['password'],
                                        email=self.cleaned_data['email'])
    new_user.first_name=self.cleaned_data['first_name']
    new_user.save()

    return new_user
    
  class Meta:
    model = UserProfile
    exclude  = ('user',)
    
  #Django's form system automatically looks for any method whose name
  #starts with clean_ and ends in the name of a form on the field,
  #then calls it after the field's built-in validation rules have
  #been applied
  '''def clean_username(self):
    try:
      #The attribute clean_data is a dictionary
      #of any submitted data that's made it through
      #validation so far
      User.objects.get(username=self.cleaned_data['username'])
    except User.DoesNotExist:
      return self.cleaned_data['username']
    raise forms.ValidationError("This username is already in use")
  '''
  #def clean(self):
  # if 'password1' is self.cleaned_data and 'password2' is self.cleaned_data:
  #   raise forms.ValidationError("You must type the same password each time")
  # return self.cleaned_data
  
# This is a simplified version of the edit form
# since a facebook user for example does not
# have to edit stuff here

class EditSocialUserForm(ModelForm):
    
  class Meta:
    model = UserProfile
    fields = ('tags',)

class EditProfilePictureUserForm(ModelForm):
    
  class Meta:
    model = UserProfile
    fields = ('picture',)

class EditUserForm(ModelForm):
  # user object fields
  username = forms.CharField(max_length=30, label='Username')
  password = forms.CharField(max_length=20, 
                             widget=forms.PasswordInput(render_value=False))
  first_name =  forms.CharField( max_length=30) 
  email = forms.EmailField()
  
  #user profile object fields
  tags = forms.CharField(max_length=200,
                         help_text="Comma separated",
                         required=False)
  
  class Meta:
    model = UserProfile
    exclude  = ('user',)
    


class AdventureForm (ModelForm):

  name = forms.CharField(max_length=60, help_text="Eg. SF Throlley")
  cost = forms.DecimalField(max_digits=6, decimal_places=2,)
  tips = forms.CharField(max_length=250,
                         required=False,
                         widget=forms.Textarea())
  location_formatted_address = forms.CharField(max_length=60,)
  location_lat = forms.DecimalField(max_digits=100,)
  location_lon = forms.DecimalField(max_digits=100,)
    
  class Meta:
    model = Adventure 
    exclude  = ('user', 'currency_type','location_lat', 'location_lon',)
      

class ImageForm(ModelForm):
      class Meta:
          model = Image
      def __init__(self, user, *args, **kwargs):
          super(ImageForm, self).__init__(*args, **kwargs)
          self._user = user
          
          
          
class ProfileImageForm(ModelForm):
      class Meta:
          model = ProfileImage
      def __init__(self, user, *args, **kwargs):
          super(ProfileImageForm, self).__init__(*args, **kwargs)
          self._user = user


