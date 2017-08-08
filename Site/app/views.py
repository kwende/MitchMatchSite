"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from random import randint

from app.models import Record, Set, SetMember

def home(request):

    if request.method == "POST":
        baddies = [request.POST[p] for p in request.POST if p.startswith("member_")]
        for baddy in baddies:
            item = SetMember.objects.get(pk = int(baddy))
            item.IsGood = False
            item.save()

        set = Set.objects.get(pk = int(request.POST["setId"]))
        set.Checked = True
        set.save()

        return HttpResponseRedirect("/")
    else:
        assert isinstance(request, HttpRequest)
    
        ids = Set.objects.filter(Checked = False).values_list('id', flat=True)
        randomIndex = randint(0, len(ids) - 1)

        set = Set.objects.get(pk = ids[randomIndex])
        setMembers = SetMember.objects.filter(SetId__id = set.id)

        return render(request,
            'app/index.html',
            {
                'setId':set.id,
                'setMembers':setMembers,
            })
