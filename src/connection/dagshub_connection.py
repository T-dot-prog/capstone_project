import os

def fetch_data_from_dagshub(repo_owner, repo_name, file_path, output_path, branch="main", token=None):
    """
    Fetches a file from a DagsHub repository for data versioning.

    Args:
        repo_owner (str): DagsHub repository owner.
        repo_name (str): DagsHub repository name.
        file_path (str): Path to the file in the repository.
        output_path (str): Local path to save the downloaded file.
        branch (str): Branch name (default: "main").
        token (str, optional): DagsHub personal access token for private repos.

    Returns:
        str: Path to the downloaded file.
    """
    import requests

    base_url = f"https://dagshub.com/{repo_owner}/{repo_name}/raw/{branch}/{file_path}"
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    response = requests.get(base_url, headers=headers, stream=True)
    if response.status_code == 200:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        return output_path
    else:
        raise Exception(f"Failed to fetch file from DagsHub. Status code: {response.status_code}, URL: {base_url}")
