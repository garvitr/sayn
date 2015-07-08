from django.forms import DateInput, ClearableFileInput, CheckboxInput
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe

class CustomDateInput(DateInput):
    input_type = 'date'

class AvatarInput(ClearableFileInput):
    '''renders the input file as an avatar image, and removes the 'currently' html'''

    template_with_initial = u'%(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'

    def render(self, name, value, attrs=None):
        substitutions = {
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(AvatarInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = ('<img src="%s" width="60" height="60"></img>'
                                        % (escape(value.url)))

            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)