from django import forms
from django.contrib.auth.models import Group
from django.forms import DateField, EmailInput, PasswordInput, Select, TextInput, BooleanField, FileInput
from progress.models import CustomUser, News, Society, Task
from progress.widgets import CustomDateInput
from django.contrib.auth.hashers import make_password


class RegistrationForm(forms.ModelForm):
    GROUPS = (
        (1, 'Administrator'),
        (2, 'SC'),
        (3, 'CC1'),
        (4, 'CC2'),
        (5, 'Other')
    )
    date_of_birth = DateField(input_formats=['%d %B, %Y'], widget=CustomDateInput(attrs={'class': 'datepicker'}, format='%d %B, %Y'))
    nominated_on = DateField(input_formats=['%d %B, %Y'], widget=CustomDateInput(attrs={'class': 'datepicker'}, format='%d %B, %Y'))
    group = forms.ChoiceField(choices=GROUPS, required=True)

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

    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin', False)
        super(RegistrationForm, self).__init__(*args, **kwargs)

        if admin == False:
            self.fields['group'].choices = self.GROUPS[1:]
        else:
            self.fields['group'].choices = self.GROUPS

    def save(self, commit=True):
        instance = super(RegistrationForm, self).save(commit=False)

        def save_m2m():
            instance.groups.clear()
            instance.groups.add(self.cleaned_data['group'])

        self.save_m2m = save_m2m

        if commit:
            instance.password = make_password(self.cleaned_data['password'])
            instance.save()
            self.save_m2m()

        return instance


class UserEditForm(RegistrationForm):
    class Meta:
        model = CustomUser
        exclude = ['password']
        widgets = {
            'avatar': FileInput()
        }

    def __init__(self, *args, **kwargs):
        if 'instance' in kwargs:
            initial = kwargs.setdefault('initial', {})
            try:
                initial['group'] = kwargs['instance'].groups.get().id
            except:
                pass
        admin = kwargs.pop('admin', False)
        super(UserEditForm, self).__init__(*args, **kwargs)

        if admin == False:
            self.fields['group'].choices = self.GROUPS[1:]
        else:
            self.fields['group'].choices = self.GROUPS

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
        exclude = ['user']

        labels = {
            'name':'Task name',
            'description':'Task description',
            'assigned_on': 'Task Assigned On',
            'completed_on': 'Task Completed On',
            'status': 'Task Status',
            'approved':'Approve Task'
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.status == 2:
            self.fields['completed_on'].widget.attrs['disabled'] = True

    def clean_completed_on(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.status == 2:
            return instance.completed_on
        return self.cleaned_data['completed_on']

    def clean(self):
        cleaned_data = super(TaskForm, self).clean()
        instance = getattr(self, 'instance', None)

        if instance and instance.status == 2 and cleaned_data['status'] != 2:
            cleaned_data['completed_on'] = None

        if cleaned_data['status'] == 2 and cleaned_data['completed_on'] is None:
            self.add_error('completed_on', 'Task Status set as completed but Completed On date not mentioned')

        if cleaned_data['status'] != 2 and cleaned_data['completed_on'] is not None:
            self.add_error('completed_on', 'Task Status not set as completed but Completed On date is set')

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        exclude = ['user', 'created_on']