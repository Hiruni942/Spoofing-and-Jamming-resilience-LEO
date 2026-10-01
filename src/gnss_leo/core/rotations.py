"""
Rotation matrices for coordinate transformations.
"""

import numpy as np


def rotation_1(angle):
    """
    Rotation matrix about x-axis.
    
    Parameters
    ----------
    angle : float
        Rotation angle in radians
        
    Returns
    -------
    np.ndarray
        3x3 rotation matrix
    """
    c = np.cos(angle)
    s = np.sin(angle)
    
    return np.array([
        [1, 0, 0],
        [0, c, -s],
        [0, s, c]
    ])


def rotation_3(angle):
    """
    Rotation matrix about z-axis.
    
    Parameters
    ----------
    angle : float
        Rotation angle in radians
        
    Returns
    -------
    np.ndarray
        3x3 rotation matrix
    """
    c = np.cos(angle)
    s = np.sin(angle)
    
    return np.array([
        [c, -s, 0],
        [s, c, 0],
        [0, 0, 1]
    ])
