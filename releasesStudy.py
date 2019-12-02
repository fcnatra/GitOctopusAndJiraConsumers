import gitLibraryTest
import authenticationInfo

gitRepository = gitLibraryTest.connect(authenticationInfo.gitBaseUrl, authenticationInfo.gitAccessToken)

groupsManager = gitRepository.groups
gitLibraryTest.printGroups(groupsManager)

groupId = 41
groupProjectManager = groupsManager.get(groupId).projects
gitLibraryTest.printProjects(groupProjectManager)

projectId = 23
projectManagerRETAbet = gitRepository.projects.get(projectId)

filterInformation = gitLibraryTest.FilterInformation(startDate = '2019-04-11T00:00:00Z')
gitLibraryTest.printCommits(projectManager, filterInformation)

events = gitLibraryTest.printEvents(projectManager, filterInformation)

gitLibraryTest.printEventsRelatedToMaster(events)