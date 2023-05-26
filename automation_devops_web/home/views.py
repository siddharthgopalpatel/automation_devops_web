#!/usr/bin/env python3

from django.shortcuts import render, HttpResponse
from .texttohtml import formatHtml
from django.template.loader import render_to_string

import argparse
import subprocess
import re
import time

def index(request):
    return(render(request, "index.html"))


def inputfile(request):
    return(render(request, "input.html"))


def result(request):
    if request.method == "POST":
        text1 = request.POST.get("tool")
        text2 = request.POST.get("action")


        if (text1=='apache'):
            if (text2=='create'):
                subprocess.call("echo | tee /var/log/ad.log; cd automation_devops/apache_project_docker; docker-compose up -d &", shell=True)
                text1 = "Default port for Apache is 80 & 443. Type <IP>:80 in the browser to access Apache"
                return(render(request, "result1.html", {"htmlcode": "Apache", "html": "CREATED", "text1": text1 }))            

            elif (text2=='destroy'):
                subprocess.call("cd automation_devops/apache_project_docker; docker-compose down --rmi all &", shell=True)
                subprocess.call("cp /var/log/ad.log /var/log/ad_apache.log", shell=True)
                text = "It may take few seconds to destroy the environment, Thank You"
                return(render(request, "result2.html", {"htmlcode": "Apache", "html": "DESTROYED", "text": text }))

            elif (text2=='connect'):
                subprocess.call("docker exec -it apacheserver /bin/bash", shell=True)
                return(render(request, "thankyou.html"))        
        
            elif (text2=='connectivity'):
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
                return(render(request, "thankyou.html"))

            elif (text2=='logs'):
                print("========================================================")
                print("Apache container logs as below : ")
                subprocess.call("docker logs apacheserver", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))

        elif (text1=='ansible'):
            if (text2=='create'):
                subprocess.call("echo | tee /var/log/ad.log; cd automation_devops/ansible_project_docker && docker-compose up -d &", shell=True)
                text1 = "Ansible usually connects passwordless through port 22. Login to ansible server to work on it"
                return(render(request, "result1.html", {"htmlcode": "Ansible", "html": "CREATED", "text1": text1 }))

            elif (text2=='destroy'):
                subprocess.call("cd automation_devops/ansible_project_docker && docker-compose down --rmi all &", shell=True)
                subprocess.call("cp /var/log/ad.log /var/log/ad_ansible.log", shell=True)
                text = "It may take few seconds to destroy the environment, Thank You"
                return(render(request, "result2.html", {"htmlcode": "Ansible", "html": "DESTROYED", "text": text }))

            elif (text2=='connect'):
                subprocess.call("docker exec -it ansibleserver /bin/bash", shell=True)
                return(render(request, "thankyou.html"))

            elif (text2=='connectivity'):
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
                return(render(request, "thankyou.html"))

            elif (text2=='logs'):
                print("========================================================")
                print("Ansible container logs as below : ")
                subprocess.call("docker logs ansibleserver", shell=True)
                print("========================================================")
                print("Ubuntu container logs as below : ")
                subprocess.call("docker logs ubuntuhost", shell=True)
                print("========================================================")
                print("Amazon container logs as below : ")
                subprocess.call("docker logs amazonlinuxhost", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))

        elif (text1=='aws'):
            if (text2=='create'):
                subprocess.call("echo | tee /var/log/ad.log; cd automation_devops/aws_project_docker && docker-compose up -d &", shell=True)
                text1 = "AWS CLI is just aws command. Login to AWS container to work on it"
                return(render(request, "result1.html", {"htmlcode": "AWS", "html": "CREATED", "text1": text1 }))

            elif (text2=='destroy'):
                subprocess.call("cd automation_devops/aws_project_docker && docker-compose down --rmi all &", shell=True)
                subprocess.call("cp /var/log/ad.log /var/log/ad_aws.log", shell=True)
                text = "It may take few seconds to destroy the environment, Thank You"
                return(render(request, "result2.html", {"htmlcode": "AWS", "html": "DESTROYED", "text": text }))
        
            elif (text2=='connect'):
                subprocess.call("docker exec -it awsserver /bin/bash", shell=True)
                return(render(request, "thankyou.html"))
        
            elif (text2=='connectivity'):
                print("========================================================")
                print("AWS CLI is not running as service, hence it will not open any port. It is just Software.")
                return(render(request, "thankyou.html"))
                print("========================================================")

            elif (text2=='logs'):
                print("========================================================")
                print("AWS container logs as below : ")
                subprocess.call("docker logs awsserver", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
        elif (text1=='django'):
            if (text2=='create'):
                subprocess.call("echo | tee /var/log/ad.log; cd automation_devops/django_project_docker && docker-compose up -d &", shell=True)
                text1 = "Default port for Django is 8000. Type <IP>:8000 in the browser to access Django"
                return(render(request, "result1.html", {"htmlcode": "DJANGO", "html": "CREATED", "text1": text1 }))

            elif (text2=='destroy'):
                subprocess.call("cd automation_devops/django_project_docker && docker-compose down --rmi all &", shell=True)
                subprocess.call("cp /var/log/ad.log /var/log/ad_django.log", shell=True)
                text = "It may take few seconds to destroy the environment, Thank You"
                return(render(request, "result2.html", {"htmlcode": "DJANGO", "html": "DESTROYED", "text": text }))
        
            elif (text2=='connect'):
                subprocess.call("docker exec -it django /bin/bash", shell=True)
                return(render(request, "thankyou.html"))
        
            elif (text2=='connectivity'):
                print("========================================================")
                test = subprocess.check_output("docker network inspect django_project_docker_django_network | grep -A 4 django | grep IPv4Address", shell=True, universal_newlines=True)
                s1 = re.compile(r'[0-9.]+/')
                m1 = s1.search(test)
                host= (m1.group(0).rstrip('/'))
                subprocess.call("nc -vz -w 5 "+ host +" 8000 ", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
            elif (text2=='logs'):
                print("========================================================")
                print("Django container logs as below : ")
                subprocess.call("docker logs django", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
        elif (text1=='elk'):
            if (text2=='create'):
                subprocess.call("echo | tee /var/log/ad.log; cd automation_devops/elk_project_docker && docker-compose up -d &", shell=True)
                text1 = "Default port for Elasticsearch is 9200. Type <IP>:9200 in the browser to access Elasticsearch"
                text2 = "Default port for Kibana is 5601. Type <IP>:5601 in the browser to access Kibana"
                return(render(request, "result1.html", {"htmlcode": "ELK Stack", "html": "CREATED", "text1": text1, "text2": text2 }))

            elif (text2=='destroy'):
                subprocess.call("cd automation_devops/elk_project_docker && docker-compose down --rmi all &", shell=True)
                subprocess.call("cp /var/log/ad.log /var/log/ad_elk.log", shell=True)
                text = "It may take few seconds to destroy the environment, Thank You"
                return(render(request, "result2.html", {"htmlcode": "ELK Stack", "html": "DESTROYED", "text": text }))
        
            elif (text2=='connect'):
                subprocess.call("docker exec -it elasticsearch /bin/bash", shell=True)
                return(render(request, "thankyou.html"))
        
            elif (text2=='connectivity'):
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
        
                test = subprocess.check_output("docker network inspect elk_project_docker_elk_network | grep -A 4 filebeat | grep IPv4Address", shell=True, universal_newlines=True)
                s1 = re.compile(r'[0-9.]+/')
                m1 = s1.search(test)
                host= (m1.group(0).rstrip('/'))
                print("========================================================")
                subprocess.call("nc -vz -w 5 "+ host +" 22 ", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
        
            elif (text2=='logs'):
                print("========================================================")
                print("Elasticsearch container logs as below : ")
                subprocess.call("docker logs elasticsearch", shell=True)
                print("========================================================")
                print("Kibana container logs as below : ")
                subprocess.call("docker logs kibana", shell=True)
                print("========================================================")
                print("Logstash container logs as below : ")
                subprocess.call("docker logs logstash", shell=True)
                print("========================================================")
                print("Filebeat container logs as below : ")
                subprocess.call("docker logs filebeat", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
        elif (text1=='prometheus'):
            if (text2=='create'):
                subprocess.call("echo | tee /var/log/ad.log; cd automation_devops/prometheus_project_docker && docker-compose up -d &", shell=True)
                text1 = "Default port for Prometheus is 9090. Type <IP>:9090 in the browser to access Prometheus"
                text2 = "Default port for Node Exporter is 9100. Type <IP>:9100 in the browser to access Node Exporter"
                text3 = "Default port for Grafana is 3000. Type <IP>:3000 in the browser to access Grafana"
                return(render(request, "result1.html", {"htmlcode": "Prometheus, Node Exporter, Grafana", "html": "CREATED", "text1": text1, "text2": text2, "text3": text3 }))
            
            elif (text2=='destroy'):
                subprocess.call("cd automation_devops/prometheus_project_docker && docker-compose down --rmi all &", shell=True)
                subprocess.call("cp /var/log/ad.log /var/log/ad_prometheus.log", shell=True)
                text = "It may take few seconds to destroy the environment, Thank You"
                return(render(request, "result2.html", {"htmlcode": "Prometheus, Node Exporter and Grafana", "html": "DESTROYED", "text": text }))

            elif (text2=='connect'):
                subprocess.call("docker exec -it prometheus /bin/bash", shell=True)
                return(render(request, "thankyou.html"))

            elif (text2=='connectivity'):
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
                return(render(request, "thankyou.html"))
        
            elif (text2=='logs'):
                print("========================================================")
                print("Prometheus container logs as below : ")
                subprocess.call("docker logs prometheus", shell=True)
                print("========================================================")
                print("Grafana container logs as below : ")
                subprocess.call("docker logs grafana", shell=True)
                print("========================================================")
                print("Node Exporter container logs as below : ")
                subprocess.call("docker logs node_exporter", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
        elif (text1=='mysql'):
            if (text2=='create'):
                subprocess.call("echo | tee /var/log/ad.log; cd automation_devops/mysql_project_docker && docker-compose up -d &", shell=True)
                text1 = "Port for phpMyAdmin is 82. Type <IP>:82 in the browser to access phpMyAdmin"
                text2 = "Login to MySQL to work on it"
                return(render(request, "result1.html", {"htmlcode": "MySQL", "html": "CREATED", "text1": text1, "text2": text2 }))

            elif (text2=='destroy'):
                text = "It may take few seconds to destroy the environment, Thank You"
                subprocess.call("cd automation_devops/mysql_project_docker && docker-compose down --rmi all &", shell=True)
                subprocess.call("cp /var/log/ad.log /var/log/ad_mysql.log", shell=True)
                return(render(request, "result2.html", {"htmlcode": "MySQL", "html": "DESTROYED", "text": text }))
        
            elif (text2=='connect'):
                subprocess.call("docker exec -it sp-mysql /bin/bash", shell=True)
                return(render(request, "thankyou.html"))
        
            elif (text2=='connectivity'):
                test = subprocess.check_output("docker network inspect mysql_project_docker_mysql_network | grep -A 4 sp_phpmyadmin | grep IPv4Address", shell=True, universal_newlines=True)
                s1 = re.compile(r'[0-9.]+/')
                m1 = s1.search(test)
                host= (m1.group(0).rstrip('/'))
                print("========================================================")
                subprocess.call("nc -vz -w 5 "+ host +" 80 ", shell=True)
                print("========================================================")

                test = subprocess.check_output("docker network inspect mysql_project_docker_mysql_network | grep -A 4 sp-mysql | grep IPv4Address", shell=True, universal_newlines=True)
                s1 = re.compile(r'[0-9.]+/')
                m1 = s1.search(test)
                host= (m1.group(0).rstrip('/'))
                print("========================================================")
                subprocess.call("nc -vz -w 5 "+ host +" 3306 ", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
            elif (text2=='logs'):
                print("========================================================")
                print("MySQL container logs as below : ")
                subprocess.call("docker logs sp-mysql", shell=True)
                print("========================================================")
                print("PHP Admin container logs as below : ")
                subprocess.call("docker logs sp_phpmyadmin", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
        elif (text1=='jenkins'):
            if (text2=='create'):
                subprocess.call("echo | tee /var/log/ad.log; cd automation_devops/jenkins_project_docker && docker-compose up -d &", shell=True)
                text1 = "Default port for Jenkins is 8080. Type <IP>:8080 in the browser to access Jenkins"
                return(render(request, "result1.html", {"htmlcode": "Jenkins", "html": "CREATED", "text1": text1 }))

            elif (text2=='destroy'):
                subprocess.call("cd automation_devops/jenkins_project_docker && docker-compose down --rmi all &", shell=True)
                subprocess.call("cp /var/log/ad.log /var/log/ad_jenkins.log", shell=True)
                text = "It may take few seconds to destroy the environment, Thank You"
                return(render(request, "result2.html", {"htmlcode": "Jenkins", "html": "DESTROYED", "text": text }))
        
            elif (text2=='connect'):
                subprocess.call("docker exec -it jenkinsserver /bin/bash", shell=True)
                return(render(request, "thankyou.html"))
        
            elif (text2=='connectivity'):
                test = subprocess.check_output("docker network inspect jenkins_project_docker_jenkins_network | grep -A 4 jenkinsserver | grep IPv4Address", shell=True, universal_newlines=True)
                s1 = re.compile(r'[0-9.]+/')
                m1 = s1.search(test)
                host= (m1.group(0).rstrip('/'))
                print("========================================================")
                subprocess.call("nc -vz -w 5 "+ host +" 8080 ", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
            elif (text2=='logs'):
                print("========================================================")
                print("Jenkins container logs as below : ")
                subprocess.call("docker logs jenkinsserver", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))
        
        elif (text1=='terraform'):
            if (text2=='create'):
                subprocess.call("echo | tee /var/log/ad.log; cd automation_devops/terraform_project_docker && docker-compose up -d &", shell=True)
                text1 = "Terraform environment is getting created, Login to work on it"
                return(render(request, "result1.html", {"htmlcode": "Terraform", "html": "CREATED", "text1": text1 }))

            elif (text2=='destroy'):
                subprocess.call("cd automation_devops/terraform_project_docker && docker-compose down --rmi all &", shell=True)
                subprocess.call("cp /var/log/ad.log /var/log/ad_terraform.log", shell=True)
                text = "It may take few seconds to destroy the environment, Thank You"
                return(render(request, "result2.html", {"htmlcode": "Terraform", "html": "DESTROYED", "text": text }))

            elif (text2=='connect'):
                subprocess.call("docker exec -it terraform /bin/bash", shell=True)
                return(render(request, "thankyou.html"))
        
            elif (text2=='connectivity'):
                print("========================================================")
                print("Terraform is not running as service, hence it will not open any port. It is just Software.")
                print("========================================================")
                return(render(request, "thankyou.html"))
        
            elif (text2=='logs'):
                print("========================================================")
                print("Terraform container logs as below : ")
                subprocess.call("docker logs terraform", shell=True)
                print("========================================================")
                return(render(request, "thankyou.html"))


        # html generated code is coming from this function
        # htmlcode = formatHtml("\n\n"+text1+"\n\n")
        #print(htmlcode)


        #return(render(request, "result.html", {"htmlcode": str(htmlcode), "html": lines}))
        #return(render(request, "result.html", {"htmlcode": str(text1), "html": str(text2)}))
        #return(render(request, "result1.html", {"htmlcode": "Apache", "html": "CREATED"}))
    else:
        #htmlcode = "<h2>Oops there seems some problem, Please go back and resumit your Text</h2>"
        #return(HttpResponse(htmlcode))
        
        '''def countdown():
            t = 10
            while t:
                mins, secs = divmod(t, 60)
                timer = '{:02d}:{:02d}'.format(mins, secs)
                #print(timer, end="\r")
                time.sleep(1)
                t -= 1
                return(render(request, "result.html", {"htmlcode": 'Nidhi', "html": timer}))
            print('Times up !!!')

        countdown()'''
        return(render(request, "thankyou.html"))

def logs(request):
    with open("/var/log/ad.log", 'r') as f:
        lines = f.read()
    
    return(render(request, "result.html", {"htmlcode": "RAM", "html": "SHYAM", "lines": lines}))

