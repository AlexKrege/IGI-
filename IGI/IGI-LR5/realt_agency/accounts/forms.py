from django import forms
from .models import User
from datetime import date

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'birth_date']

    def clean_birth_date(self):
        bd = self.cleaned_data.get('birth_date')
        if bd:
            today = date.today()
            if bd > today:
                raise forms.ValidationError('Дата рождения не может быть в будущем.')
            age = (today - bd).days // 365
            if age < 18:
                raise forms.ValidationError('Вы должны быть старше 18 лет.')
        return bd

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return phone

    def clean_password2(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Пароли не совпадают')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user