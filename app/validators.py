from re import search

def add_repo_validator(entry):
    """
    Validate the entry for '-a/--add-pkg-repository' parameter.

    :string: The repository string
    :returns: True if the entry is valid; otherwise False

    """
    pattern_list = [
        '(.+?):https://(.+?).com/(.+?)/(.+?).git',
        '(.+?):git@(.+?).com:(.+?)/(.+?).git'
    ]

    for pattern in pattern_list:
        found = search(pattern, entry)

        if found:
            return True

    return False
