import datetime
import requests, json
import requestsTools
import releaseContentTools
from releaseContentTools import Version, Project
from jira.client import JIRA
import authenticationInfo

#pip install jira --trusted-host pypi.org --trusted-host files.pythonhosted.org
#pip install requests --trusted-host pypi.org --trusted-host files.pythonhosted.org

def runJiraTestCall( authInfo ):
    jira_options = {
        'server': 'https://jira.url/jira/rest/api/latest/issue/ISSUECODE-001',
        'verify': False
    }

    jira_client = JIRA(options=jira_options, basic_auth=authInfo, validate=True)
    print(jira_client.projects())

def runRequestTestCall( authInfo ):
    print( '\n---------------------------------------------\n' )
    response = requests.get( url= 'https://jira.url/jira/rest/api/latest/issue/ISSUECODE-001', auth=authInfo, verify=False )
    print( response.content )
    print( response.status_code )
    print( response.reason )

def getProjects(url):
    jsonContent = requestsTools.getJsonFromUrl( url + '/project' )
    projects = (Project(id, name) for id, name in requestsTools.getNodesFromJson(jsonContent, 'id,name'))
    return projects

def getVersions(url, project):
    jsonContent = requestsTools.getJsonFromUrl('{}/project/{}/versions'.format( url, project.id ))

    if ( jsonContent.__len__() > 0):
        jsonNodes = requestsTools.getNodesFromJson(jsonContent, 'id,name,description,released,releaseDate')
        versions = ( Version( id, name, description, released, releaseDate ) for id, name, description, released, releaseDate in jsonNodes)
    else:
        versions = []

    return versions

def retrieveJiraData(url):
    print('RETRIEVING DATA FROM JIRA...')
    projects = list(getProjects(url))
    for project in projects:
        versions = list(getVersions(url, project))
        project.versions = versions

    return projects

def getSampleProjects():
    project1 = Project( 1, 'one' )
    project1.versions = [
        Version( 11, 'one-1', 'one-1-desc', True, '2018-09-1' ),
        Version( 12, 'one-2', 'one-2-desc', True, '2018-11-2' ),
        Version( 13, 'one-3', 'one-3-desc', True, '2018-11-3' ),
    ]

    project2 = Project( 2, 'two' )
    project2.versions = [
        Version( 21, 'two-1', 'two-1-desc', True, '2018-10-1' ),
        Version( 22, 'two-2', 'two-2-desc', True, '2018-10-2' ),
        Version( 23, 'two-3', 'two-3-desc', True, '2018-11-3' ),
    ]

    return [ project1, project2 ]


requestsTools.auth = authenticationInfo.jiraBasic_auth
reportFileName = releaseContentTools.getReportFileName( 'c:\\temp', 'jiraVersions' )

projects = releaseContentTools.restoreBackup( reportFileName )
if ( projects is None ):
        requestsTools.disableWarningForInsecureHttpRequests()
        projects = retrieveJiraData( authenticationInfo.jiraApiUrl )
        releaseContentTools.backup( projects, reportFileName )

#releaseContentTools.printContentOfProjects( projects )
releaseContentTools.dumpToFile( projects, reportFileName )
