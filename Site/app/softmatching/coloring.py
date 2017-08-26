from app.displaymodels import ColoredRecord
from app.models import Record, Set, SetMember
import app.softmatching.algorithms 
import random

def setAlternativeColors(mainRecord, comparisonRecords):

    #    setFuzzyColors("LastName", coloredRecords, app.softmatching.algorithms.fuzzyLastName)
    #setFuzzyColors("FirstName", coloredRecords, app.softmatching.algorithms.fuzzyFirstName)
    #setFuzzyColors("DOB", coloredRecords, app.softmatching.algorithms.fuzzyDateEquals)
    #setFuzzyColors("Address1", coloredRecords, app.softmatching.algorithms.fuzzyAddressMatch)
    #setFuzzyColors("SSN", coloredRecords, app.softmatching.algorithms.fuzzySSNMatch)

    for comparisonRecord in comparisonRecords:

        if mainRecord.LastName == comparisonRecord.LastName:
            comparisonRecord.LastNameColor = "#FF0000"
        elif app.softmatching.algorithms.fuzzyLastName(mainRecord.LastName, comparisonRecord.LastName):
            comparisonRecord.LastNameColor = "#00FF00"

        if mainRecord.FirstName == comparisonRecord.FirstName:
            comparisonRecord.LastNameColor = "#FF0000"
        elif app.softmatching.algorithms.fuzzyFirstName(mainRecord.FirstName, comparisonRecord.FirstName):
            comparisonRecord.FirstNameColor = "#00FF00"

        if mainRecord.DOB == comparisonRecord.DOB:
            comparisonRecord.LastNameColor = "#FF0000"
        elif app.softmatching.algorithms.fuzzyDateEquals(mainRecord.DOB, comparisonRecord.DOB):
            comparisonRecord.DOBColor = "#00FF00"

        if mainRecord.Address1 == comparisonRecord.Address1:
            comparisonRecord.LastNameColor = "#FF0000"
        elif app.softmatching.algorithms.fuzzyAddressMatch(mainRecord.Address1, comparisonRecord.Address1):
            comparisonRecord.Address1Color = "#00FF00"

        if mainRecord.SSN == comparisonRecord.SSN:
            comparisonRecord.LastNameColor = "#FF0000"
        elif app.softmatching.algorithms.fuzzySSNMatch(mainRecord.SSN, comparisonRecord.SSN):
            comparisonRecord.SSNColor = "#00FF00"

    return

def setFuzzyColors(attributeName, coloredRecords, fuzzyFunction):
    attributeColorName = attributeName + "Color"

    for a in range(0, len(coloredRecords)):
        if getattr(coloredRecords[a],attributeColorName) == "":
            for b in range(a+1, len(coloredRecords)):
                if getattr(coloredRecords[b],attributeColorName) == "" and \
                    fuzzyFunction(getattr(coloredRecords[a],attributeName), getattr(coloredRecords[b],attributeName)):
                    setattr(coloredRecords[a], attributeColorName,"#00FF00")
                    setattr(coloredRecords[b], attributeColorName,"#00FF00")

def setColors(attributeName, coloredRecords):

    attributeColorName = attributeName + "Color"

    colorIndex = 0

    for a in range(0, len(coloredRecords)):
        # color identified for this guy yet?  
        if getattr(coloredRecords[a], attributeColorName) == "":

            # nope, so grab a color
            matchFound = False
            for b in range(a+1, len(coloredRecords)):
                if getattr(coloredRecords[a], attributeName) == getattr(coloredRecords[b], attributeName) and getattr(coloredRecords[b], attributeColorName) == "":
                    setattr(coloredRecords[a],attributeColorName, "#FF0000")
                    setattr(coloredRecords[b],attributeColorName, "#FF0000")
                    matchFound = True

            if matchFound:
                colorIndex = colorIndex + 1

def recordToColoredRecordType(record):
    coloredRecord = ColoredRecord()

    #coloredRecord.id = setMember.id
    coloredRecord.EnterpriseId = record.EnterpriseId
    coloredRecord.LastName = record.LastName
    coloredRecord.FirstName = record.FirstName
    coloredRecord.MiddleName = record.MiddleName
    coloredRecord.Suffix = record.Suffix
    coloredRecord.DOB = record.DOB
    coloredRecord.Gender = record.Gender
    coloredRecord.SSN = record.SSN
    coloredRecord.Address1 = record.Address1
    coloredRecord.Address2 = record.Address2
    coloredRecord.Zip = record.Zip
    coloredRecord.MothersMaidenName = record.MothersMaidenName
    coloredRecord.MRN = record.MRN
    coloredRecord.City = record.City
    coloredRecord.State = record.State
    coloredRecord.Phone = record.Phone
    coloredRecord.Phone2 = record.Phone2
    coloredRecord.Email = record.Email
    coloredRecord.Alias = record.Alias

    return coloredRecord; 

def buildColoredRecords(setMembers):

    coloredRecords = []
    for setMember in setMembers:

        coloredRecord = recordToColoredRecordType(setMember.RecordId)
        coloredRecord.id = setMember.id
        coloredRecords.append(coloredRecord)
        
    attributeNames = [a for a in dir(coloredRecords[0]) if not a.startswith("_") and not a.endswith("Color") and not a == "EnterpriseId" and not a == "id"]

    colorStrings = ["#FF0000", "#00FF00", "#0000FF"]

    # look for exact matches
    for attributeName in attributeNames:
        setColors(attributeName, coloredRecords)

    # look for soft matches
    setFuzzyColors("LastName", coloredRecords, app.softmatching.algorithms.fuzzyLastName)
    setFuzzyColors("FirstName", coloredRecords, app.softmatching.algorithms.fuzzyFirstName)
    setFuzzyColors("DOB", coloredRecords, app.softmatching.algorithms.fuzzyDateEquals)
    setFuzzyColors("Address1", coloredRecords, app.softmatching.algorithms.fuzzyAddressMatch)
    setFuzzyColors("SSN", coloredRecords, app.softmatching.algorithms.fuzzySSNMatch)

    return coloredRecords
