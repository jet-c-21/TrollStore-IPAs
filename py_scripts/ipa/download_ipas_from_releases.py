"""
Author: Jet C.
GitHub: https://github.com/jet-c-21
Create Date: 2025-03-08
"""

__version__ = "0.0.1"

# >>> Dynamic Changing sys.path in Runtime by Adding Project Directory to Path >>>
import pathlib
import sys

THIS_FILE_PATH = pathlib.Path(__file__).absolute()
THIS_FILE_PARENT_DIR = THIS_FILE_PATH.parent
PROJECT_DIR = THIS_FILE_PARENT_DIR.parent.parent
sys.path.append(str(PROJECT_DIR))
print(f"[*INFO*] - append directory to path: {PROJECT_DIR}")
# <<< Dynamic Changing sys.path in Runtime by Adding Project Directory to Path <<<

import os
import json
from dotenv import load_dotenv
from typing import Optional, Dict, Union
from tqdm.auto import tqdm
import requests
from github import Github

SETTINGS_DIR = PROJECT_DIR / "settings"
assert SETTINGS_DIR.is_dir(), f"{SETTINGS_DIR} is not existed"

GITHUB_ENV_FILE = SETTINGS_DIR / "github.env"
assert GITHUB_ENV_FILE.is_file(), f"{GITHUB_ENV_FILE} is not existed"

load_dotenv(dotenv_path=GITHUB_ENV_FILE)

USER_HOME_DIR = pathlib.Path.home()


def download_file(file_download_link: str, download_path: pathlib.Path) -> Union[pathlib.Path]:
    """Download a file from a URL and save it to the specified path."""
    response = requests.get(file_download_link, stream=True)
    if response.status_code == 200:
        with open(download_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)
        print(f"[*INFO*] - Downloaded: {download_path}")
        return download_path
    else:
        print(f"[*ERROR*] - Failed to download: {file_download_link}")
        return None

def _download_ipas_from_swaggyp36000_trollstore_ipas(download_dir:Optional[pathlib.Path]=None, max_download_versions=6,):
    github_client = Github(os.getenv("GITHUB_TOKEN"))
    repo = github_client.get_repo("swaggyp36000/trollstore-ipas")

    if download_dir is None:
        download_dir = USER_HOME_DIR / "my_home" / "TrollStore-IPAs_Backup"
        download_dir.mkdir(parents=True, exist_ok=True)

    # releases = repo.get_releases()
    # for release in releases:
    #     print(release.title)

    app_json_file = PROJECT_DIR / "apps.json"
    with open(app_json_file, "r") as f:
        app_json = json.load(f)

    for app_idx, app_dict in enumerate(tqdm(app_json["apps"], desc="Processing Apps", unit="app"), start=1):
        app_dict:Dict
        app_name = app_dict["name"]

        print()
        msg = f"[*INFO*] - start downloading #{str(app_idx).zfill(3)}: {app_name} ..."
        print(msg)

        app_download_root_dir = download_dir / app_name
        app_download_root_dir.mkdir(parents=True, exist_ok=True)

        if max_download_versions == "max":
            ver_ls = app_dict["versions"]
        else:
            ver_ls = app_dict["versions"][:max_download_versions]

        for ver in ver_ls:
            download_url = ver["downloadURL"]
            download_file_name = download_url.split("/")[-1]
            download_file_path = app_download_root_dir / download_file_name
            if download_file_path.is_file():
                msg = f"[*INFO*] - {download_file_path} is existed, skip downloading"
                print(msg)
                continue

            download_file(download_url, download_file_path)

        msg = f"[*INFO*] - finish downloading #{str(app_idx).zfill(3)}: {app_name}\n"
        print(msg)


if __name__ == '__main__':
    _download_ipas_from_swaggyp36000_trollstore_ipas()