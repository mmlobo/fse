"""
plotting.py

Module containing plotting functions for visualization.

Project: Fault Slip and Separation Explorer Tool
Author: Marta Magán Lobo
Date: 2022

"""
import math
from typing import Tuple, Union
import mplstereonet
import matplotlib.pyplot as plt
import numpy as np

def plot_dip_separation(fault: Tuple[Union[int, float], Union[int, float]], 
                        bedding: Tuple[Union[int, float], Union[int, float]], 
                        net_slip: Union[int, float]):
    """
    Plotting function to visualize dip separation relationships based on fault and bedding orientations.

    Args:
    - fault (tuple): Fault plane parameters [dip, dip direction].
    - bedding (tuple): Bedding plane parameters [dip, dip direction].
    - net_slip: Amount of net slip on the fault.

    Returns:
    - None (displays a plot).

    This function generates a plot that shows different dip separation relationships 
    based on the given fault and bedding orientations and the net slip.

    Note: Requires matplotlib and numpy libraries.
    """
    
    # Calculate cutoff pitch based on fault and bedding angles
    cutoff = cutoff_pitch(fault, bedding)
    
    # Create the plot
    fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(8, 6))
    ax1.set_aspect('equal', adjustable='box')  # Set aspect ratio
    
    # Customize ticks and secondary x-axis
    plt.xticks([10, 45, 80, 100, 135, 170, 190, 225, 260, 280, 315, 350])
    plt.yticks(np.arange(0, 190, 45))
    secax = ax1.secondary_xaxis('top')
    secax.set_xticks([0, 90, 180, 270, 360])
    
    # Set limits and draw reference lines
    plt.xlim(0, 360)
    plt.ylim(0, 180)
    plt.axhline(90, color="black", linestyle='dashed')
    plt.axvline(180, color="black", linestyle='dashed')
    
    # Define x coordinates for filling areas using numpy arrays
    x1 = np.arange(180, 370, 10)
    x2 = np.arange(0, 190, 10)
    x3 = np.array([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 90, 90, 90, 90, 90, 90, 90, 90, 90])
    x4 = np.array([90, 90, 90, 90, 90, 90, 90, 90, 90, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180])
    
    # Fill areas with different colors using numpy functions
    ax1.fill_between(-(180 - x1), x2, 90, color='yellow', alpha=.2, label='REVERSE DIP SEPARATION')
    ax1.fill_between(x1, x2, 90, color='orange', alpha=.2, label='NORMAL DIP SEPARATION')
    ax1.fill_between(-(180 - x1), x3, color='orange', alpha=.2)
    ax1.fill_between(x1, x3, color='yellow', alpha=.2)
    ax1.fill_between(x1, x4, 180, color='yellow', alpha=.2)
    ax1.fill_between(-(180 - x1), x4, 180, color='orange', alpha=.2)
    
    # Plot diagonal lines with a single call
    ax1.plot(x1, -(180 - x1), color='#98ceff', zorder=6, linewidth=2, label='NO DIP SEPARATION')
    ax1.plot(x2, x2, color='#98ceff', zorder=6, linewidth=2)
    
    # Add legend with reduced calls
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), shadow=True, ncol=5, frameon=False, fontsize="small")
    
    # Draw vertical lines at specific x-coordinates using a loop
    xcoords = [10, 45, 80, 100, 135, 170, 190, 225, 260, 280, 315, 350]
    for xc in xcoords:
        ax1.axvline(x=xc, c='black', linewidth=0.2)
    
    # Add text annotations with reduced calls
    text_annotations = [
        (2, 97, 'Left-lateral', 90),
        (25, 97, 'Left-lateral normal', 90),
        (60, 97, 'Normal left-lateral', 90),
        (87, 97, 'Normal', 90),
        (115, 20, 'Normal right-lateral', 90),
        (150, 20, 'Right-lateral normal', 90),
        (172, 46, 'Right-lateral', 90),
        (182, 97, 'Right-lateral', 90),
        (205, 97, 'Right-lateral reverse', 90),
        (240, 97, 'Reverse right-lateral', 90),
        (267, 97, 'Reverse', 90),
        (295, 22, 'Reverse left-lateral', 90),
        (330, 22, 'Left-lateral reverse', 90),
        (352, 51, 'Left-lateral', 90)
    ]
    
    for x, y, text, rotation in text_annotations:
        ax1.text(x, y, text, size='small', rotation=rotation)
    
    # Set axis labels
    plt.ylabel("Pitch of the cut-off lines", size='large')
    plt.xlabel("Pitch of the net-slip", size='large')
    
    # Plot the data points
    plt.plot(net_slip, cutoff, 'o', zorder=7)
    
    # Show the plot
    plt.show()
    
    # Save the figure as png (optional)
    fig.savefig('dip_separation.png', transparent=True)

def plot_strike_separation(fault: Tuple[Union[int, float], Union[int, float]], 
                           bedding: Tuple[Union[int, float], Union[int, float]], 
                           net_slip: Union[int, float]):
    """
    Plotting function to visualize strike separation relationships based on fault and bedding orientations.

    Args:
    - fault: Angle of the fault plane (degrees).
    - bedding: Angle of the bedding plane (degrees).
    - net_slip: Amount of net slip on the fault.

    Returns:
    - None (displays a plot).

    This function generates a plot that shows different strike separation relationships 
    based on the given fault and bedding orientations and the net slip.

    Note: Requires matplotlib and numpy libraries.
    """
    
    # Calculate cutoff pitch based on fault and bedding angles
    cutoff = cutoff_pitch(fault, bedding)
    
    # Create the plot
    fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(8, 6))
    ax1.set_aspect('equal', adjustable='box')  # Set aspect ratio
    
    # Customize ticks and secondary x-axis
    plt.xticks([10, 45, 80, 100, 135, 170, 190, 225, 260, 280, 315, 350])
    plt.yticks(np.arange(0, 190, 45))
    secax = ax1.secondary_xaxis('top')
    secax.set_xticks([0, 90, 180, 270, 360])
    
    # Set limits and draw reference lines
    plt.xlim(0, 360)
    plt.ylim(0, 180)
    plt.axhline(90, color="black", linestyle='dashed')
    plt.axvline(180, color="black", linestyle='dashed')
    
    # Define x coordinates for filling areas using numpy arrays
    x1 = np.arange(180, 370, 10)
    x2 = np.arange(0, 190, 10)
    
    # Fill areas with different colors using numpy functions
    ax1.fill_between(-(180 - x1), x2, color='orange', alpha=.2)
    ax1.fill_between(x1, x2, color='yellow', alpha=.2, label='LEFT STRIKE SEPARATION')
    ax1.fill_between(x1, x2, np.max(x2), color='orange', alpha=.2, label='RIGHT STRIKE SEPARATION')
    ax1.fill_between(-(180 - x1), x2, np.max(x2), color='yellow', alpha=.2)
    
    # Plot diagonal lines with a single call
    ax1.plot(x1, -(180 - x1), color='#98ceff', zorder=6, linewidth=2, label='NO STRIKE SEPARATION')
    ax1.plot(x2, x2, color='#98ceff', zorder=6, linewidth=2)
    
    # Add legend with reduced calls
    ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.16), shadow=True, ncol=5, frameon=False, fontsize="small")
    
    # Draw vertical lines at specific x-coordinates using a loop
    xcoords = [10, 45, 80, 100, 135, 170, 190, 225, 260, 280, 315, 350]
    for xc in xcoords:
        ax1.axvline(x=xc, c='black', linewidth=0.2)
    
    # Add text annotations with reduced calls
    text_annotations = [
        (2, 97, 'Left-lateral', 90),
        (25, 97, 'Left-lateral normal', 90),
        (60, 97, 'Normal left-lateral', 90),
        (87, 97, 'Normal', 90),
        (115, 20, 'Normal right-lateral', 90),
        (150, 20, 'Right-lateral normal', 90),
        (172, 46, 'Right-lateral', 90),
        (182, 97, 'Right-lateral', 90),
        (205, 97, 'Right-lateral reverse', 90),
        (240, 97, 'Reverse right-lateral', 90),
        (267, 97, 'Reverse', 90),
        (295, 22, 'Reverse left-lateral', 90),
        (330, 22, 'Left-lateral reverse', 90),
        (352, 51, 'Left-lateral', 90)
    ]
    
    for x, y, text, rotation in text_annotations:
        ax1.text(x, y, text, size='small', rotation=rotation)
    
    # Set axis labels
    plt.ylabel("Pitch of the cut-off lines", size="large")
    plt.xlabel("Pitch of the net-slip", size="large")
    
    # Plot the data points
    plt.plot(net_slip, cutoff, 'o', zorder=7)
    
    # Show the plot
    plt.show()
    
    # Save the figure as png (optional)
    fig.savefig('strike_separation.png', transparent=True)
    
def plot_folds(net_slip: Union[int, float], 
               cutoff: Union[int, float]):
    """
    Plotting function to visualize fold relationships based on net slip and cutoff values.

    Args:
    - net_slip: Pitch of the net slip.
    - cutoff: Pitch of axial plane cut-off line.

    Returns:
    - None (displays a plot).

    This function generates a plot that shows different fold relationships 
    based on the net slip and cutoff values.

    Note: Requires matplotlib and numpy libraries.
    """
    
    # Create the plot
    fig, ax1 = plt.subplots(1, 1, sharex=True, figsize=(8, 6))
    ax1.set_aspect('equal', adjustable='box')  # Set aspect ratio
    
    # Customize ticks and secondary x-axis
    plt.xticks([10, 45, 80, 100, 135, 170, 190, 225, 260, 280, 315, 350])
    plt.yticks(np.arange(0, 190, 45))
    secax = ax1.secondary_xaxis('top')
    secax.set_xticks([0, 90, 180, 270, 360])
    
    # Set limits and draw reference lines
    plt.xlim(0, 360)
    plt.ylim(0, 180)
    plt.axhline(90, color="black", linestyle='dashed')
    plt.axvline(180, color="black", linestyle='dashed')
    
    # Define x coordinates for filling areas using numpy arrays
    x1 = np.arange(180, 370, 10)
    x2 = np.arange(0, 190, 10)
    
    # Plot diagonal lines with a single call
    ax1.plot(x1, -(180 - x1), color='#98ceff', zorder=6, linewidth=2, label='CONSTANT FAULT CHARACTER')
    ax1.plot(x2, x2, color='#98ceff', zorder=6, linewidth=2)
    
    # Fill areas with different colors using numpy functions
    ax1.fill_between(x1, 360, color='yellow', alpha=.2, label='ALTERNATION OF APPARENTLY REVERSE AND NORMAL FAULT SEGMENTS')
    ax1.fill_between(x2, 360, color='yellow', alpha=.2)
    
    # Add legend with reduced calls
    ax1.legend(loc='upper center', bbox_to_anchor=(0.46, -0.16), shadow=True, ncol=5, frameon=False, fontsize="small")
    
    # Draw vertical lines at specific x-coordinates using a loop
    xcoords = [10, 45, 80, 100, 135, 170, 190, 225, 260, 280, 315, 350]
    for xc in xcoords:
        ax1.axvline(x=xc, c='black', linewidth=0.2)
    
    # Add text annotations with reduced calls
    text_annotations = [
        (2, 97, 'Left-lateral', 90),
        (25, 97, 'Left-lateral normal', 90),
        (60, 97, 'Normal left-lateral', 90),
        (87, 97, 'Normal', 90),
        (115, 20, 'Normal right-lateral', 90),
        (150, 20, 'Right-lateral normal', 90),
        (172, 46, 'Right-lateral', 90),
        (182, 97, 'Right-lateral', 90),
        (205, 97, 'Right-lateral reverse', 90),
        (240, 97, 'Reverse right-lateral', 90),
        (267, 97, 'Reverse', 90),
        (295, 22, 'Reverse left-lateral', 90),
        (330, 22, 'Left-lateral reverse', 90),
        (352, 51, 'Left-lateral', 90)
    ]
    
    for x, y, text, rotation in text_annotations:
        ax1.text(x, y, text, size='small', rotation=rotation)
    
    # Set axis labels
    plt.ylabel("Pitch of axial plane cut-off line", size="large")
    plt.xlabel("Pitch of the net-slip", size="large")
    
    # Plot the data points
    plt.plot(net_slip, cutoff, 'o', zorder=7)
    
    # Show the plot
    plt.show()
    
    # Save the figure as png (optional)
    fig.savefig('folds.png', transparent=True)

def cutoff_pitch(fault: Tuple[Union[int, float], Union[int, float]], 
                 bedding: Tuple[Union[int, float], Union[int, float]]):
    """
    Calculates the pitch angle of the cutoff line on the fault plane.

    Args:
    - fault: Tuple containing (strike, dip) of the fault plane in degrees.
    - bedding: Tuple containing (strike, dip) of the bedding plane in degrees.

    Returns:
    - beta: Pitch angle of the cutoff line on the fault plane in degrees.
    """

    # Calculate the intersection line between fault plane and bedding plane
    cutoff_line = mplstereonet.plane_intersection(fault[1] - 90, fault[0], bedding[1] - 90, bedding[0])

    # Calculate the rake of the cutoff line on the fault plane
    cutoff_rake = mplstereonet.azimuth2rake(fault[1] - 90, fault[0], cutoff_line[1])

    # Adjust beta to be within [0, 180) degrees
    if cutoff_rake < 0:
        beta = 180 + cutoff_rake
    else:
        beta = cutoff_rake

    return beta
    
def plot_fault_plane(fault: Tuple[Union[int, float], Union[int, float]], 
                     bedding: Tuple[Union[int, float], Union[int, float]], 
                     net_slip_rake: Union[int, float]):
    """
    Plot the fault plane and its associated cut-off lines based on the given parameters.

    Args:
    - fault: Tuple containing (strike, dip) of the fault plane in degrees.
    - bedding: Tuple containing (strike, dip) of the bedding plane in degrees.
    - net_slip_rake: Rake angle (direction) of the net slip in degrees.

    Returns:
    - None (displays a plot).

    This function generates a plot showing the fault plane and its cut-off lines 
    (FW and HW) based on the provided orientation and net slip direction.

    Note: Requires matplotlib and numpy libraries.
    """

    # Calculate the pitch angle of the cutoff line on the fault plane
    beta = cutoff_pitch(fault, bedding)
    tan_beta = math.tan(math.radians(beta))

    # Determine unit vector of the cutoff line on the bedding plane
    if 0 <= beta < 90:
        v_cutoff = [1, -tan_beta]
    elif 90 < beta <= 180:
        v_cutoff = [-1, tan_beta]

    v = np.array(v_cutoff)
    uv_cutoff = v / np.linalg.norm(v)  # Unit vector of cutoff line direction

    # Calculate the tangent of the net slip direction angle
    tan_alfa = math.tan(math.radians(net_slip_rake))

    # Determine unit vector of the net slip direction
    if 0 <= net_slip_rake < 90:
        v_netslip = [1, -tan_alfa]
    elif 90 < net_slip_rake < 180:
        v_netslip = [-1, tan_alfa]
    elif 180 <= net_slip_rake < 270:
        v_netslip = [-1, tan_alfa]
    elif 270 < net_slip_rake <= 360:
        v_netslip = [1, -tan_alfa]
    elif net_slip_rake == 90:
        v_netslip = [0, -1]
    elif net_slip_rake == 270:
        v_netslip = [0, 1]

    vector = np.array(v_netslip)
    unit_vector = vector / np.linalg.norm(vector)  # Unit vector of net slip direction

    # Define coordinates for FW (Forward) and HW (Hinterland) cut-off lines
    fw_x = [0, uv_cutoff[0]]
    fw_y = [0, uv_cutoff[1]]

    hw_x = [unit_vector[0], uv_cutoff[0] + unit_vector[0]]
    hw_y = [unit_vector[1], uv_cutoff[1] + unit_vector[1]]

    # Create the plot
    fig, ax = plt.subplots()
    ax.quiver(0, 0, unit_vector[0], unit_vector[1], units='xy', scale=1, color='green')  # Plot net slip direction

    plt.plot(fw_x, [0, 0], color='black', linestyle='dashed')
    plt.plot(fw_x, fw_y, label='FW cut-off line')  # Plot FW cut-off line
    plt.plot(hw_x, [unit_vector[1], unit_vector[1]], color='black', linestyle='dashed')
    plt.plot(hw_x, hw_y, label='HW cut-off line')  # Plot HW cut-off line

    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlim(-3, 3)
    plt.ylim(-3, 3)
    plt.legend()
    plt.show()
    
    # Save the figure as png (optional)
    fig.savefig('fault-plane.png', transparent=True)