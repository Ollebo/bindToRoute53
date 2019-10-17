from os import listdir
from os.path import isfile, join
import dns.zone
from dns.exception import DNSException
from dns.rdataclass import *
from dns.rdatatype import *
import yaml
 



def setupDomainFile(domain):
    #Setup the hosted zone file first


    record = {
              "AWSTemplateFormatVersion": "2010-09-09",
              "Resources": {
                "DNS": {
                  "Type": "AWS::Route53::HostedZone",
                  "Properties": {
                    "Name": "{0}".format(domain),
                    "HostedZoneConfig": {
                      "Comment": "DNS Settings for {0}".format(domain)
                    }
                  }
                }
              }
            }
    f.write(yaml.dump(record))




def createRoue53Template(name,target,type,domain):
    '''
    Create route 53 cloud formations to be applied
    '''
    awsName = name.replace('-','')

    record ={
            "ResourcesSPACE": {
            awsName: {
            "DependsOn": "DNS",
            "Type": "AWS::Route53::RecordSet",
            "Properties": {
              "HostedZoneName": "{0}.".format(domain),
              "Name": "{0}".format(name),
              "Type": "{0}".format(type),
              "TTL": 900,
              "ResourceRecords": [
                target
              ]
            }
          }
        }}



    out = yaml.dump(record)
    f.write(out.replace('ResourcesSPACE:',''))



 
def extractRecords(filename):
    '''
    Extract the records from the file
    '''


    domain = filename
    
    zone = dns.zone.from_file('records/'+filename, domain)



    #Setup the hosed zone for file
    setupDomainFile(domain)

    #Start lopping records

    for name,node in zone.nodes.items():
        rdatasets = node.rdatasets
        dnsname = format(name)
        for rdataset in rdatasets:

            for rdata in rdataset:

                if rdataset.rdtype == MX:
                    print("** MX-specific rdata **")
                    print("exchange:{0}".format(rdata.exchange))
                    print("preference:{0}".format(rdata.preference))
                    #Create record
                    createRoue53Template(dnsname,rdata.exchange,'MX',domain)


                if rdataset.rdtype == NS:
                    #Create record
                    createRoue53Template(dnsname,format(rdata.target),'NS',domain)
                if rdataset.rdtype == CNAME:
                    #Create record
                    createRoue53Template(dnsname,format(rdata.target),'CNAME',domain)
                if rdataset.rdtype == A:
                    #Create record
                    createRoue53Template(dnsname,rdata.address,'A',domain)









# Get all the files in the dir records to process

dirName = 'records'
fileNames = [f for f in listdir(dirName) if isfile(join(dirName, f))]


for filename in fileNames:


    f = open("route53/{0}".format(filename), "w")
    extractRecords(filename)
    f.close()
    