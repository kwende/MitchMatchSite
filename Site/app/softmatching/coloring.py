from app.displaymodels import ColoredRecord
from app.models import Record, Set, SetMember
import random

def setColors(colorStrings, attributeName, coloredRecords):

    attributeColorName = attributeName + "Color"

    colorIndex = 0

    for a in range(0, len(coloredRecords)):
        # color identified for this guy yet?  
        if getattr(coloredRecords[a], attributeColorName) == "":

            # nope, so grab a color
            colorString = colorStrings[colorIndex]
            matchFound = False
            for b in range(a+1, len(coloredRecords)):
                if getattr(coloredRecords[a], attributeName) == getattr(coloredRecords[b], attributeName) and getattr(coloredRecords[b], attributeColorName) == "":
                    setattr(coloredRecords[a],attributeColorName, colorString)
                    setattr(coloredRecords[b],attributeColorName, colorString)
                    matchFound = True

            if matchFound:
                colorIndex = colorIndex + 1

def buildColoredRecords(setMembers):

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
        
    

    attributeNames = [a for a in dir(coloredRecords[0]) if not a.startswith("_") and not a.endswith("Color") and not a == "EnterpriseId" and not a == "id"]

    #r/g/b should be good enough, though r and g should only ever be used (max is a four-tuple, i think)
    colorStrings = ["#FF0000", "#00FF00", "#0000FF"]

    for attributeName in attributeNames:
        setColors(colorStrings, attributeName, coloredRecords)


    return coloredRecords
