import csv
from app.models import Record, Set, SetMember, RecordFuzzyMatch

def ImportAlternativeMatches(txtFile):

    with open(txtFile) as input:
        allLines = input.readlines()

        print("Reading all records...")
        allRecords = list(Record.objects.all())
        print("...done")

        matchedRecords = []
        num = 0
        for line in allLines:

            print("processing line " + str(num) + " of " + str(len(allLines)))
            num = num + 1

            enterpriseIds = line.split(',')

            numAppended = 0
            if len(enterpriseIds) > 1:
                toMatchId = int(enterpriseIds[0])
                fuzzyMatchedIds = [int(a) for a in enterpriseIds[1:]]
                print("\tGoing to add " + str(len(fuzzyMatchedIds)) + " fuzzy matches.")

                toMactch = None
                for record in allRecords:
                    if record.EnterpriseId == toMatchId:
                        toMatch = record
                        break

                for fuzzyMatchedId in fuzzyMatchedIds:
                    matched = None

                    for record in allRecords:
                        if record.EnterpriseId == fuzzyMatchedId:
                            fuzzyMatchRecord = RecordFuzzyMatch(ToMatch = toMatch, FuzzyMatched = record)
                            matchedRecords.append(fuzzyMatchRecord)
                            numAppended = numAppended + 1
                            break

            print("\tadded " + str(numAppended) + " fuzzy matches")

        RecordFuzzyMatch.objects.bulk_create(matchedRecords)

def ImportSets(txtFile, versionNumber):

    with open(txtFile) as input:
        lines = input.readlines()

        num = 0
        for line in lines:
            print(str(num / len(lines)) + "%")
            num = num + 1

            set = Set(VersionNumber = versionNumber, Checked = False, Notes = "")
            set.save()
            setId = set.id

            recordIds = [int(s.strip()) for s in line.split(',')]

            for recordId in recordIds:
                record = Record.objects.filter(EnterpriseId = recordId)[0]
                setMember = SetMember(RecordId = record, SetId = set, IsGood = True)
                setMember.save()

    return

def ImportAllRecords(csvFile):

    num = 0
    with open(csvFile) as csvTextFile:
        csvReader = csv.reader(csvTextFile)

        for line in csvReader:
            print(line[0])

            if num > 0:
                record = Record(EnterpriseId = int(line[0]),
                    LastName = line[1],
                    FirstName = line[2],
                    MiddleName = line[3],
                    Suffix = line[4],
                    DOB = line[5],
                    Gender = line[6],
                    SSN = line[7],
                    Address1 = line[8],
                    Address2 = line[9],
                    Zip = line[10],
                    MothersMaidenName = line[11],
                    MRN = line[12],
                    City = line[13],
                    State = line[14],
                    Phone = line[15],
                    Phone2 = line[16],
                    Email = line[17],
                    Alias = line[18])
                record.save()
            
            num = num + 1
    return