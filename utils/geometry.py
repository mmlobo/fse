"""
geometry.py

Module containing geometric calculations for fault and bedding plane analysis.

Project: Fault Slip and Separation Explorer Tool
Author: Marta Magán Lobo
Date: 2022

"""

import math
from typing import List, Tuple, Union
import numpy as np

def normal_vector(plane: Tuple[Union[int, float], Union[int, float]]):
    """
    Calculates the normal vector of a given plane in terms of its direction and angle of dip.

    Args:
       plane (tuple): a tuple of two elements [dip, dip_direction] where.
            dip is the dip angle in degrees and 
            dip_direction is the dip direction in degrees from north.

    Returns:
        np.ndarray: a unit normal vector of the plane.
    """
    # Input validation
    if not (isinstance(plane, (list, tuple)) and len(plane) == 2 and 
            all(isinstance(x, (int, float)) for x in plane)):
        raise ValueError("El parámetro 'plane' debe ser una lista o tupla con dos números (dip, dip_direction).")

    dip, dip_direction = plane

    # Direction vector of the plane
    u = [math.sin(math.radians(dip_direction - 90)), math.cos(math.radians(dip_direction - 90)), 0]
    
    # Dip vector of the plane
    v = [math.sin(math.radians(dip_direction)), math.cos(math.radians(dip_direction)), -math.tan(math.radians(dip))]
    
    # Normal vector of the plane using the cross product of u and v
    n = np.cross(v, u)
    
    # Unit vector
    u_ns = n / np.linalg.norm(n)
    
    return u_ns

def lineEquation3Dto2D (A: List[Union[int, float]],
                        v: List[Union[int, float]],
                        i: List[Union[int, float]],
                        j: List[Union[int, float]],
                        k: List[Union[int, float]]):
    """
    Calculates the 2D line equation parameters (slope and intercept) from a 3D line.

    Args:
        A (list): A point on the 3D line.
        v (list): Direction vector of the 3D line.
        i (list): First basis vector of the 2D plane.
        j (list): Second basis vector of the 2D plane.
        k (list): Normal vector to the 2D plane.

    Returns:
        list: A list containing the slope (m) and intercept (a) of the line in the 2D plane.
    """
    # Validate input dimensions
    if not (len(A) == len(v) == len(i) == len(j) == len(k) == 3):
        raise ValueError("All input vectors must have exactly 3 elements.")
    
    # Projection of point A onto the i and j basis vectors
    a1=np.dot(i,A)
    a2=np.dot(j,A)

    # Vector perpendicular to both k and v (lying in the 2D plane)
    vp=np.cross(k,v)

    # Projection of vp onto the i and j basis vectors
    p1=np.dot(i,vp)
    p2=np.dot(j,vp)

    # Slope of the line in 2D  
    m=p1/p2

    # Intercept of the line in 2D
    a=(a1*p1+a2*p2)/p2

    return [m,a]

def cal_intersection(a1: Union[int, float],
                     b1: Union[int, float],
                     a2: Union[int, float],
                     b2: Union[int, float]):
    """
    Calculates the intersection point of two lines given by their slope-intercept form.

    The lines are represented by the equations:
    y = a1 * x + b1
    y = a2 * x + b2

    Args:
        a1 (float): Slope of the first line.
        b1 (float): Y-intercept of the first line.
        a2 (float): Slope of the second line.
        b2 (float): Y-intercept of the second line.

    Returns:
        tuple: A tuple (x, y) representing the intersection point of the two lines,
               or None if the lines are parallel and do not intersect.
    """
    try:
        # Calculate the x-coordinate of the intersection point
        x = (b2-b1)/(a1-a2)

        # Calculate the y-coordinate of the intersection point
        y = a1*(b2-b1)/(a1-a2) + b1

        return (x,y)
    except ZeroDivisionError:
        # Handle the case where the lines are parallel (a1 == a2)
        print("The lines are parallel and do not intersect.")
        return None
    
def plane_equation (n: List[Union[int, float]],
                    P: List[Union[int, float]]):
    """
    Calculates the coefficients of the plane equation given a normal vector and a point on the plane.

    The plane equation is in the form:
    Ax + By + Cz + D = 0

    Args:
        n (list): Normal vector of the plane [A, B, C].
        P (list): A point on the plane [x0, y0, z0].

    Returns:
        list: A list of coefficients [A, B, C, D] for the plane equation.
    """
    # Validate inputs
    if not (len(n) == len(P) == 3):
        raise ValueError("The normal vector 'n' and point 'P' must both have exactly 3 elements.")
    if not (all(isinstance(coord, (int, float)) for coord in n) and all(isinstance(coord, (int, float)) for coord in P)):
        raise ValueError("All elements of 'n' and 'P' must be numeric values.")
     
    # Calculate the D coefficient using the point P
    D = -n[0] * P[0] - n[1] * P[1] - n[2] * P[2]
    
    # Return the plane equation coefficients [A, B, C, D]
    return [n[0], n[1], n[2], D]

def plane_intersectionMap(P1: List[Union[int, float]],
                       P2: List[Union[int, float]]):
    """
    Calculates the intersection line of two planes given by their general equations.

    The planes are represented by the equations:
    P1: A1*x + B1*y + C1*z + D1 = 0
    P2: A2*x + B2*y + C2*z + D2 = 0

    Args:
        P1 (list): Coefficients [A1, B1, C1, D1] of the first plane equation.
        P2 (list): Coefficients [A2, B2, C2, D2] of the second plane equation.

    Returns:
        list: A list containing the direction vector of the intersection line and a point on the line.
              Format: [direction_vector, point_on_line]
    """
    # Validate inputs
    if not (len(P1) == len(P2) == 4):
        raise ValueError("Both input arrays must have exactly 4 elements.")
    if not (all(isinstance(coord, (int, float)) for coord in P1) and all(isinstance(coord, (int, float)) for coord in P2)):
        raise ValueError("All elements of P1 and P2 must be numeric values.")

    # Normal vector of the first plane
    n1 = [P1[0], P1[1], P1[2]]
    
    # Normal vector of the second plane
    n2 = [P2[0], P2[1], P2[2]]
    
    # Direction vector of the intersection line of P1 and P2
    vr = np.cross(n1, n2)
    
    # Initial point, solving equation system for y=0
    # Equations for y=0:
    # A1*x + C1*z + D1 = 0
    # A2*x + C2*z + D2 = 0
    A = np.array([[P1[0], P1[2]], [P2[0], P2[2]]])
    B = np.array([P1[3], P2[3]])

    if np.linalg.det(A) == 0:
        # If the determinant is zero, the system cannot be solved (planes are parallel or coincident)
        print("The system of equations cannot be solved, planes may be parallel or coincident.")
        X = None
    else:
        # Solve the system of equations
        X = np.linalg.inv(A).dot(B)
    
    Pp = [X[0], 0, X[1]]
    return [vr, Pp]

def plane_intersectionSection(P1: List[Union[int, float]],
                              P2: List[Union[int, float]]):
    """
    Calculates the intersection line between a given plane and  by their general equations.

    The planes are represented by the equations:
    P1: A1*x + B1*y + C1*z + D1 = 0
    P2: A2*x + B2*y + C2*z + D2 = 0

    Args:
        P1 (list): Coefficients [A1, B1, C1, D1] of the first plane equation.
        P2 (list): Coefficients [A2, B2, C2, D2] of the second plane equation.

    Returns:
        list: A list containing the direction vector of the intersection line and a point on the line.
              Format: [direction_vector, point_on_line]
    """
    # Validate inputs
    if not (len(P1) == len(P2) == 4):
        raise ValueError("Both input arrays must have exactly 4 elements.")
    if not (all(isinstance(coord, (int, float)) for coord in P1) and all(isinstance(coord, (int, float)) for coord in P2)):
        raise ValueError("All elements of P1 and P2 must be numeric values.")

    # Normal vector of the first plane
    n1 = [P1[0], P1[1], P1[2]]
    
    # Normal vector of the second plane
    n2 = [P2[0], P2[1], P2[2]]
    
    # Direction vector of the intersection line of P1 and P2
    vr = np.cross(n1, n2)
    
    # Initial point, solving equation system for z=0
    # Equations for y=0:
    # A1*x + C1*z + D1 = 0
    # A2*x + C2*z + D2 = 0
    A = np.array([[P1[0], P1[1]], [P2[0], P2[1]]])
    B = np.array([P1[3], P2[3]])

    if np.linalg.det(A) == 0:
        # If the determinant is zero, the system cannot be solved (planes are parallel or coincident)
        print("The system of equations cannot be solved, planes may be parallel or coincident.")
        X = None
    else:
        # Solve the system of equations
        X = np.linalg.inv(A).dot(B)
    
    Pp = [X[0], X[1], 0]
    return [vr, Pp]

def apply_netslip(P: List[Union[int, float]],
                  v: List[Union[int, float]],
                  a: Union[int, float]):
    """
    Applies the net slip to a point P based on a direction vector v and a scalar magnitude a.

    Args:
        P (list): The original point coordinates.
        v (list): The direction vector of the net-slip.
        a (int / float): The magnitude of the net-slip.

    Returns:
        np.ndarray: The new coordinates of the point after applying the slip.
    """
    # Validate inputs
    if not isinstance(a, (int, float)):
        raise ValueError("The magnitude 'a' must be a numeric value.")
    if not (len(P) == len(v)):
        raise ValueError("The point 'P' and direction vector 'v' must have the same length.")
    
    # Convert the direction vector v to a numpy array
    u=np.array(v)

    # Calculate the displacement by scaling the direction vector by the magnitude a
    displacement = a * u
    
    # Add the displacement to the original point P to get the new point
    new_point = np.add(P, displacement)
    
    return new_point