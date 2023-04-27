from github import Github
import os
import requests
import easygui
from easygui import *
from tqdm import tqdm


def download_file_with_progress(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
    with open(filename, 'wb') as f:
        for data in response.iter_content(block_size):
            f.write(data)
            progress_bar.update(len(data))
    progress_bar.close()


username = "Remu-1"
repository = "FAUMC"
branch = "main"
folder_path = "Mods"


correct_dir_ans = easygui.ynbox('Would you like to install at the standard dir?', 'Installation', ('Yes', 'No'))
print(correct_dir_ans)
home_dir = os.path.expanduser("~")
local_dir_path = os.path.join(home_dir, "Library", "Application Support", "minecraft", "mods")

if os.path.exists(local_dir_path) and os.path.isdir(local_dir_path) and correct_dir_ans:
    print(f"Folder found: {local_dir_path}")

else:

    mc_dir = easygui.diropenbox(
        default='~',
        title='please select your minecraft mods directory'
    )
    if os.path.isdir(mc_dir):
        if os.path.basename(mc_dir) == "mods":
            print("folder is named 'mods'")
        else:
            mods_dir = os.path.join(mc_dir, "mods")
            if os.path.exists(mods_dir) and os.path.isdir(mods_dir):
                print("this directory contains a folder titled 'mods'")
            else:
                easygui.msgbox("the folder does not have the desired name or contain a subdirectory named 'mods'")
                exit()
    else:
        easygui.msgbox("this path does not point to a directory")
        exit()


g = Github()
repo = g.get_repo(f"{username}/{repository}")
contents = repo.get_contents(folder_path, ref=branch)

for content in contents:
    if content.type == "dir":
        continue

    file_name = content.name
    if os.path.exists(local_dir_path) and os.path.isdir(local_dir_path) and correct_dir_ans:
        file_path = os.path.join(local_dir_path, file_name)
    else:
        if os.path.exists(mc_dir) and os.path.isdir(mc_dir):
            file_path = os.path.join(mc_dir, "mods", file_name)

    if os.path.exists(file_path):
        print(f"{file_name} already exists.")
    else:
        print(f"{file_name} does not exist. Downloading...")
        download_url = content.download_url
        download_file_with_progress(download_url, file_path)
easygui.msgbox("Download Complete!")