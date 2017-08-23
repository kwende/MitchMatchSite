"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from random import randint
from app.softmatching.algorithms import easiestAgreementCount

from app.models import Record, Set, SetMember
from django.db.models import Count
from django.core.cache import cache

from app.displaymodels import ColoredRecord

import random

allRecords = None

def findAlternatives(request):
    global allRecords
    enterpriseId = request.GET["id"]
    allIds = [int(a) for a in request.GET["all"].split(',')]

    baseRecord = Record.objects.get(EnterpriseId = enterpriseId)

    if allRecords is None:
        allRecords = Record.objects.filter(EnterpriseId__gte = 15374761)

    alternatives = []

    for comparisonRecord in allRecords:
        if not comparisonRecord.EnterpriseId in allIds:
            count = easiestAgreementCount(baseRecord, comparisonRecord)
            if count >= 2:
                alternatives.append(comparisonRecord)

    return render(request, 'app/alternatives.html',
                  {
                      'count' : len(alternatives),
                      'alternatives' : alternatives
                  })

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

        coloredRecords = []
        for setMember in setMembers:
            coloredRecord = ColoredRecord()

            coloredRecord.id = setMember.id
            coloredRecord.EnterpriseId = setMember.RecordId.EnterpriseId
            coloredRecord.LastName = setMember.RecordId.LastName
            coloredRecord.FirstName = setMember.RecordId.FirstName
            coloredRecord.MiddleName = setMember.RecordId.MiddleName
            coloredRecord.Suffix = setMember.RecordId.Suffix
            coloredRecord.DOB = setMember.RecordId.DOB
            coloredRecord.Gender = setMember.RecordId.Gender
            coloredRecord.SSN = setMember.RecordId.SSN
            coloredRecord.Address1 = setMember.RecordId.Address1
            coloredRecord.Address2 = setMember.RecordId.Address2
            coloredRecord.Zip = setMember.RecordId.Zip
            coloredRecord.MothersMaidenName = setMember.RecordId.MothersMaidenName
            coloredRecord.MRN = setMember.RecordId.MRN
            coloredRecord.City = setMember.RecordId.City
            coloredRecord.State = setMember.RecordId.State
            coloredRecord.Phone = setMember.RecordId.Phone
            coloredRecord.Phone2 = setMember.RecordId.Phone2
            coloredRecord.Email = setMember.RecordId.Email
            coloredRecord.Alias = setMember.RecordId.Alias

            coloredRecords.append(coloredRecord)
        
        r = lambda: random.randint(0,255)
        for a in range(0, len(coloredRecords)):
            for b in range(a+1, len(coloredRecords)):

                if coloredRecords[a].LastName == coloredRecords[b].LastName:
                    color = '#%02X%02X%02X' % (r(),r(),r())
                    coloredRecords[a].LastNameColor = color
                    coloredRecords[b].LastNameColor = color

        enterpriseIdsForSet = ",".join([str(s.RecordId.EnterpriseId) for s in setMembers])
        
        return render(request,
            'app/index.html',
            {
                'setId':set.id,
                'coloredRecords':coloredRecords,
                'numberLeft' : len(ids),
                'enterpriseIds' : enterpriseIdsForSet,
            })
