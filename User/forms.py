from django.forms import ModelForm, FileInput, TextInput, Textarea, Select, DateInput, EmailInput, NumberInput
from .models import Profile


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['last_name', 'first_name', 'sur_name', 'position', 'body', 'date_of_birth', 'paul',
                  'tel_number', 'itn', 'image']
        widgets = {
            'last_name': TextInput(attrs={'class': 'form-control input-shadow', 'placeholder': 'Фамилия'}),
            'first_name': TextInput(attrs={'class': 'form-control input-shadow', 'placeholder': 'Имя'}),
            'sur_name': TextInput(attrs={'class': 'form-control input-shadow', 'placeholder': 'Отчество'}),
            'position': Select(attrs={'class': 'form-control input-shadow', 'placeholder': 'Должность'}),
            'body': Textarea(attrs={'class': 'form-control input-shadow', 'placeholder': 'О себе'}),
            'date_of_birth': DateInput(attrs={'type': 'date', 'class': 'form-control input-shadow', 'placeholder': 'День рождения'}),
            'paul': Select(attrs={'class': 'form-control input-shadow', 'placeholder': 'Пол'}),
            'tel_number': TextInput(attrs={'class': 'form-control input-shadow', 'placeholder': 'Номер телефона'}),
            'itn': NumberInput(attrs={'class': 'form-control input-shadow', 'placeholder': 'Идентификационный номер налогоплательщика (сокращенно ИНН)'}),
            'image': FileInput(attrs={'class': 'form-control'})
        }

