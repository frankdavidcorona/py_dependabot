import os
import subprocess
from git import Repo

LOCAL_REPOS_DIRECTORY = '/Users/frank/Developer/strictlyzero/repos/'


def run_npm_audit_fix(repo_path):
    subprocess.run(['npm', 'install'], cwd=repo_path)
    audit_result = subprocess.run(
        ['yarn', 'audit', 'fix'], cwd=repo_path, capture_output=True, text=True)
    return 'fixed' in audit_result.stdout


repo_dirs = [d for d in os.listdir(LOCAL_REPOS_DIRECTORY) if os.path.isdir(
    os.path.join(LOCAL_REPOS_DIRECTORY, d))]
total_repos = len(repo_dirs)

for index, repo_name in enumerate(repo_dirs):
    repo_path = os.path.join(LOCAL_REPOS_DIRECTORY, repo_name)
    repo = Repo(repo_path)

    progress_percentage = (index + 1) / total_repos * 100
    print(
        f"Procesando repositorio {index + 1}/{total_repos} ({progress_percentage:.2f}%): {repo_name}")

    if run_npm_audit_fix(repo_path):
        commit_msg = 'chore: update security dependencies'
        branch_name = 'security-updates'
        repo.git.checkout('-b', branch_name)
        repo.git.add('--all')
        repo.git.commit('-m', commit_msg)

        print(
            f"Actualizaciones de seguridad aplicadas en el repositorio {repo_name}.")
        print(
            f"Revisa y fusiona la rama '{branch_name}' en la rama principal.")
    print("\n")
