from django import forms
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    email_or_username = forms.CharField(
        widget = forms.TextInput(attrs={
            'dir' : 'auto',
            'autocomplete' : 'username',
            'class' : 'form-input',
            'placeholder' : _('نام کاربری یا ایمیل خود را وارد کنید')
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'dir' : 'auto',
            'placeholder' : _('رمز عبور را وارد کنید'),
            'class' : 'form-input',
            'autocomplete' : 'current-password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class' : 'form-input'
        })
    )

class RegisterForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control', 'autocomplete': 'curent-password', 'placeholder': 'Curent Password'
    }), required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'fullname', 'username']
        widgets = {
            'email' : forms.EmailInput(attrs={
                'class' : 'form-control', 'autocomplete' : 'email', 'placeholder' : 'Email'
            }),
            'password' : forms.PasswordInput(attrs={
                'class' : 'form-control', 'autocomplete' : 'password', 'placeholder' : 'Password'
            }),
            'fullname' : forms.TextInput(attrs={
                'class' : 'form-control', 'required': 'True', 'autocomplete' : 'fullname', 'placeholder' : 'Fullname'
            }),
            'username' : forms.TextInput(attrs={
                'class' : 'form-control', 'autocomplete' : 'username', 'placeholder' : 'Username'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('این ایمیل قبلا ثبت شده است'))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_('نام کاربری قبلا ثبت شده است'))
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError(_('رمز عبور باید حداقل ۸ کاراکتر باشد'))
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError(_('پسورد ها یکسان نیستند'))
        return password2

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if username == email:
            raise forms.ValidationError(_('نام کاربری و ایمیل نمی‌تواند یکسان باشد'))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
