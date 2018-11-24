repos = {}

def get_repository(name):
    if name not in repos:
        raise NotImplemented
    return repos[name]


def configure(repositories):
    global repos
    repos = repositories

