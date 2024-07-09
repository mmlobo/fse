import math
from typing import Tuple, Union
import mplstereonet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils.geometry import cal_intersection, normal_vector, lineEquation3Dto2D, plane_equation, plane_intersectionMap, plane_intersectionSection, apply_netslip


def section_map(fault: Tuple[Union[int, float], Union[int, float]], 
                bedding: Tuple[Union[int, float], Union[int, float]], 
                net_slip_rake: Union[int, float], 
                net_slip_value: Union[int, float]):
    """
    Plots the map and cross-section of the intersection between a fault and bedding plane with given net slip parameters.

    Args:
        fault (tuple): Fault plane parameters [dip, dip direction].
        bedding (tuple): Bedding plane parameters [dip, dip direction].
        net_slip_rake (float): Rake of the net slip.
        net_slip_value (float): Magnitude of the net slip.

    Returns:
        None
    """
    # Avoid infinite values
    if bedding[1] == 90:
        bedding[1] = 90.00001
    if fault[1] == 90:
        fault[1] = 90.00001

    # Origin
    O = [0, 0, 0]

    # Normal vector of fault plane
    nf = normal_vector(fault)

    # Normal vector of bedding plane
    nb = normal_vector(bedding)

    # Adjust rake if necessary
    if net_slip_rake >= 180 and net_slip_rake < 360:
        rake = (net_slip_rake - 180)
    else:
        rake = net_slip_rake

    # Calculate net slip vector
    lon, lat = mplstereonet.rake(fault[1] - 90, fault[0], rake)
    pb_netslip = mplstereonet.geographic2plunge_bearing(lon, lat)
    netslip = [math.sin(math.radians(pb_netslip[1])), math.cos(math.radians(pb_netslip[1])), -math.tan(math.radians(pb_netslip[0]))]

    # Unit vector in the direction of the net slip
    v = np.array(netslip)
    if net_slip_rake >= 180:
        v = -v
    u_ns = v / np.linalg.norm(v)

    # Normal vector of a plane orthogonal to the fault plane
    ns = [math.sin(math.radians(fault[1] - 90)), math.cos(math.radians(fault[1] - 90)), 0]

    # Fault plane equation
    pf = plane_equation(nf, O)
    # Bedding plane equation on the footwall
    pfw = plane_equation(nb, O)

    # Apply net-slip
    new_O = apply_netslip(O, u_ns, -net_slip_value)

    # Bedding plane equation on the hangingwall
    phw = plane_equation(nb, new_O)

    # Plane equation of the section
    ps = plane_equation(ns, O)

    # Intersection with the section
    IF = plane_intersectionSection(pf, ps)
    IFW = plane_intersectionSection(pfw, ps)
    IHW = plane_intersectionSection(phw, ps)

    # Change the reference system from 3D to 2D
    j = [0, 0, 1]
    k = ns
    i = np.cross(j, k)
    rf = lineEquation3Dto2D(IF[1], IF[0], i, j, k)
    rfw = lineEquation3Dto2D(IFW[1], IFW[0], i, j, k)      
    rhw = lineEquation3Dto2D(IHW[1], IHW[0], i, j, k)

    # Intersection points between fault and bedding on the footwall and hangingwall
    fw = cal_intersection(rf[0], rf[1], rfw[0], rfw[1])
    hw = cal_intersection(rf[0], rf[1], rhw[0], rhw[1])

    # x, y values to plot in section
    xf = np.arange(-20, 20, 1)
    xfw = np.arange(-20, fw[0] + 1, 1)
    xhw = np.arange(hw[0], 20, 1)

    yf = rf[0] * xf + rf[1]
    yfw = rfw[0] * xfw + rfw[1]
    yhw = rhw[0] * xhw + rhw[1]

    # Normal vector to horizontal plane (map)
    uf = [0, 0, 1]
    ph = plane_equation(uf, O)

    # Intersection with map
    HIF = plane_intersectionMap(pf, ph)
    HIFW = plane_intersectionMap(pfw, ph)
    HIHW = plane_intersectionMap(phw, ph)

    # Change the reference system from 3D to 2D
    j = [0, 1, 0]
    k = [0, 0, 1]
    i = [1, 0, 0]
    rfm = lineEquation3Dto2D(HIF[1], HIF[0], i, j, k)
    rfwm = lineEquation3Dto2D(HIFW[1], HIFW[0], i, j, k)
    rhwm = lineEquation3Dto2D(HIHW[1], HIHW[0], i, j, k)

    # Intersection points between fault and bedding on the footwall and hangingwall in map
    fwm = cal_intersection(-rfm[0], rfm[1], -rfwm[0], rfwm[1])
    hwm = cal_intersection(-rfm[0], rfm[1], -rhwm[0], rhwm[1])

    # Normal vector of fault plane in 2D
    x = np.dot(i, nf)
    y = np.dot(j, nf)

    # x, y values to plot in section and map
    xfm = np.arange(-50, 50, 1)
    xfwm = np.arange(-50, 50, 1)
    xhwm = np.arange(-50, 50, 1)

    yfm = -rfm[0] * xfm + rfm[1]
    yfwm = -rfwm[0] * xfwm + rfwm[1]
    yhwm = -rhwm[0] * xhwm + rhwm[1]

    # For plotting block segments in map
    vfw = np.vstack((xfwm, yfwm)).T
    vhw = np.vstack((xhwm, yhwm)).T

    df_fw = pd.DataFrame(vfw)
    df_hw = pd.DataFrame(vhw)

    print(f"Dip separation: {round(math.dist(fw, hw), 2)}")
    print(f"Strike separation: {round(math.dist(fwm, hwm), 2)}")

    bed = bedding[1]
    if bed > 180:
        bed = bed - 180
    f = fault[1]
    if f > 180:
        f = f - 180

    # Filter segments based on bedding and fault angles
    if x > 0:
        if bed == 0:
            df_fw = df_fw.drop(df_fw[df_fw[1] < 0].index)
            df_hw = df_hw.drop(df_hw[df_hw[0] < hwm[0]].index)
        elif bed == 180:
            df_fw = df_fw.drop(df_fw[df_fw[1] > 0].index)
            df_hw = df_hw.drop(df_hw[df_hw[0] < hwm[0]].index)
        elif bed < f:
            df_fw = df_fw.drop(df_fw[df_fw[1] < 0].index)
            df_hw = df_hw.drop(df_hw[df_hw[1] > hwm[1]].index)
        elif bed > f:
            df_fw = df_fw.drop(df_fw[df_fw[1] > 0].index)
            df_hw = df_hw.drop(df_hw[df_hw[1] < hwm[1]].index)       
    elif x < 0:
        if bed == 0:
            df_fw = df_fw.drop(df_fw[df_fw[1] > 0].index)
            df_hw = df_hw.drop(df_hw[df_hw[0] > hwm[0]].index)
        elif bed == 180:
            df_fw = df_fw.drop(df_fw[df_fw[1] < 0].index)
            df_hw = df_hw.drop(df_hw[df_hw[0] > hwm[0]].index)
        elif bed < f:
            df_fw = df_fw.drop(df_fw[df_fw[1] > 0].index)
            df_hw = df_hw.drop(df_hw[df_hw[1] < hwm[1]].index)         
        elif bed > f:  
            df_fw = df_fw.drop(df_fw[df_fw[1] < 0].index)
            df_hw = df_hw.drop(df_hw[df_hw[1] > hwm[1]].index)

    fwm_aux = df_fw.to_numpy()
    b, c = np.split(fwm_aux, 2, axis=1)

    hwm_aux = df_hw.to_numpy()
    d, e = np.split(hwm_aux, 2, axis=1)

    # Plot section and map
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1.set_aspect('equal', adjustable='box')
    if fault[1] == 90.00001:
        fault[1] = 90
    ax1.text(0, rf[0] * (-15) + rf[1], str(fault[1]) + '\u2192', size='large')

    ax1.plot(xf, yf, color='#ff0004')
    ax1.plot(xfw, yfw, color='#0100ff')
    ax1.plot(xhw, yhw, color='#0100ff')
    ax1.scatter(hw[0], hw[1], marker='.', color='#0100ff', label='point')

    ax2.set_aspect('equal', adjustable='box')
    if bedding[1] >= 270 or 90 < bedding[1] <= 180:
        ax2.text(-50, 40, 'N \u2191', size='x-large')
    else:
        ax2.text(40, 40, 'N \u2191', size='x-large')
    ax2.text(10, -10, '\u251c', size='x-large', rotation=-bedding[1] + 90)

    ax2.plot(xfm, yfm, color='#ff0004')
    ax2.plot(b, c, color='#0100ff')
    ax2.plot(d, e, color='#0100ff')

    ax2.quiver(0, 0, 10 * x, 10 * y, units='xy', scale=1, color='#ff0004')
    ax2.scatter(hwm[0], hwm[1], marker='.', color='#0100ff', label='point')

    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)  

    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)

    # Show the plot
    plt.show()

    fig.savefig('map-section.png', transparent=True)