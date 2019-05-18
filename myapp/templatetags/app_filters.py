from django import template
from datetime import datetime, date, timedelta
from django.template.defaulttags import register
from ..models import profile

register = template.Library()
...
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def ttt():
	return profile.objects.get(User=currentuser).webmails

@register.filter(name='formattime')
def formattime(strtime):
	try:
		context = datetime.strptime(strtime, "%Y-%m-%d %H:%M:%S.%f")
	except:
		context = strtime
	return context


@register.filter(name='rempvep')
def rempvep(value):
	a = value.replace('<p>', '')
	return a.replace('</p>', '')