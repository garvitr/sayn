from django import forms
from django.contrib.auth.models import Group
from django.forms import DateField, EmailInput, PasswordInput, Select, TextInput, BooleanField
from progress.models import CustomUser, Society, Task
from progress.widgets import CustomDateInput

class RegistrationForm(forms.ModelForm):
    date_of_birth = DateField(input_formats=['%d %B, %Y'], widget=CustomDateInput(attrs={'class': 'datepicker'}, format='%d %B, %Y'))
    nominated_on = DateField(input_formats=['%d %B, %Y'], widget=CustomDateInput(attrs={'class': 'datepicker'}, format='%d %B, %Y'))
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

    class Meta:
        model = CustomUser
        exclude = ['is_active']
        widgets = {
            'first_name': TextInput(attrs={'class': 'validate', 'required': True}),
            'last_name': TextInput(attrs={'class': 'validate', 'required': True}),
            'position': TextInput(attrs={'class': 'validate', 'required': True}),
            'gender': Select(attrs={'class': 'validate', 'required': True}),
            'email': EmailInput(attrs={'class': 'validate', 'required': True}),
            'role': Select(attrs={'class': 'validate', 'required': True}),
            'contact_number': TextInput(attrs={'class': 'validate', 'pattern': '\+?1?\d{9,15}$', 'required': True}),
            'nominated_through': TextInput(attrs={'class': 'validate', 'required': True}),
            'password': PasswordInput(attrs={'class': 'validate', 'required': True}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'position': 'Position in NS',
            'gender': 'Gender',
            'email': 'Email',
            'date_of_birth': 'Date of Birth',
            'role': 'Role',
            'contact_number': 'Contact Number',
            'nominated_on': 'Nominated On',
            'nominated_through': 'Nominated Through',
            'society': 'Society',
        }

    def save(self, commit=True):
        instance = forms.ModelForm.save(self, False)
        old_save_m2m = self.save_m2m

        def save_m2m():
            old_save_m2m()
            instance.groups.clear()
            instance.groups.add(self.cleaned_data['group'])

        self.save_m2m = save_m2m

        if commit:
            instance.save()
            self.save_m2m()

        return instance


class UserEditForm(RegistrationForm):
    class Meta:
        model = CustomUser
        exclude = ['is_active', 'password']

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            try:
                initial['group'] = kwargs['instance'].groups.get()
            except:
                pass
        super(UserEditForm, self).__init__(*args, **kwargs)

class SocietyForm(forms.ModelForm):
    class Meta:
        model = Society
        exclude = []

        labels = {
            'contact_firstname': 'Contact Firstname',
            'contact_lastname': 'Contact Lastname',
            'contact_position': 'Contact Position',
            'contact_email': 'Contact Email'
        }

class TaskForm(forms.ModelForm):
    assigned_on = DateField(input_formats=['%d %B, %Y'], widget=CustomDateInput(attrs={'class': 'datepicker'}, format='%d %B, %Y'))
    completed_on = DateField(input_formats=['%d %B, %Y'], widget=CustomDateInput(attrs={'class': 'datepicker'}, format='%d %B, %Y'), required=False)

    class Meta:
        model = Task
        exclude = ['user', 'approved']

        labels = {
            'name':'Task name',
            'description':'Task description',
            'assigned_on': 'Task Assigned On',
            'completed_on': 'Task Completed On',
            'status': 'Task Status',
            'approved':'Approve Task'
        }