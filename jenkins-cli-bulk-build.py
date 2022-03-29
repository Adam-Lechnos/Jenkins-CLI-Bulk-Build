#!/usr/bin/env python3

import requests, sys, os, time, json, argparse

parser = argparse.ArgumentParser(description='Perform bulk Jenkins builds against JSON file')
parser.add_argument('-e', '--environment', default='prod', help='Optional. Set the Jenkins envrionment (Prod|Dev, Default=Prod)')
parser.add_argument('-j', '--job', default='api_processor', help='Optional (Default=api_processor)')
args = parser.parse_args()

class Build:
    def __init__(self, url, auth, git_org):
        self.url = url
        self.auth = auth
        self.git_org = git_org

    def trigger(self, payload, build):
        data=payload
        response = requests.post(self.url+"/buildWithParameters", data=data, auth=self.auth)

        if response.status_code == 201:
            print(f"Jenkins build '{build}' initiated successfully")
        else:
            sys.exit(f"Jenkins build '{build}' failed, Status code: {response.status_code}")

        return(build)

if args.environment.lower() == "prod":
    jenkinsURL = "jenkins prod url here"
    with open('jenkins_token') as token_file:
        token = token_file.read().rstrip()
        print("\n++Prod Jenkins API++")
else:
    jenkinsURL = "jenkins dev url here"
    with open('jenkins_token_dev') as token_file:
        token = token_file.read().rstrip()
        print("\n++Dev Jenkins API++")

jenkinsParentJobLoc="/job/"+args.job
url=jenkinsURL + jenkinsParentJobLoc
git_org="github org here"
auth=(os.getlogin(),token)

with open('builds.json') as builds:
    data = json.load(builds)

execBuild=Build(url, auth, git_org)  
print("\n=============\nBuilding Jobs\n=============")
for i in data:
    data[i]['git_org']=git_org
    print(f"\n*{i}*\n\nParameters:\n{data[i]}\n")
    execBuild.trigger(data[i], i)
    time.sleep(2)

print("\nSUCCESS\n")
