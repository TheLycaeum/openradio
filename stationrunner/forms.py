import os
from django import forms
from django.forms import Form
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from stationrunner.models import Station, AudioFile, Channel

class UserCreateForm(UserCreationForm):
    """
    Extends Django's UserCreationForm
    """
    email_exists_message = "A user with that email id already exists."
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try: 
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.email_exists_message,
            code='duplicate_email',
        )

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user
        
class StationForm(ModelForm):
    class Meta:
        model = Station
        fields = ['name', 'address']

class AddMemberForm(Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(),
                                  empty_label='Choose a User',
    )

class RemoveMemberForm(Form):
    member = forms.ModelChoiceField(queryset=User.objects.all(),
                                  empty_label='Choose a Member',
    )

## To Alen, channel related forms here
class ChannelForm(Form):
     # class Meta:
     #    model = Channel
     #    fields = ['name', 'frequency']
    name = forms.CharField()
    frequency = forms.CharField(widget=forms.Textarea)
    station = forms.ModelChoiceField(queryset=Station.objects.all())

########################################

class AudioFileForm(forms.ModelForm):
    class Meta:
        model = AudioFile
        fields = ['name', 'audio_file']

    def clean_audio_file(self):
        audio = self.cleaned_data['audio_file']
        if audio:
            if audio._size > 5*1024*1024:
                raise ValidationError("File too large ( > 5mb )")
            if os.path.splitext(audio.name)[1] != ".mp3":
                raise ValidationError("We only support mp3!")
            return audio
        else:
            raise validationError("Couldn't read uploaded file")
