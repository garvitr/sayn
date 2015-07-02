import django_filters
from django_filters import DateRangeFilter
from progress.models import CustomUser, News, Task
from progress.widgets import CustomDateInput

class CustomUserFilter(django_filters.FilterSet):
    class Meta:
        model = CustomUser
        fields = [
            'society',
            'role',
            'is_active',
        ]

class TaskFilter(django_filters.FilterSet):
    assigned_on = DateRangeFilter()
    completed_on = DateRangeFilter()

    class Meta:
        model = Task
        fields = [
            'assigned_on',
            'completed_on',
            'status',
            'approved',
        ]

class TaskAdminFilter(TaskFilter):
    class Meta:
        model = Task
        fields = [
            'assigned_on',
            'completed_on',
            'status',
            'approved',
            'user',
        ]

class NewsFilter(django_filters.FilterSet):
    created_on = DateRangeFilter()

    class Meta:
        model = News
        fields = [
            'created_on',
        ]