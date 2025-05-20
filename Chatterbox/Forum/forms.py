from django import forms
from .models import Ads, Response, Category

class AdForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required= False,
        label='Категория',
        empty_label="Выберите категорию",
        to_field_name= 'name',
        widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = Ads
        fields = ['title', 'description', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'})
        }
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'image': 'Изображение',
        }

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Напишите ваш отклик здесь...'
            })
        }
        labels = {
            'text': 'Текст отклика'
        }