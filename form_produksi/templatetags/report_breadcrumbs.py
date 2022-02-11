from django.contrib.admin.templatetags.admin_list import register
from django.contrib.admin.templatetags.base import InclusionAdminNode
from django.utils.translation import gettext_lazy as _
from django.utils.text import capfirst
from django.utils import formats
from django.db import models
from django.contrib.admin.utils import get_fields_from_path

import datetime

def date_hierarchy(cl):
    """
    Display the date hierarchy for date drill-down functionality.
    """
    if cl.date_hierarchy:
        field_name = cl.date_hierarchy
        field = get_fields_from_path(cl.model, field_name)[-1]
        if isinstance(field, models.DateTimeField):
            dates_or_datetimes = 'datetimes'
            qs_kwargs = {'is_dst': True}
        else:
            dates_or_datetimes = 'dates'
            qs_kwargs = {}
        year_field = '%s__year' % field_name
        month_field = '%s__month' % field_name
        day_field = '%s__day' % field_name
        field_generic = '%s__' % field_name
        year_lookup = cl.params.get(year_field)
        month_lookup = cl.params.get(month_field)
        day_lookup = cl.params.get(day_field)

        def link(filters):
            return cl.get_query_string(filters, [field_generic])

        if not (year_lookup or month_lookup or day_lookup):
            # select appropriate start level
            date_range = cl.queryset.aggregate(first=models.Min(field_name),
                                               last=models.Max(field_name))
            if date_range['first'] and date_range['last']:
                '''
                if dates_or_datetimes == 'datetimes':
                    date_range = {
                        k: timezone.localtime(v) if timezone.is_aware(v) else v
                        for k, v in date_range.items()
                    }'''
                if date_range['first'].year == date_range['last'].year:
                    year_lookup = date_range['first'].year
                    if date_range['first'].month == date_range['last'].month:
                        month_lookup = date_range['first'].month

        if year_lookup and month_lookup and day_lookup:
            day = datetime.date(int(year_lookup), int(month_lookup), int(day_lookup))
            return {
                'show': True,
                'back': {
                    'link': link({year_field: year_lookup, month_field: month_lookup}),
                    'title': capfirst(formats.date_format(day, 'YEAR_MONTH_FORMAT'))
                },
                'choices': [{'title': capfirst(formats.date_format(day, 'MONTH_DAY_FORMAT'))}]
            }
        elif year_lookup and month_lookup:
            months = getattr(cl.queryset, dates_or_datetimes)(field_name, 'month', **qs_kwargs)
            return {
                'show': True,
                'back': {
                    'link': link({year_field: year_lookup}),
                    'title': str(year_lookup)
                },
                'choices': [{
                    'link': link({year_field: year_lookup, month_field: month.month}),
                    'title': capfirst(formats.date_format(month, 'YEAR_MONTH_FORMAT'))
                } for month in months]
            }
        elif year_lookup:
            months = getattr(cl.queryset, dates_or_datetimes)(field_name, 'month', **qs_kwargs)
            return {
                'show': True,
                'back': {
                    'link': link({}),
                    'title': _('All dates')
                },
                'choices': [{
                    'link': link({year_field: year_lookup, month_field: month.month}),
                    'title': capfirst(formats.date_format(month, 'YEAR_MONTH_FORMAT'))
                } for month in months]
            }
        else:
            years = getattr(cl.queryset, dates_or_datetimes)(field_name, 'year', **qs_kwargs)
            return {
                'show': True,
                'back': None,
                'choices': [{
                    'link': link({year_field: str(year.year)}),
                    'title': str(year.year),
                } for year in years]
            }

@register.tag(name='date_hierarchy')
def date_hierarchy_tag(parser, token):
    return InclusionAdminNode(
        parser, token,
        func=date_hierarchy,
        template_name='date_hierarchy.html',
        takes_context=False,
    )