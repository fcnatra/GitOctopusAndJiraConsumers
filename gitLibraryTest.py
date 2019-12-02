import gitlab
import requestsTools

#pip install gitlab --trusted-host pypi.org --trusted-host files.pythonhosted.org

def connect(url, accessToken):
    requestsTools.disableWarningForInsecureHttpRequests()
    gitRepository = gitlab.Gitlab(url, private_token=accessToken, ssl_verify=False)
    gitRepository.auth()
    return gitRepository

def printGroups(groupsManager):
    print('[GROUPS]')
    groups = groupsManager.list()
    for group in groups:
        print('\tGroup {}: {} - {}'.format(group.id, group.name, group.path))
    return groups

def printProjects(groupProjectsManager):
    projects = groupProjectsManager.list()
    groupManager = projects[0].manager._parent
    print('\n[PROJECTS] Group {}: {} - {}'.format(groupManager.id, groupManager.name, groupManager.path))
    for project in projects:
        print('\tProject {}: {}'.format(project.id, project.name))
    return projects

class FilterInformation:
    def __init__(self, startDate = '2019-04-01T00:00:00Z', dataPerPage = 50, pageLimit = 15):
        self.startDate = startDate
        self.dataPerPage = dataPerPage
        self.pageLimit = pageLimit

def printCommits(projectsManager, filterInformation):
    print('\n[COMMITS] Project {}: {}'.format(projectsManager.id, projectsManager.name))
    commits = projectsManager.commits.list(since=filterInformation.startDate)

    for commit in commits:
        print('\tCommit {} - {} {}'.format(commit.created_at, commit.author_name, commit.title))

    return commits

def printEvents(projectsManager, filterInformation):
    print('\n[EVENTS] Project {}: {}'.format(projectsManager.id, projectsManager.name))
    
    pageNumber = 0
    pageContainsEvents = True
    allEvents = []
    actionsOverMaster = []

    while(pageContainsEvents and pageNumber < filterInformation.pageLimit):
        events = projectsManager.events.list(since=filterInformation.startDate, per_page=filterInformation.dataPerPage, page=pageNumber)
        pageContainsEvents = (len(events) > 0)

        if (not pageContainsEvents): break
        
        for event in events: allEvents.append(event)

        pageContainsEvents = (len(events) == filterInformation.dataPerPage)
        if (pageContainsEvents): pageNumber+=1

    for event in allEvents:
        push_data = event._attrs.get( 'push_data' )
        ref = ''
        commitTitle = ''
        if( push_data is not None ):
            ref = push_data[ 'ref' ]
            commitTitle = push_data[ 'commit_title' ]
        print( '\tEvent {} - {} {} {} {}'.format(event.created_at, event.author_username, event.action_name, ref, commitTitle ))

    return allEvents

def printEventsRelatedToMaster(allEvents):
    print( '\n\t[ACTIONS OVER MASTER]' )
    for event in allEvents:
        push_data = event._attrs.get( 'push_data' )
        ref = ''
        commitTitle = ''
        if( push_data is not None ):
            ref = push_data[ 'ref' ]
            commitTitle = push_data[ 'commit_title' ]
        if ( 'master' in ref ):
            print( '\tEvent {} - {} {} {} {}'.format( event.created_at, event.author_username, event.action_name, 
                event.push_data['ref'], event.push_data['commit_title'] ))
