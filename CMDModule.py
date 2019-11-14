#!/usr/bin/python
import subprocess
import sys
import os
import socket


def valid_ipv4(ip):
    try:
        socket.inet_aton(ip)
        # legal
        if (len(ip) < 7):
            return 0
        else:
            return 1
    except socket.error:
        # Not legal
        return 0

class CMD:
    nx_group = []
    smp_group = []
    aos_group = []
    stc_group = []
    dsc_group = []
    dm_group = []
    dwh_group = []
    bi_group = []
    other_group = []
    flag = ''
    invetory_path = ''

    def __init__(self, path):
        self.invetory_path = path


    def analyze_inventory_file(self):
        with open(self.invetory_path, 'r') as f:
            for line in f:
                newline = line.strip()
                if newline.startswith('[NX]'):
                    flag = 'nx'
                    continue
                elif newline.startswith('[SMP]'):
                    flag = 'smp'
                    continue
                elif newline.startswith('[OTHER]'):
                    flag = 'other'
                    continue
                elif newline.startswith('[AOS]'):
                    flag = 'aos'
                    continue
                elif newline.startswith('[DSC]'):
                    flag = 'dsc'
                    continue
                elif newline.startswith('[STC]'):
                    flag = 'stc'
                    continue
                elif newline.startswith('[DWH]'):
                    flag = 'dwh'
                    continue
                elif newline.startswith('[BI]'):
                    flag = 'bi'
                    continue
                else:
                    if (valid_ipv4(newline) == 1):
                        if flag == 'nx':
                            self.nx_group.append(newline)
                            continue
                        elif flag == 'smp':
                            self.smp_group.append(newline)
                            continue
                        elif flag == 'other':
                            self.other_group.append(newline)
                            continue
                        elif flag == 'aos':
                            self.aos_group.append(newline)
                            continue
                        elif flag == 'dsc':
                            self.dsc_group.append(newline)
                            continue
                        elif flag == 'stc':
                            self.stc_group.append(newline)
                            continue
                        elif flag == 'dwh':
                            self.dwh_group.append(newline)
                            continue
                        elif flag == 'bi':
                            self.bi_group.append(newline)
                            continue
                        else:
                            continue
                    else:
                        continue





    def show_devices(self):
        print("NX: ", self.nx_group)
        print("SMP: ", self.smp_group)
        print("ASO: ", self.aos_group)
        print("STC: ", self.stc_group)
        print("DSC: ", self.dsc_group)
        print("DWH: ", self.dwh_group)
        print("BI: ", self.bi_group)
        print("OTHER: ", self.other_group)





    @staticmethod
    def remote_cmd(host, user, psswd ,cmd):
        HOST=host
        COMMAND=cmd
        USER=user
        PASS= psswd

        read, write = os.pipe()
        os.write(write, "kourdiserver")
        os.close(write)

        sshproc = subprocess.Popen(["ssh", "-q", "%s@%s" % (USER,HOST), COMMAND], shell=False,stdin=read, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
     #   sshproc.stdin.write(b'kourdiserver\n')
     #   sshproc.communicate()[0]
     #   sshproc.stdin.close()
        print "A"



        result = sshproc.stdout.readlines()

        if result == []:
            error = sshproc.stderr.readlines()
            print >>sys.stderr, "ERROR: %s" % error
        else:
            print result
            return result



    def group_cmd(self, group, command):
        if group == 'nx':
            for host in self.nx_group:
                remote_cmd(host, 'allot', command)
        elif group == 'smp':
            for host in self.smp_group:
                remote_cmd(host, 'allot', command)
        elif group == 'other':
            for host in self.other_group:
                remote_cmd(host, 'allot', command)
        elif group == 'aos':
            for host in self.aos_group:
                remote_cmd(host, 'allot', command)
        elif group == 'dsc':
            for host in self.dsc_group:
                remote_cmd(host, 'allot', command)
        elif group == 'stc':
            for host in self.stc_group:
                remote_cmd(host, 'allot', command)
        elif group == 'dwh':
            for host in self.dwh_group:
                remote_cmd(host, 'allot', command)
        elif group == 'bi':
            for host in self.bi_group:
                remote_cmd(host, 'allot', command)


    def get_stdout_cmd(self, command):
        cmd = command.split(' ')
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = output.communicate()
        return stdout


    def local_cmd(self, command):
        cmd = command
        os.system(cmd)

    def local_threadcmd(self, command):
        cmd = command
        os.system(cmd)

    def get_stdout_threadcmd(self, command):
        cmd = command.split(' ')
        output = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = output.communicate()
        return stdout
