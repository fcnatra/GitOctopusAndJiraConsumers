import requestsTools
import authenticationInfo

requestsTools.accessToken = authenticationInfo.gitAccessToken

def getGroups(url):
    groupsUrl = url + '/groups/'
    jsonContent = requestsTools.getJsonFromUrl(groupsUrl)
    nodes = requestsTools.getNodesFromJson(jsonContent, 'id,web_url')
    return nodes

def getProjects(url, groupId):
    projectsUrl = url + '/groups/' + str(groupId) + '/projects/'
    jsonContent = requestsTools.getJsonFromUrl(projectsUrl)
    nodes = requestsTools.getNodesFromJson(jsonContent, 'id,name')
    return nodes

def getProjectActivity(url, projectId):
    projectAcivityUrl = url + '/projects/' + str(projectId) + '/events/'
    jsonContent = requestsTools.getJsonFromUrl(projectAcivityUrl)
    nodes = requestsTools.getNodesFromJson(jsonContent, 'created_at,author_username,action_name,push_data')
    return nodes

def jsonSample(url):    
    groups = getGroups(url)

    for groupId, groupUrl in groups:
        print('Group ' + str(groupId) + ': ' + groupUrl)

        projects = getProjects(url, groupId)

        for projectId, projectName in projects:
            print('\t Project ' + str(projectId) + ': ' + projectName)
            
            activities = getProjectActivity(url, projectId)

            for dataRow in activities:
                print('\t\t' + str(dataRow[0]) + ' by ' + dataRow[1] + ' (' + dataRow[2], end=')')
                if (len(dataRow) == 4):
                    extendedInfo = dataRow[3]
                    print(' ' + extendedInfo['action'] + ' ' + extendedInfo['ref_type'] + ' ' + extendedInfo['ref'] + ': ' + str(extendedInfo['commit_title']))
                else:
                    print('\n')

requestsTools.setupAuthentication()
jsonSample(authenticationInfo.gitApiUrl)

