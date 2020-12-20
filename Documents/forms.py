from django.forms import ModelForm, Select, Textarea, TextInput, DateInput, FileInput
from .models import *


class CreateDocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'body', 'end_date', 'purposes']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'body': Textarea(attrs={'class': 'form-control'}),
            'end_date': DateInput(attrs={'class': 'form-control', 'type': 'date', 'required': ''}),
            'purposes': Select(attrs={'class': 'form-control'}),
        }


class CreateStatementForm(ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'body']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'value': 'Заявление',  'readonly': ''}),
            'body': Textarea(attrs={'class': 'form-control'}),
        }


class CreateReportForm(ModelForm):
    class Meta:
        model = Document
        fields = ['name', 'body']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'value': 'Рапорт',  'readonly': ''}),
            'body': Textarea(attrs={'class': 'form-control'}),
        }
