from django.template import Library
from django.db.models import Count, Sum, F, Func, IntegerField
from django.db.models import OuterRef, Subquery

from form_produksi.models import KK

register = Library()

def totals_row(cl):
    total_functions = getattr(cl.model_admin, 'total_functions', {})
    totals = []
    ids = cl.result_list.values_list('id', flat = True)
    ids = list(ids)
    qs = cl.queryset.filter(id__in = ids)
    for idx, field_name in enumerate(cl.list_display):
        if idx == 1:
            totals.append('Summary')
        elif field_name in total_functions:
            formula = total_functions[field_name]
            expr = formula[0]
            format = formula[1]

            if len(formula) >= 3:
                qs = qs.values(formula[2])

            try:
                summary = qs.aggregate(agg = expr)
            except:
                summary = 0
            
            try:
                if format == '%':
                    summary = "{0:.2%} ".format(summary['agg'])
                elif format == 'f':
                    summary = '{:,.2f}'.format(summary['agg'])
                else:
                    summary = '{:,.2f}'.format(summary['agg'])
            except:
                summary = '-'
            totals.append(summary)
        else:
            totals.append('-')
    return {'cl': cl, 'totals_row': totals}
    
register.inclusion_tag("admin/cl_summary.html")(totals_row)