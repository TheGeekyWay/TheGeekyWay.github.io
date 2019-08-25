import json

import requests


url = 'https://api.github.com/graphql'
oauth_token = 'PASTE YOUR OAUTH TOKEN HERE'
headers = {'Authorization': f'bearer {oauth_token}'}

# Replace the query within strings to any custom
# one that you wish to try
graphql_query = '''\
query {
  repository(owner:"python", name:"cpython") {
    pullRequests(states: OPEN, first: 1) {
      nodes {
        title
      }
    }
  }
}
'''
variables = '''\

'''

def get_details():
    github_query = {}
    github_query["query"] = graphql_query
    github_query["variables"] = variables
    github_query = json.dumps(github_query)

    response = requests.post(url, data=github_query, headers=headers)
    response.raise_for_status()
    response = json.loads(response.content)

    # Print errors more readably
    if 'errors' in response:
        for error in response['errors']:
            print(error['message'])
        exit()
    return response


def main():
    response = get_details()

    # Just to print it in the same structure that we used to send it
    print(json.dumps(response, indent=2, sort_keys=False))
if __name__ == "__main__":
    main()
