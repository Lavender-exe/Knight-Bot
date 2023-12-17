import git

repo = git.Repo(".")
origin = repo.remote(name='origin')
