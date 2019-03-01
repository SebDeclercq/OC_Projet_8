from typing import Any, Dict, Optional, Sequence, Tuple, Type
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser


Fieldset = Tuple[Optional[str], Dict[str, Sequence[str]]]


class UserCreationForm(forms.ModelForm):
    '''A from for creating new Users'''
    password1: forms.CharField = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )
    password2: forms.CharField = forms.CharField(
        label='Password', widget=forms.PasswordInput
    )

    class Meta:
        model: Type[CustomUser] = CustomUser
        fields: Sequence[str] = ('email', 'name', 'firstname',)

    def clean_password2(self) -> Optional[str]:
        password1: Optional[str] = self.cleaned_data.get('password1')
        password2: Optional[str] = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password mismatch')
        return password2

    def save(self, commit: bool = True) -> Any:
        user: Any = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password: ReadOnlyPasswordHashField = ReadOnlyPasswordHashField()

    class Meta:
        model: Type[CustomUser] = CustomUser
        fields = ('email', 'password', 'name', 'firstname',
                  'is_active', 'is_admin')

    def clean_password(self) -> Optional[str]:
        return self.initial.get('password')


class UserAdmin(BaseUserAdmin):
    form: Type[UserChangeForm] = UserChangeForm
    add_form: Type[UserCreationForm] = UserCreationForm

    list_display: Sequence[str] = ('email', 'name', 'firstname', 'is_admin')
    list_filter: Sequence[str] = ('is_admin',)
    fieldsets: Tuple[Fieldset, Fieldset, Fieldset] = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'firstname')}),
        ('Permissions', {'fields': ('is_admin',)})
    )
    add_fieldsets: Tuple[Fieldset] = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'firstname', 'password1', 'password2')
        }),
    )
    search_fields: Sequence[str] = ('email', 'name')
    ordering: Sequence[str] = ('name', 'firstname')
    filter_horizontal: Sequence[str] = ()


admin.site.register(CustomUser, UserAdmin)
admin.site.unregister(Group)
