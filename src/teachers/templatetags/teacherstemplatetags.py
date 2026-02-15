from django import template
from subjects.models import SubjectProfile

register = template.Library()

@register.filter
def count_teachers(class_p):

    sbj = SubjectProfile.objects.all()
    print(sbj)
    return 5
    
