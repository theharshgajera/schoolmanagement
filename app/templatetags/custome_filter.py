# D:\College-Mgmt\app\templatetags\custom_filters.py

from django import template

register = template.Library()

@register.filter
def filter_student(results, student_id):
    return results.filter(student_id__id=student_id).first() or None

@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key))