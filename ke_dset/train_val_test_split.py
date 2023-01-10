from pathlib import Path
import os

import numpy as np

from ke_dset.configs import ORI_KE2_PATH, ORI_KE_PATH, BLACK_LIST

np.random.seed(1)

KE2_DIRS = list(Path(ORI_KE2_PATH).iterdir())
KE_DIRS = list(Path(ORI_KE_PATH).iterdir())


KE2_DIRS = [i for i in KE2_DIRS if (i.parent.name, i.name) not in BLACK_LIST]
KE_DIRS = [i for i in KE_DIRS if (i.parent.name, i.name) not in BLACK_LIST]

DSET_DIR = "/mnt/sda/shane/projects/my-demucs/ke_ori_dset"

os.makedirs(DSET_DIR, exist_ok=True)

dset_flags = ["train", "valid", "test"]
for flag in dset_flags:
    os.makedirs(f"{DSET_DIR}/{flag}", exist_ok=True)


flag = np.random.choice(
    dset_flags,
    size=len(KE2_DIRS) + len(KE_DIRS),
    p=[0.9, 0.05, 0.05]
)

for idx, dir_ in enumerate(KE2_DIRS + KE_DIRS):
    dset_name = dir_.parent.name
    song_name = dir_.name
    os.symlink(
        src=dir_,
        dst=f"{DSET_DIR}/{flag[idx]}/{dset_name}_{song_name}"
    )
    if flag[idx] == "valid":
        os.symlink(
            src=dir_,
            dst=f"{DSET_DIR}/train/{dset_name}_{song_name}"
        )
