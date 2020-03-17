#!/usr/bin/python


import subprocess
import sys
import time
from datetime import datetime
import tarfile
import os
import csv
import CMDModule
import socket



class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



system_kpi_dict = {

'Loadavg1':     ('.1.3.6.1.4.1.2021.10.1.5.1','Numeric'),
'Loadavg5':     ('.1.3.6.1.4.1.2021.10.1.5.2','Numeric'),
'Loadavg15':    ('1.3.6.1.4.1.2021.10.1.5.3','Numeric'),
'CpuUserPerc':  ('1.3.6.1.4.1.2021.11.9.0','Percent'),
'CpuSysPerc':   ('1.3.6.1.4.1.2021.11.10.0','Percent'),
'CpuIdlePerc':  ('1.3.6.1.4.1.2021.11.11.0','Percent'),
'CpuRawUser':   ('1.3.6.1.4.1.2021.11.50.0','Numeric'),
'CpuRawNice':   ('1.3.6.1.4.1.2021.11.51.0','Numeric'),
'CpuRawSystem': ('1.3.6.1.4.1.2021.11.52.0','Numeric'),
'CpuRawIdle':   ('1.3.6.1.4.1.2021.11.53.0','Numeric'),
'memTotalSwap': ('1.3.6.1.4.1.2021.4.3.0','KB'),
'memAvailSwap': ('1.3.6.1.4.1.2021.4.4.0','KB'),
'memTotalReal': ('1.3.6.1.4.1.2021.4.5.0','KB'),
'memUsedReal':  ('1.3.6.1.4.1.2021.4.6.0','KB'),
'memTotalFree': ('1.3.6.1.4.1.2021.4.11.0','KB'),
'memShared':    ('1.3.6.1.4.1.2021.4.13.0','KB'),
'memBuffer':    ('1.3.6.1.4.1.2021.4.14.0','KB'),
'memCached':    ('1.3.6.1.4.1.2021.4.15.0','KB'),
'memSwapError': ('1.3.6.1.4.1.2021.4.100.0','Numeric'),
'sysUpTime':    ('1.3.6.1.2.1.1.3.0','Timestamp')
}


aos_kpi_dict = {

#'Hostname':     ('1.3.6.1.4.1.2603.5.2.6.4.1','STRING'),
'Totalbps':     ('1.3.6.1.4.1.2603.5.4.9.1.5.1000.1.1000.4','bps'),
'Totalpps':     ('1.3.6.1.4.1.2603.5.4.9.1.5.1000.1.1000.3','pps'),
'TotalNoOfConnections': ('1.3.6.1.4.1.2603.5.4.9.1.5.1000.1.1000.6','Numeric'),
'TotalDroppedFrames':   ('1.3.6.1.4.1.2603.5.4.9.1.5.1000.1.1000.11','Numeric'),
'TotalCER':     ('1.3.6.1.4.1.2603.5.5.18.1.3.0.10001','Numeric'),
'SWversion':    ('1.3.6.1.4.1.2603.5.2.6.13','STRING'),
'BoxKeySN':    ('1.3.6.1.4.1.2603.5.2.6.12','STRING')
}

smp_kpi_dict = {
#'Hostname':     ('1.3.6.1.2.1.1.5','STRING'),
'alsmpNumOfActiveSubs': ('1.3.6.1.4.1.2603.11.2.4','Numeric'),
'alsmpNumOfActiveSess': ('1.3.6.1.4.1.2603.11.2.5','Numeric'),
#'alSMPInSdMsg': '1.3.6.1.4.1.2603.11.2.12.1',
#'alSMPInFailedSdMsg':   '1.3.6.1.4.1.2603.11.2.12.11',
#'alSMPOutFailedSdMsg':  '1.3.6.1.4.1.2603.11.2.12.16',
'alSMPInSdMsgPeakRate': ('1.3.6.1.4.1.2603.11.2.12.21','Numeric'),
'alSMPOutSdMsgPeakRate':        ('1.3.6.1.4.1.2603.11.2.12.25','Numeric'),
'SWversion':    ('1.3.6.1.4.1.2603.5.2.6.13','STRING')
}

nic_dict = {
'L1': '100',
'L2':  '101',
'L3':  '102',
'L4':  '103',
'L5':  '104',
'L6':  '105',
'LAG1': '960',
'LAG2': '961',
'LAG3': '962',
'LAG4': '963',
'LAG5': '964',
'LAG6': '965',
'LAG7': '966',
'LAG8': '967'
}

disk_dict = {
'/': '1',
'/opt/' : '2',
'/opt/sybase/data/' : '3'
}

nic_kpi_dict = {

'Txbps': ('1.3.6.1.4.1.2603.5.2.6.3.1.13.<nicIdx>','bps'),
'Rxbps': ('1.3.6.1.4.1.2603.5.2.6.3.1.14.<nicIdx>','bps'),
'Txpps': ('1.3.6.1.4.1.2603.5.2.6.3.1.15.<nicIdx>','pps'),
'Rxpps': ('1.3.6.1.4.1.2603.5.2.6.3.1.16.<nicIdx>','pps'),
#'ifInOctets':    ('1.3.6.1.2.1.2.2.1.10.<nicIdx>','STRING),
#'ifOutOctets':   ('1.3.6.1.2.1.2.2.1.16.<nicIdx>,'STRING'),
'ifDesc':        ('1.3.6.1.2.1.2.2.1.2.<nicIdx>','STRING'),
'ifOperStatus':  ('1.3.6.1.2.1.2.2.1.8.<nicIdx>','STRING')
}

disk_kpi_dict = {
'dskPath':       ('1.3.6.1.4.1.2021.9.1.2.<diskIdx>','STRING'),
'dskTotal':      ('1.3.6.1.4.1.2021.9.1.6.<diskIdx>','KB'),
'dskAvail':      ('1.3.6.1.4.1.2021.9.1.7.<diskIdx>','KB'),
'dskUsed':       ('1.3.6.1.4.1.2021.9.1.8.<diskIdx>','KB'),
'dskPercent':    ('1.3.6.1.4.1.2021.9.1.9.<diskIdx>','Percent')
}



global value_type
global kpi_value
global kpi
global kpi_timestamp
global ip
global hostname
global kpi_value



today = time.strftime("%Y%m%d_%H%M%S")


def clean_output(s):
    out = s.replace("\n", " ").replace("kB", " ").replace(".rmn.local", " ")
    return out

def create_csv(header,fname):
    with open(fname, 'wb') as csvfile:
        print fname
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
    return fname




def add_row_to_csv(csv_file, row):
    today = (time.strftime("%d-%m-%Y"))
    newRow = row
    with open(csv_file, 'ab') as fd:
        writer = csv.writer(fd)
        writer.writerow(newRow)




def fill_system_kpi(cmd_instance,csv_file):
    kpi_timestamp = time.strftime("%Y-%m-%d_%H:%M:%S")



    #AOS

    for ip in cmd_instance.aos_group:
        command = "snmpwalk -v 2c -c v1v2Config %s %s"%(ip,'1.3.6.1.4.1.2603.5.2.6.4.1')
        hostname = cmd_instance.get_stdout_cmd(command).split(': ')[1].replace("\"", " ").partition('.')[0].strip()
        if('sgve0' in hostname):
                component = 'SGVE'
        else:
                component = 'SG9700'


        for kpi, oid in aos_kpi_dict.items():
            command = "snmpwalk -v 2c -c v1v2Config %s %s" % (ip, oid[0])
            kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
            if ("error" in kpi_out):
                print(command)

            try:
                kpi_value = kpi_out.split(': ')[1]
            except:
                kpi_value = 'N/A'


            try:
                value_type = oid[1]
            except:
                value_type = 'ERROR'

            new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
            add_row_to_csv(csv_file,new_row)


        for kpi, oid in system_kpi_dict.items():
            command = "snmpwalk -v 2c -c v1v2Config %s %s" % (ip, oid[0])
            kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
            if ("error" in kpi_out):
                print(command)

            try:
                kpi_value = kpi_out.split(': ')[1]
            except:
                kpi_value = 'N/A'


            try:
                value_type = oid[1]
            except:
                value_type = 'ERROR'



            new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
            add_row_to_csv(csv_file, new_row)



        for kpi, oid in nic_kpi_dict.items():
            for nic,nicidx in nic_dict.items():
                new_oid = oid[0].replace("<nicIdx>", nicidx)
                command = "snmpwalk -v 2c -c v1v2Config %s %s" % (ip, new_oid)
                kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))

                try:
                   kpi_value = kpi_out.split(': ')[1]
                except:
                    kpi_value = 'N/A'

                try:
                    value_type = oid[1]
                except:
                    value_type = 'ERROR'


                new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), (kpi+nic).strip(), kpi_value.strip(), value_type.strip()]
                add_row_to_csv(csv_file, new_row)


        for kpi, oid in disk_kpi_dict.items():
            for disk,diskidx in disk_dict.items():
                new_oid = oid[0].replace("<diskIdx>", diskidx)
                command = "snmpwalk -v 2c -c v1v2Config %s %s" % (ip, new_oid)
                kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))

                try:
                    kpi_value = kpi_out.split(': ')[1]
                except:
                    kpi_value = 'N/A'


                try:
                    value_type = oid[1]
                except:
                    value_type = 'ERROR'


                new_kpi = kpi.strip() + '_' + disk

                if(kpi_value == 'N/A'):
                        continue

                new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), new_kpi.strip(), kpi_value.strip(), value_type.strip()]
                add_row_to_csv(csv_file, new_row)





    # BI

    for ip in cmd_instance.bi_group:
        command = "snmpwalk -v 3 -u MD5 -a MD5 -A MD5UserAuthPassword12 -l authNoPriv %s %s" % (ip, '.1.3.6.1.2.1.1.5')

        try:
            hostname = cmd_instance.get_stdout_cmd(command).split(': ')[1].replace("\"", " ").partition('.')[0].strip()

        except:
            hostname = 'N/A'

        component = 'BI'
        for kpi, oid in system_kpi_dict.items():
            command = "snmpwalk -v 3 -u MD5 -a MD5 -A MD5UserAuthPassword12 -l authNoPriv %s %s" % (ip, oid[0])
            kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
            if ("error" in kpi_out):
                print(command)
            try:
                kpi_value = kpi_out.split(': ')[1]
            except:
                kpi_value = 'N/A'

            try:
                value_type = oid[1]
            except:
                value_type = 'ERROR'



            new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
            add_row_to_csv(csv_file, new_row)



        for kpi, oid in disk_kpi_dict.items():
            for disk, diskidx in disk_dict.items():
                new_oid = oid[0].replace("<diskIdx>", diskidx)
                command = "snmpwalk -v 3 -u MD5 -a MD5 -A MD5UserAuthPassword12 -l authNoPriv %s %s" % (ip, new_oid)
                kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))

                try:
                    kpi_value = kpi_out.split(': ')[1]
                except:
                    kpi_value = 'N/A'

                try:
                    value_type = oid[1]
                except:
                    value_type = 'ERROR'

                new_kpi = kpi.strip() + '_' + disk

                if(kpi_value == 'N/A'):
                    continue

                new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), new_kpi.strip(), kpi_value.strip(), value_type.strip()]
                add_row_to_csv(csv_file, new_row)



    # DWH

    for ip in cmd_instance.dwh_group:
        command = "snmpwalk -v 3 -u MD5 -a MD5 -A MD5UserAuthPassword12 -l authNoPriv %s %s" % (ip, '.1.3.6.1.2.1.1.5')
        try:
            hostname = cmd_instance.get_stdout_cmd(command).split(': ')[1].replace("\"", " ").partition('.')[0].strip()

        except:
            hostname = 'N/A'

        component = 'DWH'
        for kpi, oid in system_kpi_dict.items():
            command = "snmpwalk -v 3 -u MD5 -a MD5 -A MD5UserAuthPassword12 -l authNoPriv %s %s" % (ip, oid[0])
            kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
            if ("error" in kpi_out):
                print(command)
            try:
                kpi_value = kpi_out.split(': ')[1]
            except:
                kpi_value = 'N/A'

            try:
                value_type = oid[1]
            except:
                value_type = 'ERROR'



            new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
            add_row_to_csv(csv_file, new_row)



        for kpi, oid in disk_kpi_dict.items():
            for disk, diskidx in disk_dict.items():
                new_oid = oid[0].replace("<diskIdx>", diskidx)
                command = "snmpwalk -v 3 -u MD5 -a MD5 -A MD5UserAuthPassword12 -l authNoPriv %s %s" % (ip, new_oid)
                kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
                print(command)
                try:
                    kpi_value = kpi_out.split(': ')[1]
                except:
                    kpi_value = 'N/A'

                try:
                    value_type = oid[1]
                except:
                    value_type = 'ERROR'

                new_kpi = kpi.strip() + '_' + disk

                if(kpi_value == 'N/A'):
                    continue

                new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), new_kpi.strip(), kpi_value.strip(), value_type.strip()]
                add_row_to_csv(csv_file, new_row)






# NX

    for ip in cmd_instance.nx_group:
        command = "snmpwalk -On -c allotcomm -v 2c %s:1161 %s"%(ip,'.1.3.6.1.2.1.1.5')

        try:
            hostname = cmd_instance.get_stdout_cmd(command).split(': ')[1].replace("\"", " ").partition('.')[0].strip()

        except:
            hostname = 'N/A'

        component = 'NX'
        for kpi, oid in system_kpi_dict.items():
            command = "snmpwalk -On -c allotcomm -v 2c %s:1161 %s" % (ip, oid[0])
            kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
            if ("error" in kpi_out):
                print(command)
            try:
                kpi_value = kpi_out.split(': ')[1]
            except:
                kpi_value = 'N/A'

            try:
                value_type = oid[1]
            except:
                value_type = 'ERROR'


            new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
            add_row_to_csv(csv_file, new_row)


        for kpi, oid in disk_kpi_dict.items():
            for disk,diskidx in disk_dict.items():
                new_oid = oid[0].replace("<diskIdx>", diskidx)
                command = "snmpwalk -On -c allotcomm -v 2c %s:1161 %s" % (ip, new_oid)
                kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
                try:
                   kpi_value = kpi_out.split(': ')[1]
                except:
                    kpi_value = 'N/A'



                try:
                    value_type = oid[1]
                except:
                    value_type = 'ERROR'


                new_kpi = kpi.strip() + '_' + disk

                if(kpi_value == 'N/A'):
                        continue

                new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), new_kpi.strip(), kpi_value.strip(), value_type.strip()]
                add_row_to_csv(csv_file, new_row)





        # STC

        for ip in cmd_instance.stc_group:
            command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, '.1.3.6.1.2.1.1.5')

            try:
                hostname = cmd_instance.get_stdout_cmd(command).split(': ')[1].replace("\"", " ").partition('.')[0].strip()

            except:
                hostname = 'N/A'

            component = 'STC'
            for kpi, oid in system_kpi_dict.items():
                command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, oid[0])
                kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
                if ("error" in kpi_out):
                    print(command)
                try:
                    kpi_value = kpi_out.split(': ')[1]
                except:
                    kpi_value = 'N/A'

                try:
                    value_type = oid[1]
                except:
                    value_type = 'ERROR'



                new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
                add_row_to_csv(csv_file, new_row)


            for kpi, oid in disk_kpi_dict.items():
                for disk, diskidx in disk_dict.items():
                    new_oid = oid[0].replace("<diskIdx>", diskidx)
                    command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, new_oid)
                    kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
                    try:
                        kpi_value = kpi_out.split(': ')[1]
                    except:
                        kpi_value = 'N/A'

                    try:
                        value_type = oid[1]
                    except:
                        value_type = 'ERROR'

                    new_kpi = kpi.strip() + '_' + disk

                    if(kpi_value == 'N/A'):
                        continue

                    new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), new_kpi.strip(), kpi_value.strip(), value_type.strip()]
                    add_row_to_csv(csv_file, new_row)

# DSC

        for ip in cmd_instance.dsc_group:
            command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, '.1.3.6.1.2.1.1.5')

            try:
                hostname = cmd_instance.get_stdout_cmd(command).split(': ')[1].replace("\"", " ").partition('.')[0].strip()

            except:
                hostname = 'N/A'

            component = 'DSC'
            for kpi, oid in system_kpi_dict.items():
                command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, oid[0])
                kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
                if ("error" in kpi_out):
                    print(command)
                try:
                    kpi_value = kpi_out.split(': ')[1]
                except:
                    kpi_value = 'N/A'

                try:
                    value_type = oid[1]
                except:
                    value_type = 'ERROR'



                new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
                add_row_to_csv(csv_file, new_row)




            for kpi, oid in disk_kpi_dict.items():
                for disk, diskidx in disk_dict.items():
                    new_oid = oid[0].replace("<diskIdx>", diskidx)
                    command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, new_oid)
                    kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
                    try:
                        kpi_value = kpi_out.split(': ')[1]
                    except:
                        kpi_value = 'N/A'

                    try:
                        value_type = oid[1]
                    except:
                        value_type = 'ERROR'

                    new_kpi = kpi.strip() + '_' + disk

                    if(kpi_value == 'N/A'):
                        continue

                    new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), new_kpi.strip(), kpi_value.strip(), value_type.strip()]
                    add_row_to_csv(csv_file, new_row)


        # DM

        for ip in cmd_instance.dm_group:
            command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, '.1.3.6.1.2.1.1.5')
            try:
                hostname = cmd_instance.get_stdout_cmd(command).split(': ')[1].replace("\"", " ").partition('.')[0].strip()

            except:
                hostname = 'N/A'

            component = 'DM'
            for kpi, oid in system_kpi_dict.items():
                command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, oid[0])
                kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
                if ("error" in kpi_out):
                    print(command)
                try:
                    kpi_value = kpi_out.split(': ')[1]
                except:
                    kpi_value = 'N/A'

                try:
                    value_type = oid[1]
                except:
                    value_type = 'ERROR'



                new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
                add_row_to_csv(csv_file, new_row)


            for kpi, oid in disk_kpi_dict.items():
                for disk, diskidx in disk_dict.items():
                    new_oid = oid[0].replace("<diskIdx>", diskidx)
                    command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, new_oid)
                    kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))

                    try:
                        kpi_value = kpi_out.split(': ')[1]
                    except:
                        kpi_value = 'N/A'


                    try:
                        value_type = oid[1]
                    except:
                        value_type = 'ERROR'

                    new_kpi = kpi.strip() + '_' + disk

                    if(kpi_value == 'N/A'):
                        continue

                    new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), new_kpi.strip(), kpi_value.strip(), value_type.strip()]
                    add_row_to_csv(csv_file, new_row)








    # SMP

    for ip in cmd_instance.smp_group:
        command = "snmpwalk -v 2c -c allotcomm %s %s"%(ip,'.1.3.6.1.2.1.1.5')

        try:
            hostname = cmd_instance.get_stdout_cmd(command).split(': ')[1].replace("\"", " ").partition('.')[0].strip()

        except:
            hostname = 'N/A'

        component = 'SMP'
        for kpi, oid in system_kpi_dict.items():
            command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, oid[0])
            kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
            if ("error" in kpi_out):
                print(command)
            try:
                kpi_value = kpi_out.split(': ')[1]
            except:
                kpi_value = 'N/A'

            try:
                value_type = oid[1]
            except:
                value_type = 'ERROR'

            new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
            add_row_to_csv(csv_file, new_row)


        for kpi, oid in smp_kpi_dict.items():
            command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, oid[0])
            kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))
            if ("error" in kpi_out):
                print(command)
            try:
                kpi_value = kpi_out.split(': ')[1]
            except:
                kpi_value = 'N/A'

            try:
                value_type = oid[1]
            except:
                value_type = 'ERROR'

            new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), kpi.strip(), kpi_value.strip(), value_type.strip()]
            add_row_to_csv(csv_file, new_row)


        for kpi, oid in disk_kpi_dict.items():
            for disk,diskidx in disk_dict.items():
                new_oid = oid[0].replace("<diskIdx>", diskidx)
                command = "snmpwalk -v 2c -c allotcomm %s %s" % (ip, new_oid)
                kpi_out = clean_output(cmd_instance.get_stdout_cmd(command))

                try:
                   kpi_value = kpi_out.split(': ')[1]
                except:
                    kpi_value = 'N/A'



                try:
                    value_type = oid[1]
                except:
                    value_type = 'ERROR'

                if(kpi_value == 'N/A'):
                        continue

                new_kpi = kpi.strip() + '_' + disk

                new_row = [component.strip(), hostname.strip(), ip.strip(), kpi_timestamp.strip(), new_kpi.strip(), kpi_value.strip(), value_type.strip()]
                add_row_to_csv(csv_file, new_row)






if __name__ == "__main__":



    cmd_instance = CMDModule.CMD('/opt/sybase/data/KPIs/tools/scripts/invenrtory_file.ini')
    cmd_instance.analyze_inventory_file()
    cmd_instance.show_devices()

    fname_tmp = "kpi_report_%s%s"%(today,'.csv')
    fname = "/opt/sybase/data/KPIs/tools/output/"+fname_tmp
    header = ['COMPONENT','HOSTNAME', 'IP','DATE', 'KPI', 'VALUE', 'VALUE_TYPE']
    csv_fname = create_csv(header, fname)

    fill_system_kpi(cmd_instance,csv_fname)
