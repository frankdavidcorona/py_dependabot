import os
import subprocess
from git import Repo
from atlassian import Bitbucket

BITBUCKET_URL = 'https://bitbucket.org'
BITBUCKET_USERNAME = 'frank_corona'
BITBUCKET_TOKEN = 'ATBBJmBCu47Y2fbP93D9kMmTcXDaBB7F044C'
BITBUCKET_WORKSPACE = 'zerosurcharging'
BITBUCKET_REPO = 'audit-service'
BITBUCKET_BRANCH = 'develop'


def run_npm_audit_fix(repo_path):
    subprocess.run(['npm', 'install'], cwd=repo_path)
    audit_result = subprocess.run(
        ['npm', 'audit', 'fix'], cwd=repo_path, capture_output=True, text=True)
    return 'fixed' in audit_result.stdout


def create_branch_and_pull_request(bitbucket, branch_name, commit_msg):
    bitbucket.create_branch(
        BITBUCKET_WORKSPACE, BITBUCKET_REPO, branch_name, BITBUCKET_BRANCH)
    bitbucket.create_pull_request(
        project_id=BITBUCKET_WORKSPACE,
        repo_id=BITBUCKET_REPO,
        title=commit_msg,
        description=commit_msg,
        from_branch=branch_name,
        from_repo=BITBUCKET_REPO,
        to_branch=BITBUCKET_BRANCH,
        to_repo=BITBUCKET_REPO,
        close_source_branch=True
    )


# Clonar el repositorio de Bitbucket
bitbucket = Bitbucket(url=BITBUCKET_URL, username=BITBUCKET_USERNAME,
                      password=BITBUCKET_TOKEN)


repo_url = bitbucket.get_repo(BITBUCKET_WORKSPACE, BITBUCKET_REPO)[
    'links']['clone'][0]['href']
repo_path = f"{BITBUCKET_REPO}-temp"
repo = Repo.clone_from(repo_url, repo_path)

# Ejecutar npm audit fix
if run_npm_audit_fix(repo_path):
    # Crear una rama y Pull Request en Bitbucket
    commit_msg = 'chore: dependency updates'
    branch_name = 'security-updates'
    repo.git.checkout('-b', branch_name)
    repo.git.add('--all')
    repo.git.commit('-m', commit_msg)
    repo.git.push('--set-upstream', 'origin', branch_name)
    create_branch_and_pull_request(bitbucket, branch_name, commit_msg)

# Limpiar el repositorio clonado
subprocess.run(['rm', '-rf', repo_path])
