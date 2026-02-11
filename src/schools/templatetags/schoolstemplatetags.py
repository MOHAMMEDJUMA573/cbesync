from django import template

register = template.Library()

@register.filter
def add_results(results_list):
    sum = 0
    for result in results_list:
        sum += int(result.result_score)
    return sum