import pandas as pd
from netaddr import *
import ipaddress
import re
from datetime import datetime
import codecs

ip_regex = "\d+\.\d+\.\d+\.\d"
cidr_regex = "\d+.\d+\.\d+.\d+/\d+"

today = datetime.now()
yyyymmdd = today.strftime('%Y%m%d')

# fixed allocables
fixed_allocable = "/var/jpnic/data/allocable-jpnic/jprs-address.txt"
fixed_alloc_df = pd.read_csv(fixed_allocable, delimiter = "\n", names = ("IPrange",))

for i, entry in enumerate(fixed_alloc_df["IPrange"]):
    start_end = re.findall(ip_regex, entry)
    n = IPSet()
    n.add(IPRange(start_end[0], start_end[1]))
    fixed_alloc_df["IPrange"][i] = n
    
# dynamic allocables
dyn_allocable = "/var/jpnic/data/allocable-jpnic/apnic-address.csv"
dyn_alloc_df = pd.read_csv(dyn_allocable, delimiter = "\n", names = ("IPrange(dec)",))

for j, entry in enumerate(dyn_alloc_df["IPrange(dec)"]):
    start_end = re.findall("\d+", entry)
    start = ipaddress.IPv4Address(int(start_end[0]))
    end = ipaddress.IPv4Address(int(start_end[1]))
    n = IPSet()
    n.add(IPRange(str(start), str(end)))
    dyn_alloc_df["IPrange(dec)"][j] = n
    
clmn_name = {"IPrange(dec)": "IPrange"}
dyn_alloc_df = dyn_alloc_df.rename(columns = clmn_name)

# concat the two allocable dfs
allocable_df = pd.concat([fixed_alloc_df, dyn_alloc_df])
allocable_df = allocable_df.reset_index(drop = True)

# allocateds
allocated_file = "/var/jpnic/data/allocated-jpnic/allocated-jpnic-address.csv"
allocated_df = pd.read_csv(allocated_file, delimiter = "\n", names = ("IPrange(dec)",))

for k, entry in enumerate(allocated_df["IPrange(dec)"]):
    start_end = re.findall("\d+", entry)
    start = ipaddress.IPv4Address(int(start_end[0]))
    end = ipaddress.IPv4Address(int(start_end[1]))
    n = IPSet()
    n.add(IPRange(str(start), str(end)))
    allocated_df["IPrange(dec)"][k] = n
    
clmn_name = {"IPrange(dec)": "IPrange"}
allocated_df = allocated_df.rename(columns = clmn_name)

temp_file = "/var/jpnic/data/unallocated-jpnic/" + yyyymmdd + "-unallocated_temp.txt"
for available in allocable_df["IPrange"]:
    n1 = available
    for allocated in allocated_df["IPrange"]:
        n2 = allocated
        n1.remove(n2.iprange())
    print(f"{n1}", file = codecs.open(temp_file, 'a', 'utf-8'))
    
# rearrange the format
cidrs = []
with open(temp_file, mode = 'r') as f:
    for line in f:
        if (line != "IPSet([])"):
            cidrs.append(re.findall(cidr_regex, line))
cidrs = [item for sublist in cidrs for item in sublist]
cidrs.sort()

temp, cs = [], []
for cidr in reversed(cidrs):
    slash8_pref = re.match("(3|4|5|6|7|8|9)*", cidr).group()
    if slash8_pref:
        temp.append(cidr)
    else:
        cs.append(cidr)
temp.sort()
cs.sort()
cidrs = temp + cs

# write to a file
outfile = "/var/jpnic/data/unallocated-jpnic/" + yyyymmdd + "-unallocs_final.txt"
for cidr in cidrs:
    if cidr == cidrs[-1]:
        print(f"{cidr}", end = '', file = codecs.open(outfile, 'a', 'utf-8'))
    else:
        print(f"{cidr}\n", end = '', file = codecs.open(outfile, 'a', 'utf-8'))
