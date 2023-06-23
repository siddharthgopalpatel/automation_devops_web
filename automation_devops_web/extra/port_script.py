import subprocess
import datetime

def docker_container_func():
    # Getting result from container
    count = subprocess.check_output("docker ps --format '{{.Names}}' | wc -l", shell=True, universal_newlines=True)

    for i in range(int(count.strip())):
        j = str(i + 1)
        #print("==========================================================================================================")
        docker_name = subprocess.check_output("docker ps --format '{{.Names}}' | head -"+ j +" | tail -1", shell=True, universal_newlines=True)
        #print(docker_name.strip())
        port_command = subprocess.check_output("docker exec -it "+ docker_name.strip() +" netstat -ltnp | grep -v Active | grep -v Proto", shell=True, universal_newlines=True)
        #print(port_command.strip())
        #print("==========================================================================================================")

        #Get_Time
        b1 = datetime.datetime.now()
        b2 = b1.strftime("%X")
        b3 = b1.strftime("%x")
        b4 = b1.strftime("%Y")
        b5 = b1.strftime("%m")
        b6 = b1.strftime("%d")
        b7 = b1.strftime("%H")
        b8 = b1.strftime("%M")
        b9 = b1.strftime("%S")

        # File_Write():
        f = open("logs/port_ad.log", "a+")
        f.write("==========================================================================================================\n")
        f.write(""+ b3 +" "+ b2 +" "+ docker_name +"")
        f.write(""+ port_command +"")
        f.write("==========================================================================================================\n")
        f.close()

        # Log_Mng():
        c1 = subprocess.check_output("ls -ltr logs/port_ad.log | awk '{print $5}'", shell=True)
        if (int(c1) >= 20000):
                subprocess.check_output("mv logs/port_ad.log logs/port_ad.log"+b4+""+b5+""+b6+""+b7+""+b8+""+b9+"", shell=True)
        c2 = subprocess.check_output("find logs/port_ad.log* -mtime +7 -exec rm -rf {} \;", shell=True)
       
docker_container_func()
