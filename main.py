import requests
import json
from getpass import getpass
from simple_term_menu import TerminalMenu

def main():
  orgId = input("Please input your organization's ID:")
  apiToken = getpass(prompt='Please input your token:')

  endpoint = "https://snyk.io/api/v1/org/" + orgId + "/projects"

  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'token ' + apiToken
  }

  values = ""

  request = requests.request("POST", endpoint, headers=headers, data=values)
  response = request.json()

  options = ["Delete all projects", "Move all projects"]
  terminal_menu = TerminalMenu(options, title="What would you like to do ?")
  menu_entry_index = terminal_menu.show()

  if (menu_entry_index == 0):
    delete(apiToken, response, orgId)
  else:
    move(apiToken, response, orgId)

def delete(token, obj, orgId):
  while obj['projects']:
    project = obj['projects'].pop()
    projectId = project['id']
    delEndpoint = "https://snyk.io/api/v1/org/" + orgId + "/project/" + projectId
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'token ' + token
    }

    values= ""

    request = requests.request("DELETE", delEndpoint, headers=headers, data=values)
    if (request.status_code == 200):
        print("Project " + projectId + "was successfully deleted")
    else:
        print("An error occurred when deleting project " + projectId + ".")

def move(token, obj, orgId):
  targetOrgId = input("Please input the target organization's ID:")
  while obj['projects']:
    project = obj['projects'].pop()
    projectId = project['id']
    delEndpoint = "https://snyk.io/api/v1/org/" + orgId + "/project/" + projectId + "/move"
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'token ' + token
    }

    values = json.dumps({"targetOrgId": targetOrgId}, indent=4)

    request = requests.request("PUT", delEndpoint, headers=headers, data=values)
    if (request.status_code == 200):
        print("Project " + projectId + "was successfully moved")
    else:
        print("An error occurred when moving project " + projectId + ". - " + request.text)
        
if __name__ == "__main__":
  main()
