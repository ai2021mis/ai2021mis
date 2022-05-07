from django import forms
from . import models

class ProfileForm(forms.ModelForm):
	class Meta:
		model = models.employee
		fields = ['name', 'email', 'contact_num']
		widgets = {
			'name': forms.TextInput(attrs={'placeholder':'name','class':'form-control'}),
			'email': forms.TextInput(attrs={'class':'form-control'}),
			'contact_num': forms.TextInput(attrs={'class':'form-control'}),
			}
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['name'].label = '姓名'
		self.fields['email'].label = '郵箱地址'
		self.fields['contact_num'].label = '聯絡號碼'


class ProfileFormtemplate4(forms.ModelForm):
	class Meta:
		model = models.employee
		fields = ['name', 'email', 'contact_num', 'emergency_contact']
		widgets = {
			'name': forms.TextInput(attrs={'placeholder':'你的名字','class':'form-control'}),
			'email': forms.TextInput(attrs={'placeholder':'example@gmail.com','class':'form-control'}),
			'contact_num': forms.TextInput(attrs={'placeholder':'你的手機號碼','class':'form-control'}),
			'emergency_contact': forms.TextInput(attrs={'placeholder': '名字＠手機號碼', 'class': 'form-control'}),
			}
	def __init__(self, *args, **kwargs):
		super(ProfileFormtemplate4, self).__init__(*args, **kwargs)
		self.fields['name'].label = '姓名'
		self.fields['email'].label = '郵箱地址'
		self.fields['contact_num'].label = '聯絡號碼'
		self.fields['emergency_contact'].label = '緊急聯繫人'


# class ProfileForm(forms.Form):
# 	name = forms.CharField(label='姓名', required=True)
# 	email = forms.CharField(label='郵箱地址', required=True)
# 	contact_num = forms.CharField(label='聯絡號碼', required=True)
