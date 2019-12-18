#!/usr/bin/env python

import json
import os
import re
import requests
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
payload_path = os.environ.get("GITHUB_EVENT_PATH")
if not payload_path:
    sys.exit("GITHUB_EVENT_PATH not found in environment")

if not os.path.exists(payload_path):
    sys.exit("%s does not exist!" % payload_path)

payload = json.loads(open(payload_path, "r").read())

# The action should be opened, but we check anyway
action = payload.get("action", "closed")
if action != "opened":
    sys.exit("Issue parsing only happens for newly opened issues.")

# Retrieve the issue, and parse the body
issue = payload.get("issue")
if not issue:
    sys.exit("issue not found in payload.")

body = issue["body"]

# First find the identifier - an md5 hash sum
identifier = re.search("HelpMe Github Issue: (?P<name>md5.+)", body)
try:
    md5 = identifier.groups()[0]
except:
    sys.exit("Error parsing md5 identifier")

# Write the new issue to file, named by the md5
output_dir = os.path.join(root, "issues")
issue_dir = os.path.join(output_dir, md5)

exists = True
for outdir in [output_dir, issue_dir]:
    if not os.path.exists(outdir):
        exists = False
        os.mkdir(outdir)

# For a simple organization, we will store the body of content in a file named
# by the issue number.
issue_number = issue.get("number")
output_file = os.path.join(issue_dir, "%s.md" % issue_number)

# If the issue already exists, we will find the first issue that was opened
if exists:
    issue_numbers = [int(x.split(".")[0]) for x in os.listdir(outdir)]
    issue_numbers.sort()
    if issue_numbers:
        first_issue = issue_numbers[0]

        # Derive the previous issue url from the current
        issue_url = "%s/%s" % (issue.get("html_url").split("/")[:-1], first_issue)

        # Grab variables from the environment
        token = os.environ.get("GITHUB_TOKEN")
        repo = os.environ.get("GITHUB_REPOSITORY")
        issues_url = "https://api.github.com/repos/%s/issues" % repo

        # First, comment on the issue
        data = {"body": "This issue has already been opened:\n %s" % issue_url}
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token %s" % token,
        }
        response = requests.post(
            "%s/%s/comments" % (issues_url, issue_number), headers=headers, json=data
        )

        print(issues_url)
        print(data)
        print(response)

        # If successful, close the new issue
        if response.status_code in [200, 201]:
            data = {"state": "closed"}
            requests.patch(
                "%s/%s" % (issues_url, issue_number), headers=headers, json=data
            )

        else:
            print(response.json())
            sys.exit("There was a problem commenting on the issue")


# More parsing could be done of the content here, but we are going to write to markdown.
# A more suitable flat format database could likely be used here
with open(output_file, "w") as filey:
    filey.writelines("# %s\n" % issue.get("title"))
    filey.writelines(
        "Submitted by %s %s\n"
        % (issue.get("user")["login"], issue.get("author_association"))
    )
    filey.writelines(body)
