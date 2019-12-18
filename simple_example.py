#!/usr/bin/env python3

from helpme.main import get_helper

try:
    import thiscrazymoduledoesntexist
except Exception as exc:
    # The simple example doesn't provide body, title, or identifier
    # You wouldn't be able to organize repeated issues without identifier
    helper = get_helper("github", confirm=False)
    helper.run_headless(repo="rseng/github-support")
