import requestsTools
import datetime
import random
import releaseContentTools
from releaseContentTools import Project
from datetime import timedelta
import authenticationInfo

class Space: 
        def __init__( self, id, name ): self.id, self.name =  id, name

def getSpaces( url ):
        jsonContent = requestsTools.getJsonFromUrl(url + '/spaces')
        spaces = ( Space( id, name ) for id, name in requestsTools.getNodesFromJson(jsonContent['Items'], 'Id,Name' ) )
        return spaces

def getProjects( url, space ):
        jsonContent = requestsTools.getJsonFromUrl('{}/{}/projects?skip=0&take=2147483647'.format(url, space.id))
        projects = ( Project( id, name ) for id, name in requestsTools.getNodesFromJson(jsonContent['Items'], 'Id,Name' ) )
        return projects

def getVersions( url, space, project ):
        jsonContent = requestsTools.getJsonFromUrl('{}/{}/projects/{}/releases?skip=0&take=2147483647'.format( url, space.id, project.id ) )
        versions = []
        for (id, assembled, releaseNotes, version) in requestsTools.getNodesFromJson( jsonContent['Items'], 'Id,Assembled,ReleaseNotes,Version' ):
                version = releaseContentTools.Version(id, version, releaseNotes, assembled is not None, assembled )
                versions.append( version )
                
        return versions

def retrieveDataFromOctopus( url ):
        print( 'RETRIEVING DATA FROM OCTOPUS...' )
        spaces = list(getSpaces(url))
        for space in spaces:
                projects = list( getProjects( url, space ) )
                for project in projects:
                        project.versions = list( getVersions(url, space, project) )
        return projects

reportFileName = releaseContentTools.getReportFileName('C:\\temp', 'octopusReleases')

projects = releaseContentTools.restoreBackup( reportFileName )
if( projects is None ):
        requestsTools.accessToken = authenticationInfo.octopusAccessToken
        requestsTools.setupAuthentication()
        projects = retrieveDataFromOctopus( authenticationInfo.octopusApiUrl )
        releaseContentTools.backup( projects, reportFileName )

#releaseContentTools.printContentOfProjects( projects )
releaseContentTools.dumpToFile( projects, reportFileName )