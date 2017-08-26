"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest, HttpResponseRedirect
from django.template import RequestContext
from datetime import datetime
from random import randint
from app.softmatching.algorithms import easiestAgreementCount

from app.models import Record, Set, SetMember, RecordFuzzyMatch
from django.db.models import Count
from django.core.cache import cache

from app.displaymodels import ColoredRecord
from app.softmatching.coloring import buildColoredRecords, recordToColoredRecordType, setAlternativeColors

import random

allRecords = None
whichId = 0

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

def findSoftMatches(enterpriseId):
    global allRecords

    softMatches = []

    rootRecord = Record.objects.get(EnterpriseId = enterpriseId)

    matchedIds = list(RecordFuzzyMatch.objects.filter(ToMatch_id = rootRecord.id).values_list('FuzzyMatched_id', flat = True))
    softMatches = list([recordToColoredRecordType(a) for a in Record.objects.filter(id__in = matchedIds)])

    return {
        'EnterpriseId' : enterpriseId,
        'SoftMatches' : softMatches
        }

def showPassed(request):

    allCheckedSetIds = Set.objects.filter(Checked = True).values_list('id', flat = True)

    setOfSets = []

    for checkedSetId in allCheckedSetIds:
        set = list(SetMember.objects.filter(SetId__id = checkedSetId))
        setOfSets.append(set)
        
    return render(request, 
                  'app/passed.html',
                  {
                      'passedSets':setOfSets
                  })

def home(request):
    global whichId

    if request.method == "POST": #This is what we do if the button has been pressed
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
        assert isinstance(request, HttpRequest) #This is what we do if we have come into the top level site
    
        ids = Set.objects.filter(Checked = False).values_list('id', flat=True)

        randomIndex = randint(0, len(ids) - 1)
        setId = Set.objects.get(pk = ids[randomIndex]).id
        
        setMembers = SetMember.objects.filter(SetId__id = setId)

        enterpriseIdsForSet = ",".join([str(s.RecordId.EnterpriseId) for s in setMembers])

        softMatches = []
        for setMember in setMembers:
            softMatchesForEnterpriseId = findSoftMatches(setMember.RecordId.EnterpriseId)
            setAlternativeColors(setMember.RecordId, softMatchesForEnterpriseId["SoftMatches"])
            softMatches.append(softMatchesForEnterpriseId)

        return render(request,
            'app/index.html',
            {
                'setId':setId,
                'coloredRecords':buildColoredRecords(setMembers),
                'numberLeft' : len(ids),
                'enterpriseIds' : enterpriseIdsForSet,
                'softMatches' : softMatches
            })
