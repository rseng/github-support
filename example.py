#!/usr/bin/env python3

from helpme.main import get_helper


def submit_issue(exc):
    """a helper function to submit an issue based on an exception. This
       is overly commented to walk you through how this works, and what you
       can define.
    """
    # The GitHub helper doesn't require a token when the user has a browser handy
    # Set confirm to False to not require confirming the environment whitelist
    # You can set require_token to True to require using the GitHub API.
    helper = get_helper("github", confirm=False)

    # A custom body for the user to add metadata to.
    body = """
#### What is the problem?
<!-- Please write a few sentences about the issue-->
#### What steps will reproduce the problem?
<!-- What triggered this error? -->
#### Is there anything else that would be useful to know in this context?
"""

    # For a simple identifier for the hash, we will just use the exception
    # type, name, and message. You will need to decide what to use to be
    # consistent for your software package
    identifier = "%s|%s|%s" % (type(exc).__name__, exc.name, exc.msg)
    helper.run_headless(
        identifier=identifier,
        title=exc.msg,
        body=body,
        repo="rseng/github-support",
    )


try:
    import thiscrazymoduledoesntexist
except Exception as exc:
    # You likely want to use metadata from the exception for the issue identifier
    submit_issue(exc)
