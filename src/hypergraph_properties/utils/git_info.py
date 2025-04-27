import git


def get_current_commit_sha() -> str:
    repo = git.Repo(search_parent_directories=True)
    return repo.git.rev_parse(repo.head, short=True)
