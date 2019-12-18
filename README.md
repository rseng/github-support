# GitHub Support

[![https://img.shields.io/badge/rseng-project-purple](https://img.shields.io/badge/rseng-project-purple)](https://rseng.github.io/)

Hey research software engineers! How often do you support a user might trigger a bug
in your Python software and not tell you about it? Or how often is a bug triggered
but not enough information is provided about it?

## Who is Responsible?

We shouldn't place the burden on collecting and submission of information on the user -
they already have their own research and domain of knowledge to worry about. But
can we help? Wouldn't it be neat if we could embed a support system into our Python software,
and one that would interact with version control, namely GitHub? 

## What do We Need?

We need a **version controlled** and **automated** issue reporting system that guides
users to open issues that post all required data, and is able to find and close redundant issues.
It might look something like this:

 - the user triggers a bug
 - the traceback of the error is automatically collected
 - a GitHub issue is opened that includes environment, traceback, and context
 - the user can preview and add additional detail to the issue
 - the issue is assigned an identified based on a hash of it's metadata
 - a GitHub workflow will check the hash, and direct the user to another issue if it's already open

This repository is an example of exactly that. The repository itself provides the following 
files:

 - [.github/workflows](.github/workflows): include workflows to handle parsing issues.
 - [issues](issues): the small database of issues, organized by their identifiers.
 - [example.py](example.py): a dummy python script that shows throwing an exception to report an issue.

## Getting Started

### Install helpme

You'll need the [helpme](https://vsoch.github.io/helpme) command line client, version 0.0.39 or later.
You can install that with the [requirements.txt](requirements.txt) file.

```bash
pip install -r requirements.txt
```

### Start with an Example

Once you've installed, take a look at [example.py](example.py) to see what is going on.
We basically catch an exception, generate an identifier from some of its metadata,
and then generate a helpme helper for GitHub to post an issue for it. You can take a look
at an [example issue](https://github.com/rseng/github-support/issues/1) here! If you
want more examples of arguments and usage of helpme, see [the GitHub headless docs](https://vsoch.github.io/helpme/helper-github#headless).

### Choose a Workflow

Once the issue is submit, it's the workflow that derives the logic for how to handle it.
For example, if an identifier generates a hash that is already found, we would want to
close the issue with a message that points to the previous issue. For
an example of handling this, see the [report_issue](.github/workflows/report_issue.yml)
workflow.


