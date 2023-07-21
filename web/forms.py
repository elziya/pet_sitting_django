from django import forms
from django.contrib.auth import get_user_model

from django.utils import timezone

from web.models import Pet, Post

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    repeated_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['repeated_password']:
            self.add_error('password', 'Пароли не совпадают')
        return cleaned_data

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'repeated_password')


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class PetForm(forms.ModelForm):
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = Pet
        fields = ('name', 'description', 'image')


class PostForm(forms.ModelForm):
    def save(self, commit=True):
        if self.instance.id is None:
            self.instance.post_date = timezone.now()
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = Post
        fields = ('title', 'start_date', 'end_date', 'content', 'price', 'pets', 'opened')
        widgets = {
            "start_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format='%Y-%m-%dT%H:%M'
            ),
            "end_date": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format='%Y-%m-%dT%H:%M'
            )
        }


class PostFilterForm(forms.Form):
    search = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Поиск"}), required=False)
    opened = forms.NullBooleanField(label="Актуальный")
    start_date = forms.DateTimeField(
        label="От",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format='%Y-%m-%dT%H:%M'
        ),
        required=False
    )
    end_date = forms.DateTimeField(
        label="до",
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}, format='%Y-%m-%dT%H:%M'
        ),
        required=False
    )
