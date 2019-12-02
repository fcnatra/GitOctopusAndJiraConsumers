import datetime
import numpy
import glob
import os

class Project: 
    id = ''
    name = ''
    versions = []

    def __init__( self, id, name ):
        self.id = id
        self.name = name
        self.versions = []

class Version:
    id = 0
    name = ''
    releaseDate = ''
    description = ''
    released = False
    releaseDate = ''
    dateFromReleaseDate = None
    
    def __init__(self, id, name, description, released, releaseDate = None):
        self.id, self.name, self.description, self.released, self.releaseDate = id, name, description, released, releaseDate
    
    def getDateFromReleaseDate( self ):
        if ( self.dateFromReleaseDate is not None ):
            return self.dateFromReleaseDate

        if ( self.released and self.releaseDate is not None ):
            if ( len( self.releaseDate ) == 10 ): self.releaseDate += 'T00:00:00'
            if ('.' in self.releaseDate): self.releaseDate = self.releaseDate[:str.find(self.releaseDate, '.')]
            self.dateFromReleaseDate = datetime.datetime.strptime( self.releaseDate, '%Y-%m-%dT%H:%M:%S' )

        return self.dateFromReleaseDate

def __getVersionDates( projects ):
    versionDates = {}
    row = 0
    for project in projects:
        for version in project.versions:
            if ( version.released and version.releaseDate is not None ):
                versionDate = version.getDateFromReleaseDate()
                if ( versionDate not in versionDates ):
                    versionDates[ versionDate ] = list( None for x in range(0, row) )
    
                versionDates[ versionDate ].append( version.name )
        row += 1
    return versionDates

def dumpToFile( projects, fileName ):
    print( 'CREATING DUMP CONTENT...' )

    versionDates = __getVersionDates( projects )
    
    sortedDates = sorted(versionDates)
    orderedVersionDates = {}
    for iterator in sortedDates:
        orderedVersionDates[iterator] = versionDates[iterator]

    firstDate = sortedDates[0]
    lastDate = sortedDates[-1]
    numberOfDates = lastDate - firstDate
    timeLapse = [lastDate - datetime.timedelta(days=x) for x in range(0, numberOfDates.days)]
    
    numOfProjects = len( projects )

    for time in timeLapse:
        if ( time not in versionDates ): versionDates[ time ] = list( None for x in range(0, numOfProjects) )
    
    sortedDates = sorted(versionDates)
    rows = ['FECHAS']
    
    for project in projects:
        rows[0] += '\t[{}] {}'.format(project.id, project.name)        
    rows[0] += '\n'
    
    for versionDate in sortedDates:
        rowContent = str(versionDate)
        for project in projects:
            rowContent += '\t'
            for version in project.versions:
                if ( version.getDateFromReleaseDate() == versionDate ):
                    if (version.description is None): version.description = ''
                    rowContent += '{} ({})'.format( version.name, version.description[:30].replace( '\t', ' - ').replace( '\n', ' - '.replace( '\r', ' - ' )))
                    #break
        rowContent += '\n'
        rows.append(rowContent)

    dumpFile = open( fileName, 'w' )
    print( 'FILE OPENED' )
    
    for rowContent in rows:
        dumpFile.write(rowContent)

    dumpFile.close()
    print( 'FILE CLOSED' )

def getReportFileName(path, context, dateTime = datetime.datetime.now()):
    dateTimeInformation = str( dateTime ).replace( ':', '.')[:19]
    return f'{path}\\{dateTimeInformation}-{context}.csv'

def getBackupFileName( reportFileName ):
    path = os.path.dirname( reportFileName )
    reportDate = reportFileName[len( path )+1:len( path )+11]
    context = reportFileName[str.find( reportFileName, '-', len( path + reportDate ) + 1):]
    backupFileName = f'{path}\\{reportDate}{context}.backup.npy'
    return backupFileName

def backup( projects, reportFileName ):
    backupInformation = numpy.array( projects )
    backupFileName = getBackupFileName( reportFileName )
    numpy.save( backupFileName, backupInformation )

def restoreBackup( reportFileName ):
    backupFileName = getBackupFileName( reportFileName )
    if ( fileExists( backupFileName )):
        print( 'RESTORING DATA FROM BACKUP...' )
        return numpy.load( backupFileName, allow_pickle=True )

def fileExists( fileName ):
    path = os.path.dirname( fileName )
    name = fileName[len( path )+1:]
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
    return False

def printProject( project ):
    print( 'Project {}: {}'.format(project.id, project.name ))

def printVersion( version ):
    releasedOn = 'Unreleased - '
    if ( version.released ):
        if ( version.releaseDate is None ): releasedOn = 'Released/???? -'
        else: releasedOn = version.releaseDate + ' - '

    print( '\tVersion {}: {}{}'.format( version.name, releasedOn, version.description ))
    
def printContentOfProjects( projects ):
    for project in projects:
            printProject( project )
            for version in project.versions:
                printVersion( version )