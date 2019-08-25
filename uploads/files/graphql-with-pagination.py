import json

import requests


url = 'https://api.github.com/graphql'
oauth_token = 'PASTE YOUR OAUTH TOKEN HERE'
headers = {'Authorization': f'bearer {oauth_token}'}

graphql_query = '''\
query($previousEndCursor:String) {
  repository(owner:"python", name:"cpython") {
    pullRequests(states: OPEN, first: 100, after: $previousEndCursor) {
        nodes {
          title
        }
        pageInfo {
          endCursor
          hasNextPage
        }
        totalCount
    }
  }
}
'''

def get_details(endCursor=None):
    github_query = {}
    github_query["query"] = graphql_query
    if endCursor is not None:
        variables = f'''{{
                          "previousEndCursor": "{endCursor}"
                     }}
                     '''
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
    page = 1
    response = get_details()
    print(f'Page {page} fetched')
    results = response['data']['repository']['pullRequests']['nodes']
    while response['data']['repository']['pullRequests']['pageInfo']['hasNextPage']:
        page = page + 1
        response = get_details(
          response['data']['repository']['pullRequests']['pageInfo']['endCursor']
        )
        print(f'Page {page} fetched')
        results = results + response['data']['repository']['pullRequests']['nodes']
     # Just to print it in the same structure that we used to send it
    print(json.dumps(results, indent=2, sort_keys=False))
if __name__ == "__main__":
    main()
