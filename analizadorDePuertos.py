
import socket
import sys
import time

PORT_MAX = 65535
PORT_MIN = 0

s = None

def scan_ports(ip, portMin, portMax, protocol, listPorts):

    totalPorts = portMax - portMin + 1

    progressList = []
    
    b=0
    for port in range(portMin,portMax+1):

        if protocol == 'TCP':
            status = scan_tcp_port(ip, port)
        else:
            status = scan_udp_port(ip, port)
       
        if status != "closed":
            listPorts[port] = status
        
       
        portAnalyzing = port - portMin + 1
        portcent = portAnalyzing/totalPorts
       
        num_hashes = int(50 * portcent)

        # Rellena la lista de progreso con '#'
        progressList = ['#'] * num_hashes + ['-'] * (50 - num_hashes)

        cadena = "".join(progressList)

        print(f"[{cadena}]{num_hashes*2}%", end='\r')


def scan_tcp_port(ip, port):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    if result == 0:
        return "open"

    elif result == 11:
        return "filtered"
    else:
        return "closed"



def scan_udp_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    try:
        sock.sendto(b"", (ip, port))
        data, _ = sock.recvfrom(1024)
        sock.close()
        return "open"
    except socket.timeout:
        return "filtered"
    except Exception:
        return "closed"


def printListOfPorts(dicPorts, protocol, ip, executionTime):
    #print("Lista de puertos abiertos\n")
    print(f"\nTiempo de ejecucion: {executionTime}\n\n")
    #for port in dicPorts:
    #    print(f"Port {port}/{protocol} on {ip} is {dicPorts[port]}-NoParalelism\n")


def fileWithTheAccesiblePorts(ip, protocol, portMin, portMax, dicPorts, executionTime):
    f = open (f"{ip}_{protocol}_{portMin}_{portMax}.txt",'w')
    
    f.write(f"All the ports open between {portMin}-{portMax}\n\n")
    f.write(f"Execution time: {executionTime}\n")
    for port in dicPorts:
        f.write(f"Port {port}/{protocol} on {ip} is {dicPorts[port]}\n")
    
    f.close()


def main():

    executionStartTime = time.time()

    max_attempts = 5
    num_attempts = 1

    dicPorts={}
  
    while(num_attempts <= max_attempts):

        if len(sys.argv) == 5:
            ip=sys.argv[1] 
            portMin=int(sys.argv[2])
            portMax=int(sys.argv[3])
            protocol = sys.argv[4]

            protocol = protocol.upper()

            if PORT_MIN < portMin < portMax < PORT_MAX:
                if protocol in {"TCP", "UDP"}:
                    scan_ports(ip, portMin, portMax, protocol, dicPorts)

                    finalExecutionTime = time.time()
                    executionTime = finalExecutionTime - executionStartTime

                    printListOfPorts(dicPorts, protocol, ip, executionTime)
                    fileWithTheAccesiblePorts(ip, protocol, portMin, portMax, dicPorts, executionTime)

                    sys.exit()
                else:
                    num_attempts += 1
                    print("Put correct arguments\n")
                    print("./nameOfProgramm <ipToAnalize> <PortMin> <PortMax> <Protocolo TCP/UDP> \n\n")
            
        else:
            num_attempts += 1
            print("Put correct arguments\n")
            print("./nameOfProgramm <ipToAnalize> <PortMin> <PortMax> <Protocolo TCP/UDP> \n\n")

    


# Verificación si este archivo se ejecuta como el programa principal
if __name__ == "__main__":
    main()

    







