import requests, json
import urllib3

#pip install requests  --trusted-host pypi.org --trusted-host files.pythonhosted.org

accessToken = None
auth = None
verify = False

def setupAuthentication():
    disableWarningForInsecureHttpRequests()

def disableWarningForInsecureHttpRequests():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getResponseFromUrl( url ):
    response = None
    if (accessToken is not None):
        parameterConcatenator = '&' if ('?' in url) else '?'    
        response = requests.get(url + parameterConcatenator + accessToken, verify=verify)
    elif (auth is not None ):
        response = requests.get(url, auth=auth, verify=verify)
    else:
        response = requests.get(url, verify=verify)
    
    return response

def getContentFromUrl(url):
    response = getResponseFromUrl(url)
    return response.content

def getJsonFromUrl(url):
    content = getContentFromUrl(url)
    return json.loads(content)

def getNodesFromJson(jsonContent, nodeNamesCsv):
    values = []
    for mainNode in jsonContent:
        if (type(mainNode) is not str):
            nodes = []
            for childNode in nodeNamesCsv.split(','):
                if (mainNode.__contains__(childNode)):
                    nodes.append(mainNode[childNode])
                else:
                    nodes.append(None)
            values.append(nodes)

    return values
