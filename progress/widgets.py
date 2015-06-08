from django.forms import DateInput

class CustomDateInput(DateInput):
    input_type = 'date'
