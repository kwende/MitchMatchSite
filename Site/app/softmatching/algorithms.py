from Site.settings import BAD_SSNs
import re
from datetime import datetime

def kDifferences(sm, sn, k):
    matches = False

    if len(sm) == len(sn):

        nd = 0
        for i in range(len(sn)):
            if sm[i] != sn[i]:
                nd = nd + 1

        matches = nd <= k

    return matches

def isSSNValid(a):
    return a != "0" and a not in BAD_SSNs

def fuzzySSNMatch(ssnA, ssnB):
    return isSSNValid(ssnA) and isSSNValid(ssnB) and kDifferences(ssnA, ssnB, 1)

def fuzzyAddressMatch(address1, address2):

    if address1 == "" or address2 == "":
        return False
    if address1 == address2:
        return True

    numberParts1 = re.findall("\d+",address1)
    numberParts2 = re.findall("\d+",address2)

    if len(numberParts1) != len(numberParts2):
        return False

    if len(numberParts1) == 0:
        return False

    for i in range(0, len(numberParts1)):
        if numberParts1[i] != numberParts2[i]:
            return False

    return True

def dateOneOrOneDigit(part1, part2):

    part1Int = int(part1)
    part2Int = int(part2)

    if abs(part1Int - part2Int) < 2:
        return True
    else:
        return kDifferences(part1, part2, 1)

def transposedDigit(a, b):

    if len(a) != len(b):
        return False
    else:

        possibleTransposition = True
        transpositionDetected = False

        i = 0
        while i < len(a):
            if a[i] != b[i]:
                if not transpositionDetected and (i + 1 < len(a) and a[i] == b[i + 1] and b[i] == a[i + 1]):
                    transpositionDetected = True
                    i = i + 1
                else:
                    possibleTransposition = False
            i = i + 1

        return transpositionDetected and possibleTransposition

def dateTimeOffBy100(a, b):

    if a != "" and b != "":
        intA = int(a)
        intB = int(b)

        return intA == intB - 100 or intB == intA - 100
    else:
        return False


def fuzzyDateEquals(date1String, date2String):

    if date1String == "" or date2String == "":
        return False

    date1Bits = date1String.split('/')
    date2Bits = date2String.split('/')

    dayIndex = 0
    monthIndex = 1
    yearIndex = 2

    day1 = date1Bits[dayIndex]
    day2 = date2Bits[dayIndex]

    month1 = date1Bits[monthIndex]
    month2 = date2Bits[monthIndex]

    year1 = date1Bits[yearIndex]
    year2 = date2Bits[yearIndex]

    if dateOneOrOneDigit(month1, month2) and day1 == day2 and year1 == year2:
        return True

    if month1 == month2 and dateOneOrOneDigit(day1, day2) and year1 == year2:
        return True

    if month1 == month2 and day1 == day2 and (dateOneOrOneDigit(year1, year2) or transposedDigit(year1, year2) \
        or dateTimeOffBy100(year1, year2)):
        return True

    if month1 == day2 and day1 == month2 and year1 == year2:  #Transpose day an month
        return True

    return

def fuzzyLastName(lastName1, lastName2):
    return kDifferences(lastName1, lastName2, 2)

def fuzzyFirstName(firstName1, firstName2):
    return kDifferences(firstName1, firstName2, 2)

def easiestAgreementCount(row1, row2):
    fieldAgreement = 0

    if fuzzyLastName(row1.LastName, row2.LastName):
        fieldAgreement = fieldAgreement + 1

    if fuzzyFirstName(row1.FirstName, row2.FirstName):
        fieldAgreement = fieldAgreement + 1

    if fuzzySSNMatch(row1.SSN, row2.SSN):
        fieldAgreement = fieldAgreement + 1

    if fuzzyAddressMatch(row1.Address1, row2.Address1):
        fieldAgreement = fieldAgreement + 1

    if fuzzyDateEquals(row1.DOB, row2.DOB):
        fieldAgreement = fieldAgreement + 1

    return fieldAgreement



