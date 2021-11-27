"""Script for getting Follow The Money data."""
import pandas as pd


def get_and_save_ftm_data(path, target):
    """
    Get the data from the FTM repository and save it to csv format.

    Parameters
    ----------
    path : str
        http path to the ftm repo file.
    target : str
        target destination.

    """
    pd.read_csv(path, sep='|').to_csv(target, index=False, sep='|')


def get_data(path):
    """
    Get the data from local storage.

    Parameters
    ----------
    path : str
        path to local destination.

    Returns
    -------
    pandas.DataFrame
        pandas.DataFrame of the FTM data.

    """
    return pd.read_csv(path, sep='|')
