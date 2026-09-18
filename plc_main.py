#Sample command: sudo python3 plc1_main.py

from real_plc import plc1, plc2, plc3, plc4, plc5, plc6
import sys,os
sys.path.insert(0,os.getcwd())
# from SCADA import H
from IO import *
import numpy as np
from trace_check.get_data import get_all_input_with_sensors
from trace_check.get_data import get_waterlevels
from trace_check.get_data import get_full_log
from trace_check.get_data import print_all_output
import csv
from datetime import datetime
import os
import shutil
import time
from threading import Thread
from utils import PLC1_DATA, PLC1_PROTOCOL, PLC1_ADDR, PLC2_PROTOCOL, PLC2_ADDR, PLC2_DATA, PLC3_PROTOCOL, PLC3_ADDR, PLC3_DATA, PLC4_PROTOCOL, PLC4_ADDR, PLC4_DATA, PLC5_PROTOCOL, PLC5_ADDR, PLC5_DATA, PLC6_PROTOCOL, PLC6_ADDR, PLC6_DATA
####################################################################



########## TBD: HMI logging should be moved to SCADA ###########

# Logging step-wise status of plant
# timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# log_filename = os.path.join(f'logs_{timestamp}.csv')
# headers = [
#     "Timestamp","HMI.P1.State","HMI.LIT101.Pv","HMI.LIT301.Pv","HMI.P2.State","HMI.P3.State","HMI.P4.State","HMI.P5.State","HMI.P6.State",
#     "HMI.P101.Status","HMI.P102.Status","HMI.MV101.Status","HMI.MV201.Status","HMI.FIT101.Pv","HMI.LS201.Alarm","HMI.LS202.Alarm",
#     "HMI.LSL203.Alarm","HMI.LSLL203.Alarm","HMI.P201.Status","HMI.P202.Status","HMI.P203.Status","HMI.P204.Status","HMI.P205.Status",
#     "HMI.P206.Status","HMI.P207.Status","HMI.P208.Status","HMI.FIT201.Pv","HMI.AIT201.Pv","HMI.AIT202.Pv","HMI.AIT203.Pv",
#     "HMI.P301.Status","HMI.P302.Status","HMI.FIT301.Pv","HMI.PSH301.Alarm","HMI.DPSH301.Alarm","HMI.DPIT301.Pv","HMI.MV301.Status",
#     "HMI.MV302.Status","HMI.MV303.Status","HMI.MV304.Status","HMI.LS401.Alarm","HMI.LIT401.Pv","HMI.P401.Status","HMI.P402.Status",
#     "HMI.P403.Status","HMI.P404.Status","HMI.UV401.Status","HMI.AIT401.Pv","HMI.AIT402.Pv","HMI.FIT401.Pv","HMI.AIT501.Pv","HMI.AIT502.Pv",
#     "HMI.AIT503.Pv","HMI.AIT504.Pv","HMI.FIT501.Pv","HMI.FIT502.Pv","HMI.FIT503.Pv","HMI.FIT504.Pv","HMI.MV501.Status","HMI.MV502.Status",
#     "HMI.MV503.Status","HMI.MV504.Status","HMI.P501.Status","HMI.P502.Status","HMI.LSL601.Alarm","HMI.LSL602.Alarm","HMI.LSL603.Alarm",
#     "HMI.LSH601.Alarm","HMI.LSH602.Alarm","HMI.LSH603.Alarm","HMI.P601.Status","HMI.P602.Status","HMI.P603.Status",
#     "P1.MV101.DO_Open","P1.MV101.DO_Close","P1.P101.DO_Start","P1.P102.DO_Start","P2.MV201.DO_Open","P2.MV201.DO_Close",
#     "P2.P201.DO_Start","P2.P202.DO_Start","P2.P203.DO_Start","P2.P204.DO_Start","P2.P205.DO_Start","P2.P206.DO_Start",
#     "P3.MV301.DO_Open","P3.MV301.DO_Close","P3.MV302.DO_Open","P3.MV302.DO_Close","P3.MV303.DO_Open","P3.MV303.DO_Close",
#     "P3.MV304.DO_Open","P3.MV304.DO_Close","P3.P301.DO_Start","P3.P302.DO_Start","P4.P401.DO_Start","P4.P402.DO_Start",
#     "P4.P403.DO_Start","P4.P404.DO_Start","P4.UV401.DO_Start","P5.MV501.DO_Open","P5.MV501.DO_Close","P5.MV502.DO_Open",
#     "P5.MV502.DO_Close","P5.MV503.DO_Open","P5.MV503.DO_Close","P5.MV504.DO_Open","P5.MV504.DO_Close","P6.P601.DO_Start",
#     "P6.P602.DO_Start"
# ]
#
# for filename in os.listdir('.'):
#     if filename.startswith('logs') and os.path.isfile(filename):
#         os.makedirs('archive', exist_ok=True)
#         dest_path = os.path.join('archive', filename)
#         shutil.move(filename, dest_path)
#         print(f"Moved {filename} to {dest_path}")
#
# try:
#     with open(log_filename, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(headers)
# except Exception as e:
#     print(f"Error preparing log file: {e}")

###########################################################################################
############################################################################################

# Initiating Plant
# Plant = plant(time_interval,maxstep)
# Defining I/O
IO_P1 = P1()
IO_P2 = P2()
IO_P3 = P3()
IO_P4 = P4()
IO_P5 = P5()
IO_P6 = P6()


if __name__ == "__main__":
    print ("Initializing PLCs\n")
    PLC1 = plc1.plc1(name='plc1',
            protocol=PLC1_PROTOCOL,
            memory=PLC1_DATA,
            disk=PLC1_DATA)

    PLC2 = plc2.plc2(name='plc2',
            protocol=PLC2_PROTOCOL,
            memory=PLC2_DATA,
            disk=PLC2_DATA)

    PLC3 = plc3.plc3(name='plc3',
            protocol=PLC3_PROTOCOL,
            memory=PLC3_DATA,
            disk=PLC3_DATA)

    PLC4 = plc4.plc4(name='plc4',
            protocol=PLC4_PROTOCOL,
            memory=PLC4_DATA,
            disk=PLC4_DATA)

    PLC5 = plc5.plc5(name='plc5',
            protocol=PLC5_PROTOCOL,
            memory=PLC5_DATA,
            disk=PLC5_DATA)

    PLC6 = plc6.plc6(name='plc6',
            protocol=PLC6_PROTOCOL,
            memory=PLC6_DATA,
            disk=PLC6_DATA)

    time.sleep(10)

    p1 = Thread(target=PLC1.Pre_Main_Raw_Water, args=(IO_P1,))
    p2 = Thread(target=PLC2.Pre_Main_UF_Feed_Dosing, args=(IO_P2,))
    p3 = Thread(target=PLC3.Pre_Main_UF_Feed, args=(IO_P3,))
    p4 = Thread(target=PLC4.Pre_Main_RO_Feed_Dosing, args=(IO_P4,))
    p5 = Thread(target=PLC5.Pre_Main_High_Pressure_RO, args=(IO_P5,))
    p6 = Thread(target=PLC6.Pre_Main_Product, args=(IO_P6,))

    print("Starting first PLC")
    p1.start()
    print("Starting second PLC")
    p2.start()
    print("Starting third PLC")
    p3.start()
    print("Starting fourth PLC")
    p4.start()
    print("Starting fifth PLC")
    p5.start()
    print("Starting sixth PLC")
    p6.start()
