import sys
from os.path import join as pjoin
import platform
from typing import Optional
import pandas as pd
import numpy as np

__all__ = [
    "mat_version",
    "load_proofread_dendrite_list",
    "load_proofread_axon_list",
    "load_synapse_df",
    "load_target_structure",
    "load_cell_df",
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
utils_dir = pjoin("utils")


def _get_data_dir(linux_mount_location=None, windows_usb_drive=None):
    platstring = platform.platform()
    system = platform.system()
    if system == "Darwin":
        # macOS
        data_root = "/Volumes/Brain2025/"
    elif system == "Windows":
        if windows_usb_drive is None:
            raise ValueError("Windows USB drive letter must be specified, e.g. 'E'")
        data_root = f"{windows_usb_drive}:/"
    elif "amzn" in platstring:
        # then on CodeOcean
        data_root = "/data/"
    else:
        if linux_mount_location is None:
            raise ValueError(
                "Mount location must be specified, e.g. '/media/<mount_location>/Brain2025/'"
            )
        data_root = f"/media/{linux_mount_location}/Brain2025/"
    data_dir = pjoin(data_root, f"v1dd_{mat_version}")
    return data_dir


# Add utilities to path
sys.path.append(utils_dir)


def load_proofread_dendrite_list(
    linux_mount_location: Optional[str] = None, windows_usb_drive: Optional[str] = None
) -> np.ndarray:
    """Load the list of proofread dendrites root ids

    Parameters
    ----------
    linux_mount_location : str, optional
        The mount location for Linux users, if needed. Not needed on CodeOcean.
    windows_usb_drive : str, optional
        The USB drive letter for Windows users, if needed. Not needed on CodeOcean.

    Returns
    -------
    np.ndarray
        The array of proofread dendrites root ids.
    """
    data_dir = _get_data_dir(
        linux_mount_location=linux_mount_location, windows_usb_drive=windows_usb_drive
    )
    return np.load(pjoin(data_dir, f"proofread_dendrite_list_{mat_version}.npy"))


def load_proofread_axon_list(
    linux_mount_location: Optional[str] = None, windows_usb_drive: Optional[str] = None
) -> np.ndarray:
    """Load the list of proofread axons root ids

    Parameters
    ----------
    linux_mount_location : str, optional
        The mount location for Linux users, if needed. Not needed on CodeOcean.
    windows_usb_drive : str, optional
        The USB drive letter for Windows users, if needed. Not needed on CodeOcean.

    Returns
    -------
    np.ndarray
        The array of proofread axons root ids.
    """
    data_dir = _get_data_dir(
        linux_mount_location=linux_mount_location, windows_usb_drive=windows_usb_drive
    )
    return np.load(pjoin(data_dir, f"proofread_axon_list_{mat_version}.npy"))


def load_synapse_df(
    linux_mount_location: Optional[str] = None, windows_usb_drive: Optional[str] = None
) -> pd.DataFrame:
    """Load the synapse dataframe.

    Parameters
    ----------
    linux_mount_location : str, optional
        The mount location for Linux users, if needed. Not needed on CodeOcean.
    windows_usb_drive : str, optional
        The USB drive letter for Windows users, if needed. Not needed on CodeOcean.

    Returns
    -------
    pd.DataFrame
        The synapse dataframe.
    """
    data_dir = _get_data_dir(
        linux_mount_location=linux_mount_location, windows_usb_drive=windows_usb_drive
    )
    return pd.read_feather(
        pjoin(data_dir, f"syn_df_all_to_proofread_to_all_{mat_version}.feather")
    )


def load_target_structure(
    linux_mount_location: Optional[str] = None, windows_usb_drive: Optional[str] = None
) -> pd.Series:
    """Load the target structure tags.

    Parameters
    ----------
    linux_mount_location : str, optional
        The mount location for Linux users, if needed. Not needed on CodeOcean.
    windows_usb_drive : str, optional
        The USB drive letter for Windows users, if needed. Not needed on CodeOcean.

    Returns
    -------
    pd.Series
        The target structure tags.
    """
    data_dir = _get_data_dir(
        linux_mount_location=linux_mount_location, windows_usb_drive=windows_usb_drive
    )
    return pd.read_feather(
        pjoin(data_dir, f"syn_label_df_all_to_proofread_to_all_{mat_version}.feather")
    )["tag"]


def load_cell_df(
    linux_mount_location: Optional[str] = None, windows_usb_drive: Optional[str] = None
) -> pd.DataFrame:
    """Load the cell dataframe.

    Parameters
    ----------
    linux_mount_location : str, optional
        The mount location for Linux users, if needed. Not needed on CodeOcean.
    windows_usb_drive : str, optional
        The USB drive letter for Windows users, if needed. Not needed on CodeOcean.

    Returns
    -------
    pd.DataFrame
        The cell dataframe.
    """
    data_dir = _get_data_dir(
        linux_mount_location=linux_mount_location, windows_usb_drive=windows_usb_drive
    )
    return pd.read_feather(pjoin(data_dir, f"soma_and_cell_type_{mat_version}.feather"))
