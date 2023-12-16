from git import Repo

repo = Repo(".")
origin = repo.remote(name='origin')
