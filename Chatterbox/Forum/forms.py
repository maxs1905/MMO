from django import forms
from .models import Ads, Response, Category
from ckeditor_uploader.widgets import CKEditorUploadingWidget
class AdForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label='Категория',
        empty_label="Выберите категорию",
        to_field_name= 'name',
        widget=forms.Select(attrs={'class':'form-control'}))

    content = forms.CharField(
        label='Содержание объявления',
        widget=CKEditorUploadingWidget(config_name='default'),
        help_text='Здесь вы можете добавить текст, изображения, видео и другой контент'
    )

    class Meta:
        model = Ads
        fields = ['title', 'content', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class':'form-control'})
        }
        labels = {
            'title': 'Заголовок',
            'content': 'Содержание',
        }

    def clean(self):
        cleaned_data = super().clean()
        print("Form cleaned data:", cleaned_data)  # Отладочный вывод
        if not cleaned_data.get('title'):
            raise forms.ValidationError("Заголовок обязателен")
        if not cleaned_data.get('content'):
            raise forms.ValidationError("Содержание обязательно")
        return cleaned_data

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