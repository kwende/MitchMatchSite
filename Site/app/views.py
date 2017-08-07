"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

from app.models import Record

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)

    item = Record.objects.filter(id = 112275)[0]

    return render(
        request,
        'app/index.html',
        {
            'title':item.FirstName,
            'year':datetime.now().year,
        }
    )
