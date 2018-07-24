#!/usr/bin/python
import re
if __name__ == '__main__':
    ro_mount_points=""
    result=[]
    mount_re = re.compile(r'''(?P<fs>\S+) #File system
    \s+ #whitespace
    (?P<mount_point>\S+)
    \s+ #whitespace
    (?P<type>\S+)
    \s+ #whitespace
    (?P<opt>\S+)
    \s+ 
    \S+ #dump
    \s+
    \S+ #pass
    ''', re.VERBOSE)
    ro_re=re.compile(r'''^ro.*''')
    ro_mounts=[]
    try:
     #open for read
     mount=open('/proc/mounts','r')
     mountlist=mount.read().split('\n')
     mount.close()
     for i in mountlist:
         m = mount_re.match(i)
         if m:
             result.append(m.groupdict())
     for i in result:
          if re.match(ro_re, i['opt']):
             ro_mounts.append(i)
    except:
        print("Unexpected error")
        exit(3)
    if not ro_mounts:
        print("OK, no RO mounts")
        exit(0)
    else:
        for i in ro_mounts:
            ro_mount_points +=i['mount_point']+" , "
        print("Critical: %s was mounted with RO flag" %(ro_mount_points))
        exit(2)