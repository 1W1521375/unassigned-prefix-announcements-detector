import pandas as pd
import re
from netaddr import *
import ipaddress
import codecs # for file output

infile = "(file path here)"
outfile = "(file path here)"

# route information
dtyp = {"Peer ASN (ASN of the monitor)": "int16"}
ns = ("BGP Protocol", "timestamp", "W/A/B", "Peer IP(address of the monitor)", "Peer ASN (ASN of the monitor)", "Prefix", "ASPath", "Origin Protocol") 
rccX_df = pd.read_csv(infile, delimiter = "|", names = ns, dtype = dtyp)

# addresses allocated to the region
region_file = "(file path here)"
region_df = pd.read_csv(region_file, delimiter = "\t", names = ("cc", "IP block"))

# unallocated addresses in the region
nic_pooled = "(file path here)"
pooled_df = pd.read_csv(nic_pooled, header = None, names = ("IP block",))

del rccX_df["BGP Protocol"], rccX_df["timestamp"], rccX_df["W/A/B"], \
    rccX_df["Peer IP(address of the monitor)"], rccX_df["Peer ASN (ASN of the monitor)"], \
    rccX_df["ASPath"], rccX_df["Origin Protocol"]

# regular expression of a cidr
cidr_regex = "\d+\.\d+\.\d+\.\d+/\d+"
# regular expression of an ip address
ip_regex = "\d+\.\d+\.\d+\.\d+"

# extracting addressses allocated to nic
scope_blocks = []
# iteration over df /8 each
for i in range(1, 256): # all 1-255 /8 subnets comparisons
    # picks i.***.***.***/? up 
    head = str(i) + "{1}\."
    region_section = region_df.applymap(lambda x: bool(re.match(head, x)))
    region_sub_table = region_df[region_section]["IP block"].dropna()
    
    rccX_section = rccX_df.applymap(lambda x: bool(re.match(head, x)))
    rccX_sub_table = rccX_df[rcc_section]["Prefix"].dropna()
    
    scope_raw = set()
    for rccX_row in rccX_sub_table:
        n1 = IPSet()
        n1.add(IPNetwork(rccX_row))
    
        for region_row in region_sub_table:
            n2 = IPSet()
            n2.add(IPNetwork(region_row))
            intersection = n1 & n2
            scope_raw.add(str(intersection))
            
    scope = list(scope_raw)
    blocks = [re.search(cidr_regex, x).group() for i, x in enumerate(scope_raw) if x != "IPSet([])"]
    scope_blocks.append(blocks) 

print(f"first step done", sep = "\n", file = codecs.open(outfile, "a", "utf-8"))

sus_raw = set()

# detecting unallocated addresses in route
for blocks in scope_blocks:
    for bl in blocks:
        n1 = IPSet()
        n1.add(IPNetwork(bl))
        for p_block in pooled_df.itertuples():
            n2 = IPSet()
            if ("-" in (p_block[1])): # there are some entries written in a range format as ; "*** - ***"
                match = re.findall(ip_regex, p_block[1]) # returns a list of matched parts
                s1 = IPSet()
                s1.add(IPRange(match[0], match[1]))
                intersection = n1 & s1
            else:
                n2.add(IPNetwork(str(p_block[1])))
                intersection = n1 & n2
            sus_raw.add(str(intersection))

sus = list(sus_raw)
sus_blocks = [re.findall(cidr_regex, x) for i, x in enumerate(sus) if x != "IPSet([])"]
print(f"{sus_blocks}", sep = "\n", file = codecs.open(outfile, "a", "utf-8"))

print("second step done", file = codecs.open(outfile, "a", "utf-8"))
