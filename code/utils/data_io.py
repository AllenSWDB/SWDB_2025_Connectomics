import sys
from os.path import join as pjoin
import platform
import pandas as pd
import numpy as np

__all__ = [
    'mat_version',
    'load_proofread_dendrite_list',
    'load_proofread_axon_list',
    'load_synapse_df',
    'load_target_structure',
    'load_cell_df'
]

# Add the directory for the data and utilities
mat_version = 1196

platstring = platform.platform()
system = platform.system()
if system == "Darwin":
    # macOS
    data_root = "/Volumes/Brain2025/"
elif system == "Windows":
    # Windows (replace with the drive letter of USB drive)
    data_root = "E:/"
elif "amzn" in platstring:
    # then on CodeOcean
    data_root = "/data/"
else:
    # then your own linux platform
    # EDIT location where you mounted hard drive
    data_root = "/media/$USERNAME/Brain2025/"

# Set the directory to load prepared data and utility code
data_dir = pjoin(data_root, f"v1dd_{mat_version}")
utils_dir = pjoin("utils")

# Add utilities to path
sys.path.append(utils_dir)

def load_proofread_dendrite_list():
    return np.load(
        pjoin(data_dir, f"proofread_dendrite_list_{mat_version}.npy")
    )

def load_proofread_axon_list():
    return np.load(pjoin(data_dir, f"proofread_axon_list_{mat_version}.npy"))

def load_synapse_df():
    return pd.read_feather(
        pjoin(data_dir, f"syn_df_all_to_proofread_to_all_{mat_version}.feather")
    )

def load_target_structure():
    return pd.read_feather(
        pjoin(data_dir, f"syn_label_df_all_to_proofread_to_all_{mat_version}.feather")
    )["tag"]

def load_cell_df():
    return pd.read_feather(pjoin(data_dir, "soma_and_cell_type_{mat_version}.feather")