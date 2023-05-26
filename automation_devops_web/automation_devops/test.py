#!/usr/bin/env python3

import argparse
import subprocess
import re

parser = argparse.ArgumentParser()
parser.add_argument('-T', '--tool', dest='tool', help='Define the tool', type=str)
parser.add_argument('-A', '--action', dest='action', help='Action you would like to do', type=str)
args = parser.parse_args()

if (args.tool=='apache'):
    if (args.action=='create'):
        subprocess.call("cd apache_project_docker && docker-compose up -d", shell=True)

    elif (args.action=='destroy'):
        subprocess.call("cd apache_project_docker && docker-compose down --rmi all", shell=True)

    elif (args.action=='connect'):
        subprocess.call("docker exec -it apacheserver /bin/bash", shell=True)

    elif (args.action=='connectivity'):
        test = subprocess.check_output("docker network inspect apache_project_docker_apache_network | grep -A 4 apacheserver | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 80 ", shell=True)
        print("========================================================")
        print("Only port 80 will be opened by default. 443 will not be opened. Port 443 will throw error.")
        subprocess.call("nc -vz -w 5 "+ host +" 443 ", shell=True)
        print("========================================================")

    elif (args.action=='logs'):
        subprocess.call("docker logs apacheserver", shell=True)

elif (args.tool=='ansible'):
    if (args.action=='create'):
        subprocess.call("cd ansible_project_docker && docker-compose up -d", shell=True)

    elif (args.action=='destroy'):
        subprocess.call("cd ansible_project_docker && docker-compose down --rmi all", shell=True)

    elif (args.action=='connect'):
        subprocess.call("docker exec -it ansibleserver /bin/bash", shell=True)

    elif (args.action=='connectivity'):
        test = subprocess.check_output("docker network inspect ansible_project_docker_ansible_network | grep -A 4 ansibleserver | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 22 ", shell=True)
        print("========================================================")

        test = subprocess.check_output("docker network inspect ansible_project_docker_ansible_network | grep -A 4 ubuntuhost | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 22 ", shell=True)
        print("========================================================")

        test = subprocess.check_output("docker network inspect ansible_project_docker_ansible_network | grep -A 4 amazonlinuxhost | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 22 ", shell=True)
        print("========================================================")


    elif (args.action=='logs'):
        subprocess.call("docker logs ansibleserver", shell=True)
        subprocess.call("docker logs ubuntuhost", shell=True)
        subprocess.call("docker logs amazonlinuxhost", shell=True)

elif (args.tool=='aws'): 
    if (args.action=='create'):
        subprocess.call("cd aws_project_docker && docker-compose up -d", shell=True)

    elif (args.action=='destroy'):
        subprocess.call("cd aws_project_docker && docker-compose down --rmi all", shell=True)

    elif (args.action=='connect'):
        subprocess.call("docker exec -it awsserver /bin/bash", shell=True)

    elif (args.action=='connectivity'):
        print("AWS CLI is not running as service, hence it will not open any port. It is just Software.")

    elif (args.action=='logs'):
        subprocess.call("docker logs awsserver", shell=True)

elif (args.tool=='django'):
    if (args.action=='create'):
        subprocess.call("cd django_project_docker && docker-compose up -d", shell=True)

    elif (args.action=='destroy'):
        subprocess.call("cd django_project_docker && docker-compose down --rmi all", shell=True)

    elif (args.action=='connect'):
        subprocess.call("docker exec -it django /bin/bash", shell=True)

    elif (args.action=='connectivity'):
        test = subprocess.check_output("docker network inspect django_project_docker_django_network | grep -A 4 django | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        subprocess.call("nc -vz -w 5 "+ host +" 8000 ", shell=True)

    elif (args.action=='logs'):
        subprocess.call("docker logs django", shell=True)

elif (args.tool=='elk'):
    if (args.action=='create'):
        subprocess.call("cd elk_project_docker && docker-compose up -d", shell=True)

    elif (args.action=='destroy'):
        subprocess.call("cd elk_project_docker && docker-compose down --rmi all", shell=True)

    elif (args.action=='connect'):
        subprocess.call("docker exec -it elasticsearch /bin/bash", shell=True)

    elif (args.action=='connectivity'):
        test = subprocess.check_output("docker network inspect elk_project_docker_elk_network | grep -A 4 elasticsearch | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 9200 ", shell=True)
        print("========================================================")

        test = subprocess.check_output("docker network inspect elk_project_docker_elk_network | grep -A 4 kibana | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 5601 ", shell=True)
        print("========================================================")

        test = subprocess.check_output("docker network inspect elk_project_docker_elk_network | grep -A 4 logstash | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 5044 ", shell=True)
        print("========================================================")

        test = subprocess.check_output("docker network inspect elk_project_docker_elk_network | grep -A 4 filebeatserver | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 22 ", shell=True)
        print("========================================================")


    elif (args.action=='logs'):
        subprocess.call("docker logs elasticsearch", shell=True)
        subprocess.call("docker logs kibana", shell=True)
        subprocess.call("docker logs logstash", shell=True)
        subprocess.call("docker logs filebeatserver", shell=True)

elif (args.tool=='prometheus'):
    if (args.action=='create'):
        subprocess.call("cd prometheus_project_docker && docker-compose up -d", shell=True)

    elif (args.action=='destroy'):
        subprocess.call("cd prometheus_project_docker && docker-compose down --rmi all", shell=True)

    elif (args.action=='connect'):
        subprocess.call("docker exec -it prometheus /bin/bash", shell=True)

    elif (args.action=='connectivity'):
        test = subprocess.check_output("docker network inspect prometheus_project_docker_pg_network | grep -A 4 prometheus | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 9090 ", shell=True)
        print("========================================================")

        test = subprocess.check_output("docker network inspect prometheus_project_docker_pg_network | grep -A 4 grafana | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 3000 ", shell=True)
        print("========================================================")

        test = subprocess.check_output("docker network inspect prometheus_project_docker_pg_network | grep -A 4 node_exporter | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 9100 ", shell=True)
        print("========================================================")


    elif (args.action=='logs'):
        subprocess.call("docker logs prometheus", shell=True)
        subprocess.call("docker logs grafana", shell=True)
        subprocess.call("docker logs node_exporter", shell=True)

elif (args.tool=='mysql'):
    if (args.action=='create'):
        subprocess.call("cd mysql_project_docker && docker-compose up -d", shell=True)

    elif (args.action=='destroy'):
        subprocess.call("cd mysql_project_docker && docker-compose down --rmi all", shell=True)

    elif (args.action=='connect'):
        subprocess.call("docker exec -it sp-mysql /bin/bash", shell=True)

    elif (args.action=='connectivity'):
        test = subprocess.check_output("docker network inspect prometheus_project_docker_pg_network | grep -A 4 prometheus | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 9090 ", shell=True)
        print("========================================================")

        test = subprocess.check_output("docker network inspect prometheus_project_docker_pg_network | grep -A 4 grafana | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 3000 ", shell=True)
        print("========================================================")

        test = subprocess.check_output("docker network inspect prometheus_project_docker_pg_network | grep -A 4 node_exporter | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 9100 ", shell=True)
        print("========================================================")


    elif (args.action=='logs'):
        subprocess.call("docker logs sp-mysql", shell=True)
        subprocess.call("docker logs sp-php", shell=True)

elif (args.tool=='jenkins'):
    if (args.action=='create'):
        subprocess.call("cd jenkins_project_docker && docker-compose up -d", shell=True)

    elif (args.action=='destroy'):
        subprocess.call("cd jekins_project_docker && docker-compose down --rmi all", shell=True)

    elif (args.action=='connect'):
        subprocess.call("docker exec -it jenkins_server /bin/bash", shell=True)

    elif (args.action=='connectivity'):
        test = subprocess.check_output("docker network inspect jenkins_project_docker_pg_network | grep -A 4 prometheus | grep IPv4Address", shell=True, universal_newlines=True)
        s1 = re.compile(r'[0-9.]+/')
        m1 = s1.search(test)
        host= (m1.group(0).rstrip('/'))
        print("========================================================")
        subprocess.call("nc -vz -w 5 "+ host +" 8090 ", shell=True)
        print("========================================================")

    elif (args.action=='logs'):
        subprocess.call("docker logs jenkins", shell=True)

elif (args.tool=='terraform'):
    if (args.action=='create'):
        subprocess.call("cd terraform_project_docker && docker-compose up -d", shell=True)

    elif (args.action=='destroy'):
        subprocess.call("cd terraform_project_docker && docker-compose down --rmi all", shell=True)

    elif (args.action=='connect'):
        subprocess.call("docker exec -it terraform /bin/bash", shell=True)

    elif (args.action=='connectivity'):
        print("Terraform is not running as service, hence it will not open any port. It is just Software.")

    elif (args.action=='logs'):
        subprocess.call("docker logs terraform", shell=True)

else:
    print('''python test.py -T tool -A action

where,
tool = <apache|ansible|aws|django|terraform|jenkins|elk|prometheus|mysql> 
action = <create|destroy|connect|connectivity|logs>
''')
