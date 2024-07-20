from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from users.models import *
from django.contrib import messages


class Userprofilform(UserChangeForm):
    
    class Meta:
        model = User
        fields = ('first_name','last_name','nomi','tg','tel','img')

    def __init__(self,*args,**kwargs):
        super(Userprofilform,self).__init__(*args,**kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class NewIshchiForm(forms.ModelForm):
    
    class Meta:
        model = Istemolchi
        fields = ('full_name', 'pazivnoy', 'tel',)
    
    def __init__(self, *args, **kwargs):
        super(NewIshchiForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class QarzForm(forms.ModelForm):
    
    class Meta:
        model = Qarz
        fields = ('summa',)
    
    def __init__(self, *args, **kwargs):
        super(QarzForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class TolovForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Tolov
        fields = ('naxt','karta','izox','date',)
    
    def __init__(self, *args, **kwargs):
        super(TolovForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            