import nmap3
import socket
nmap = nmap3.Nmap()

target = []
with open('masterlist.txt','r') as f:
    for line in f:
        line = line.replace("\n", "")
        if line not in target and len(line)>0:
            target.append(line)

print(target)

class Nmap():

    def __init__(self):
        self.check = []
        self.find = []

    def file_all(self,file_output):
        with open('active_assets_details.txt', "a") as fh:
            fh.write(file_output)

    def file(self,file_output):
        if self.check.count(file_output.strip('\n'))==1:
            with open('active_assets_list.txt', "a") as fh:
                fh.write(file_output)

    def scanner(self):
        nmap = nmap3.NmapScanTechniques()

        for i in target:
            print(i)
            try:
                host = socket.gethostbyname(i)
                if host not in self.find:
                    self.find.append(host) 
                    result = nmap.nmap_tcp_scan(host, args="-sV -Pn -p 1-1000,3389,3306,9200,9300,5432,5900,27017")
                    v = 0
                    for j in result[host]['ports']:
                        if 'version' in result[host]['ports'][v]['service']:
                            file_output = j['protocol'] +' '+j['portid'] +' '+ host+"\n"
                            print(file_output)
                            self.file_all(file_output)
                            file_output = host+"\n"
                            self.check.append(file_output.strip('\n'))
                           # print(file_output)
                            self.file(file_output)

                        elif j['state'] == 'filtered':
                            pass
                        else:
                            file_output = j['protocol'] +' '+j['portid'] +' '+ host+"\n"
                            print(file_output)
                            self.file_all(file_output)
                            file_output =host+"\n"
                            self.check.append(file_output.strip('\n'))
                           # print(file_output)
                            self.file(file_output)
                        v+=1
                    print('==================================================================')
            except Exception as e:
                print(e)
                #pass
        print('Assets list Created by Port Scanning')
