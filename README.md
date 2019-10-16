# bindToRoute53


## Bind config into rouet53 cloudformations
We are moving our old bind server over to route53 and as we have all our config as code. 
I needed to migrate our bind configs into route53 cloud templates.


So here is a small python script that reads the files in the folder recors. Then converts them into route 53 cloudformatins templates.


To do 

- The filename of the recors must be the same as the domain example hacking.robots.beer if the domain in hacking.robots.beer (I use the filename when a genereate)
- You need to add txt and verify MX records :-)
- Theer is a limit of 50 recors in every cloudformation template .. I hit that but check so you dont go over



## To use

### Req

 - Docker
 - Docker-compose 


### Use
 
 Build the image

 ```
 docker-compose build
 ```


 Add your bind file in the records folder (with correct name)

 '''
 docker-compose up
 '''

This will generate the route53 cloudtemplates.

Is you get any errors verify that then name of the file is the same as the domain !


## Output 

This is my cmd output when building


```
mahe@:~/projects/hrb/bindToRoute53$ docker-compose build
Building bindtorouet53
Step 1/10 : FROM python
 ---> 02d2bb146b3b
Step 2/10 : EXPOSE 8080
 ---> Using cache
 ---> 0bae49565167
Step 3/10 : RUN mkdir /code
 ---> Using cache
 ---> 25c452acb603
Step 4/10 : COPY . /code/
 ---> 748de0c0acb3
Step 5/10 : WORKDIR /code/code
 ---> Running in 78ba6d14b2e7
Removing intermediate container 78ba6d14b2e7
 ---> 02c858a406ca
Step 6/10 : RUN pip install --upgrade pip
 ---> Running in 69626ded3399
Collecting pip
  Downloading https://files.pythonhosted.org/packages/4a/08/6ca123073af4ebc4c5488a5bc8a010ac57aa39ce4d3c8a931ad504de4185/pip-19.3-py2.py3-none-any.whl (1.4MB)
Installing collected packages: pip
  Found existing installation: pip 19.2.3
    Uninstalling pip-19.2.3:
      Successfully uninstalled pip-19.2.3
Successfully installed pip-19.3
Removing intermediate container 69626ded3399
 ---> d27a971b31c7
Step 7/10 : RUN pip3 install git+https://github.com/rthalley/dnspython
 ---> Running in ffe41cbd327e
Collecting git+https://github.com/rthalley/dnspython
  Cloning https://github.com/rthalley/dnspython to /tmp/pip-req-build-gittsrh8
  Running command git clone -q https://github.com/rthalley/dnspython /tmp/pip-req-build-gittsrh8
Building wheels for collected packages: dnspython
  Building wheel for dnspython (setup.py): started
  Building wheel for dnspython (setup.py): finished with status 'done'
  Created wheel for dnspython: filename=dnspython-2.0.0-py2.py3-none-any.whl size=185372 sha256=a0d13e5a72b5c837ebf0a5c2994120603c542a0cf3ec31c2a413cd8314178dc7
  Stored in directory: /tmp/pip-ephem-wheel-cache-ihr_ut_i/wheels/6b/57/51/8a22d863467edb8665f76580d84ac4e5ddfbd315f5fa1c4f7d
Successfully built dnspython
Installing collected packages: dnspython
Successfully installed dnspython-2.0.0
Removing intermediate container ffe41cbd327e
 ---> d29c07d9dd3e
Step 8/10 : RUN pip3 install easyzone
 ---> Running in c97fc2f12fc1
Collecting easyzone
  Downloading https://files.pythonhosted.org/packages/b0/1a/bf74b3267d641848ced5523c1422704790af7211e86aa765f6922b4e1c3a/easyzone-1.2.2.tar.gz
Requirement already satisfied: dnspython in /usr/local/lib/python3.7/site-packages (from easyzone) (2.0.0)
Building wheels for collected packages: easyzone
  Building wheel for easyzone (setup.py): started
  Building wheel for easyzone (setup.py): finished with status 'done'
  Created wheel for easyzone: filename=easyzone-1.2.2-cp37-none-any.whl size=7992 sha256=cdca0bcf42b6b66b2dd9cced5a0db511f43cb4e929d2942f6a8536913bd84a9d
  Stored in directory: /root/.cache/pip/wheels/b7/88/af/e6827feaee57713c87d6cb817a3da9b4ccf3dd59554c8b33ca
Successfully built easyzone
Installing collected packages: easyzone
Successfully installed easyzone-1.2.2
Removing intermediate container c97fc2f12fc1
 ---> f12078c49ccf
Step 9/10 : RUN pip3 install pyyaml
 ---> Running in 8036d5c7872a
Collecting pyyaml
  Downloading https://files.pythonhosted.org/packages/e3/e8/b3212641ee2718d556df0f23f78de8303f068fe29cdaa7a91018849582fe/PyYAML-5.1.2.tar.gz (265kB)
Building wheels for collected packages: pyyaml
  Building wheel for pyyaml (setup.py): started
  Building wheel for pyyaml (setup.py): finished with status 'done'
  Created wheel for pyyaml: filename=PyYAML-5.1.2-cp37-cp37m-linux_x86_64.whl size=468686 sha256=998f6b37cf6da1dde4183a60486d6eaf332dce0c5e07730bb3e28d8516b39b01
  Stored in directory: /root/.cache/pip/wheels/d9/45/dd/65f0b38450c47cf7e5312883deb97d065e030c5cca0a365030
Successfully built pyyaml
Installing collected packages: pyyaml
Successfully installed pyyaml-5.1.2
Removing intermediate container 8036d5c7872a
 ---> 4c1842480db8
Step 10/10 : CMD ["python","migrate.py"]
 ---> Running in 981e956422f0
Removing intermediate container 981e956422f0
 ---> 66c9a2ecdb4d
Successfully built 66c9a2ecdb4d
Successfully tagged bindtoroute53_bindtorouet53:latest

mahe@:~/projects/hrb/bindToRoute53$ docker-compose up
Recreating bindtoroute53_bindtorouet53_1 ... done
Attaching to bindtoroute53_bindtorouet53_1
bindtoroute53_bindtorouet53_1 exited with code 0


mahe:~/projects/hrb/bindToRoute53$ cat code/route53/hacking.robots.beer 
AWSTemplateFormatVersion: '2010-09-09'
Resources:
  DNS:
    Properties:
      HostedZoneConfig:
        Comment: DNS Settings for hacking.robots.beer
      Name: hacking.robots.beer
    Type: AWS::Route53::HostedZone

  '@':
    DependsOn: DNS
    Properties:
      HostedZoneName: hacking.robots.beer.
      Name: '@'
      ResourceRecords:
      - dns
      TTL: 900
      Type: NS
    Type: AWS::Route53::RecordSet

  a_robot:
    DependsOn: DNS
    Properties:
      HostedZoneName: hacking.robots.beer.
      Name: a_robot
      ResourceRecords:
      - 127.0.0.1
      TTL: 900
      Type: A
    Type: AWS::Route53::RecordSet

  c_robot:
    DependsOn: DNS
    Properties:
      HostedZoneName: hacking.robots.beer.
      Name: c_robot
      ResourceRecords:
      - a_robot
      TTL: 900
      Type: CNAME
    Type: AWS::Route53::RecordSet



```

