"""
main.py

Main script to execute the fault slip and separation explorer tool.

This script integrates various functions and modules to analyze and visualize relationships between fault slip
and separation.

Project: Fault Slip and Separation Explorer Tool
Author: Marta Magán Lobo
Date: 2022

For usage instructions and further details, please refer to the README.md file.

"""
from utils.analysis import section_map
from utils.plotting import plot_dip_separation, plot_fault_plane, plot_strike_separation

def main():
    while True:
        try:
            fault_dip = float(input("Enter Fault dip (0-90): "))
            if 0 <= fault_dip <= 90:
                break
            else:
                print("Fault dip must be between 0 and 90. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            fault_dip_direction = float(input("Enter Fault dip direction (0-360): "))
            if 0 <= fault_dip_direction <= 360:
                break
            else:
                print("Fault dip direction must be between 0 and 360. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            bedding_dip = float(input("Enter Bedding dip (0-90): "))
            if 0 <= bedding_dip <= 90:
                break
            else:
                print("Bedding dip must be between 0 and 90. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            bedding_dip_direction = float(input("Enter Bedding dip direction (0-360): "))
            if 0 <= bedding_dip_direction <= 360:
                break
            else:
                print("Bedding dip direction must be between 0 and 360. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            pitch_net_slip = float(input("Enter Pitch net slip (0-360): "))
            if 0 <= pitch_net_slip <= 360:
                break
            else:
                print("Pitch net slip must be between 0 and 360. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    while True:
        try:
            units_net_slip = input("Enter Units net slip (10 by default): ")
            if units_net_slip == "":
                units_net_slip = 10
            else:
                units_net_slip = float(units_net_slip)
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"Fault dip: {fault_dip}")
    print(f"Fault dip direction: {fault_dip_direction}")
    print(f"Bedding dip: {bedding_dip}")
    print(f"Bedding dip direction: {bedding_dip_direction}")
    print(f"Pitch net slip: {pitch_net_slip}")
    print(f"Units net slip: {units_net_slip}")

    fault = (int(fault_dip),int(fault_dip_direction))
    net_slip_rake = int(pitch_net_slip)
    net_slip_value = int(units_net_slip)
    bedding = (int(bedding_dip),int(bedding_dip_direction))

    while True:
        print("\nSelect :")
        print("1. Plot fault plane as in Ragan (2009)")
        print("2. Dip separation plot")
        print("3. Strike separation plot")
        print("4. Section and Map analysis")
        print("5. Exit")

        opcion = input("Select option: ")

        if opcion == "1":
            plot_fault_plane(fault, bedding, net_slip_rake)
        elif opcion == "2":
           plot_dip_separation(fault, bedding, net_slip_rake)
        elif opcion == "3":
            plot_strike_separation(fault, bedding, net_slip_rake)
        elif opcion == "4":
            section_map(fault, bedding, net_slip_rake,net_slip_value)
        elif opcion == "5":
            print("Exit...")
            break
        else:
            print("Invalid option. Please, select options 1 to 5.")
if __name__ == "__main__":
    main()
