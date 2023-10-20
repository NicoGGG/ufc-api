import django_filters
from .models import Fight
from django.db.models import Q


class FightFilter(django_filters.FilterSet):
    fighter = django_filters.CharFilter(label="Fighter", method="filter_by_fighter")

    class Meta:
        model = Fight
        fields = ["event_id", "weight_class", "fighter"]

    def filter_by_fighter(self, queryset, name, value):
        return queryset.filter(
            Q(fighter_one__first_name__icontains=value)
            | Q(fighter_one__last_name__icontains=value)
            | Q(fighter_one__nickname__icontains=value)
            | Q(fighter_two__first_name__icontains=value)
            | Q(fighter_two__last_name__icontains=value)
            | Q(fighter_two__nickname__icontains=value)
        )
