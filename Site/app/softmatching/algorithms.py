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

    if address1 == "" or address1 == "":
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

        for i in range(0, len(a)):
            if a[i] != b[i]:
                if not transpositionDetected and (i + 1 < len(a) and a[i] == b[i + 1] and b[i] == a[i + 1]):
                    transpositionDetected = True
                    i = i + 1
                else:
                    possibleTransposition = True

        return transpositionDetected and possibleTransposition

def dateTimeOffBy100(a, b):

    intA = int(a)
    intB = int(b)

    return a == b - 100 or b == a - 100


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

    if dateOneOrOneDigit(month1, month2) and day1 == day2 and year1 == year1:
        return True

    if month1 == month2 and dateOneOrOneDigit(day1, day2):
        return True

    if month1 == month2 and day1 == day2 and (dateOneOrOneDigit(year1, year2) or transposedDigit(year1, year2) \
        or dateTimeOffBy100(year1, year2)):
        return True

    if month1 == day2 and day1 == month2 and year1 == year2:
        return True

    return

def easiestAgreementCount(row1, row2):
    fieldAgreement = 0

    if kDifferences(row1.LastName, row2.LastName, 2):
        fieldAgreement = fieldAgreement + 1

    if kDifferences(row1.FirstName, row2.LastName, 2):
        fieldAgreement = fieldAgreement + 1

    if fuzzySSNMatch(row1.SSN, row2.SSN):
        fieldAgreement = fieldAgreement + 1

    if fuzzyAddressMatch(row1.Address1, row2.Address2):
        fieldAgreement = fieldAgreement + 1

    if fuzzyDateEquals(row1.DOB, row2.DOB):
        fieldAgreement = fieldAgreement + 1

    return fieldAgreement