from re import A
import requests as rq
import json
import pandas as p
import numpy as n

from requests.auth import HTTPBasicAuth

credentials = json.loads(open('/Users/dwhelan/Desktop/Computer Science/Sweng/Github-API-Access/access_and_graphs/creds.json').read())
auth = HTTPBasicAuth(credentials['username'],credentials['password'])

def top_level():
    data = rq.get('https://api.github.com/users/' + credentials['username'],auth=auth)
    data = data.json()
    print("Hunting and Gathering Repo info\n")
    url = data['repos_url']
    page = 1
    repos = []
    while(True):
        resp = rq.get(url)
        resp = resp.json()
        repos = repos + resp
        fetched = len(resp)
        if(fetched == 30):
            page = page + 1
            url = data['repos_url'] + "?page=" + str(page)
        else:
            break
    repo_info = []
    for i, repo in enumerate(repos):
        data  = []
        data.append(repo['id'])
        data.append(repo['name'])    
        data.append(repo['owner']['login'])
        data.append(repo['url'])
        data.append(repo['url'] + '/languages')
        data.append(repo['description'])
        data.append(repo['commits_url'].split('{')[0])
        data.append(repo['created_at'])
        data.append(repo['updated_at'])
        data.append(repo['open_issues_count'])
        repo_info.append(data)
    repo_dataframe = p.DataFrame(repo_info, columns = ['ID','Name','Owner','Repo URL','Languages URL','Description','Commits URL','Created At','Updated At','Open Issues'])
    print("Repos Hunted and Gathered\n")

    print("Hunting and Gathering Language Data\n")
    for i in range(repo_dataframe.shape[0]):
        resp = rq.get(repo_dataframe.loc[i,'Languages URL'],auth=auth)
        resp = resp.json()
        if resp != {}:
            languages = []
            for key in resp.items():
                languages.append(key)
            languages = ', '.join(str(v) for v in languages)
            repo_dataframe.loc[i,'Languages'] = languages
        else:
            repo_dataframe.loc[i,'Languages'] = ""
    print("Languages Hunted and Gathered\n")
    repo_dataframe.to_csv('repos_info.csv', index = False)
    print("Repos saved to repos_info.csv\n")

    print("Hunting and Gathering Commits Data\n")
    commits_info = []
    for i in range(repo_dataframe.shape[0]):
        url = repo_dataframe.loc[i, 'Commits URL']
        page = 1
        while(True):
            resp = rq.get(url)#,auth=auth)
            resp = resp.json()
            print("URL: {} Commits: {}\n".format(url, len(resp)))
            for c in resp:
                print(c)
                commit_data = []
                commit_data.append(repo_dataframe.loc[i, 'ID'])
                commit_data.append(repo_dataframe.loc[i, 'Name'])
                commit_data.append(str(c['sha']))
                commit_data.append(c['commit']['committer']['date'])
                commits_info.append(commit_data)
            if(len(resp) == 30):
                page = page + 1
                url = repo_dataframe.loc[i, 'Commits URL'] + "?page=" + str(page)
            else:
                break
    commits_dataframe = p.DataFrame(commits_info, columns = ['Repo ID','Repo Name','Commit ID','Date'])
    commits_dataframe.to_csv('commits_info.csv', index=False)
    print("Commits infor saved to commits_info.csv\n")

if __name__ == "__main__":
    top_level()

