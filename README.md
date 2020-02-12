# Route research by JPNIC
This is a simple script that compares a full route information (observed announcements) and lists of assigned/unassigned IP prefixes managed by a region/organisation, then detects unassigned prefixes that actually are anounced in the internet.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites
(What things you need to install the software and how to install them)

```
python3 (>= 3.6.7)
pip install pandas
pip install netaddr
pip install ipaddress
pip install codecs
```

For preparation of input data, below is recommended;
```
libbgmdump
```

### Input data format
For route information, a txt format table file as shown below is required:
```
BGP Protocol|timestamp|W/A/B|Peer IP|Peer ASN|Prefix\ASPath|Origin Protocol|Next Hop|LocalPref|MED|Community strings|Atomic Aggregator|Aggregator
TABLE_DUMP2|mm/dd/yy hh:mm:ss|B|192.0.2.0|64496|203.0.113.0/30|64501 64502 64503 64504 64506|IGP
...
```
We first downloaded a mrt format file from RIPE RIS: https://www.ripe.net/analyse/internet-measurements/routing-information-service-ris/ris-raw-data  
Then coverted them into txt format using `libbgpdump`.

For assigned IP prefixes of an organisation, a simple txt/csv format below is supported:
```
NAME_OF_THE_ORGANISATION 192.0.2.0/24
NAME_OF_THE_ORGANISATION 203.0.113.0/24
...
```
For unassigned IP, 
```
192.0.2.0/26
203.0.113.0/28
...
```

## Output example

Running the script gives a list of unassigned AND annoucned prefixes, which theoretically are not supposed to appear in any of the actual internet routes.

```
[['192.0.2.0/28'], ['203.0.113.0/30']]
```

## Authors

Kentaro Goto, a univ student currently working at JPNIC

## Acknowledgements

* Akira Shibuya, JPNIC
* Masayuki Okada, JPNIC

