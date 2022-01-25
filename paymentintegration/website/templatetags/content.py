from django import template
from ..models import Content, ContentView

register = template.Library()

@register.simple_tag
def get_content_view(content, user):
    return ContentView.objects.filter(content=content,user=user,view=True).exists()