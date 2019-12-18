#!/usr/bin/env python

import json
import os
import re
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

body = issue['body']

# First find the identifier - an md5 hash sum
identifier = re.search("HelpMe Github Issue: (?P<name>md5.+)", body)
try:
    md5 = identifier.groups()[0]
except:
    sys.exit("Error parsing md5 identifier")

# Write the new issue to file, named by the md5
output_dir = os.path.join(root, "issues")
issue_dir = os.path.join(output_dir, md5)

for outdir in [output_dir, issue_dir]:
    if not os.path.exists(outdir):
        os.mkdir(outdir)

# For a simple organization, we will store the body of content in a file named
# by the issue number.
issue_number = issue.get("number")
output_file = os.path.join(issue_dir, "%s.md" % issue_number)

# More parsing could be done of the content here, but we are going to write to markdown.
# A more suitable flat format database could likely be used here
with open(output_file, 'w') as filey:
    filey.writelines("#%s\n" % issue.get('title'))
    filey.writelines("Submitted by %s %s\n" % (issue.get('user')['login'], issue.get('author_association')))
    filey.writelines(body)
