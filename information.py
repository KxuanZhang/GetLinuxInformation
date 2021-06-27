import os
import psutil
from collections import OrderedDict
import pprint
import time
 

# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))


 # Return RAM information (unit=kb) in a list                                      
# Index 0: total RAM                                                              
# Index 1: used RAM                                                                
# Index 2: free RAM                                                                

def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
 


# Return information about disk space as a list (unit included)                    
# Index 0: total disk space                                                        
# Index 1: used disk space                                                        
# Index 2: remaining disk space                                                    
# Index 3: percentage of disk used                                                 

def getDiskSpace():
    p = os.popen("df -h /")
    i = 0
    while 1:
        i = i +1
        line = p.readline()
        if i==2:
            return(line.split()[1:5])

def CPUinfo():
    '''Return the info in /proc/cpuinfo
    as a dirctionary in the follow format:
    CPU_info['proc0']={...}
    CPU_info['proc1']={...}
    '''
    
    CPUinfo=OrderedDict()
    procinfo=OrderedDict()
 
    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                #end of one processor
                CPUinfo['proc%s' % nprocs]=procinfo
                nprocs = nprocs+1
                #Reset
                procinfo=OrderedDict()
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''
    return CPUinfo



 

if __name__ == '__main__':

    CPUinfo = CPUinfo()
    isWriteFile = True
    for processor in CPUinfo.keys():
            print('CPUinfo[{0}]={1}'.format(processor,CPUinfo[processor]['model name']))
    while True:
        # CPU informatiom
        CPU_temp = getCPUtemperature()
        # CPU占用率
        cpu_res = psutil.cpu_percent()
        

        # RAM information
        # Output is in kb, here I convert it in Mb for readability

        RAM_stats = getRAMinfo()
        RAM_total = round(int(RAM_stats[0]) / 1000,1)
        RAM_used = round(int(RAM_stats[1]) / 1000,1)
        RAM_free = round(int(RAM_stats[2]) / 1000,1)
        # Disk information

        DISK_stats = getDiskSpace()
        DISK_total = DISK_stats[0]
        DISK_used = DISK_stats[1]
        DISK_perc = DISK_stats[3]
        
        if isWriteFile:
            t = time.localtime()
            times = '%d:%d:%d' % (t.tm_hour, t.tm_min, t.tm_sec)
            with open('systemInformation.txt', 'a+') as f:
                f.write('time:%s,CPU_res:%s \n' % (times, cpu_res))
                f.write('time:%s,CPU_temp:%s \n' % (times, CPU_temp))
                f.write('time:%s,RAM Total:%s \n' % (times, str(RAM_total)))
                f.write('time:%s,RAM Used:%s \n' % (times, str(RAM_used)))
                f.write('time:%s,RAM Free:%s \n' % (times, str(RAM_free)))
        
        print('____________________________________________')
        print('CPU Temperature = '+CPU_temp)
        print('CPU_resource = ' + str(cpu_res))
        print('')
        print('RAM Total = '+str(RAM_total)+' MB')
        print('RAM Used = '+str(RAM_used)+' MB')
        print('RAM Free = '+str(RAM_free)+' MB')
        print('') 
        print('DISK Total Space = '+str(DISK_total)+'B')
        print('DISK Used Space = '+str(DISK_used)+'B')
        print('DISK Used Percentage = '+str(DISK_perc))
        time.sleep(1)
        