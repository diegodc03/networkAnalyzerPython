
import socket
import sys
import multiprocessing
import time

PORT_MAX = 65535
PORT_MIN = 0

s = None

def scan_ports(args):
    ip, portMin, portMax, protocol = args
    dicPorts = {}
    for port in range(portMin,portMax+1):
        if protocol == 'TCP':
            status = scan_tcp_port(ip, port)
        else:
            status = scan_udp_port(ip, port)
       
        if status != "closed":
            dicPorts[port] = status

    return dicPorts
        

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


def printListOfPorts(dicPorts, protocol, ip):

    for port in dicPorts:
        print(f"Port {port}/{protocol} on {ip} is {dicPorts[port]}")


def fileWithTheAccesiblePorts(ip, protocol, portMin, portMax, openPorts, executionTime):
    f = open (f"{ip}_{protocol}_{portMin}_{portMax}.txt",'w')
    
    f.write(f"All the ports open between {portMin}-{portMax}")
    f.write(f"Execution time: {executionTime}")
    for port in openPorts:
        f.write(f"Port {port}/{protocol} on {ip} is {openPorts[port]}")
    
    f.close()


def main():

    executionStartTime = time.time

    max_attempts = 5
    num_attempts = 1

    num_process = 4
    dicPorts={}
    
    tupletype = ()

    while(num_attempts <= max_attempts):

        if len(sys.argv) == 5:
            ip=sys.argv[1] 
            portMin=int(sys.argv[2])
            portMax=int(sys.argv[3])
            protocol = sys.argv[4]

            protocol = protocol.upper()

            ranges = []

            if PORT_MIN < portMin < portMax < PORT_MAX:
                if protocol in {"TCP", "UDP"}:
                    
                    #Dividimos el rango de puertos en 4 partes
                    rangePorts = portMax - portMin + 1
                    #Tenemos el numero de rango puertos a escanear por cada proceso
                    step = rangePorts // num_process

                    #usamos una lista que tiene dentro una tupla cada elemento
                    ranges = [(ip, portMin + i * step, portMin + (i + 1) * step - 1, protocol) for i in range(num_process)] 
                    ranges[-1] = (ip, portMin + (num_process - 1) * step, portMax, protocol)

                    with multiprocessing.Pool(processes=num_process) as pool:
                        listOfPorts = pool.map( scan_ports, ranges)

                    # Conseguimos tener un único diccionario
                    open_ports = {}
                    for result in listOfPorts:
                       open_ports.extend(result)

                    finalExecutionTime = time.time

                    executionTime = executionStartTime - finalExecutionTime
                    
                    printListOfPorts(dicPorts, protocol, ip, executionTime)

                    #Añadir a un fichero .txt
                    fileWithTheAccesiblePorts(ip,protocol, portMin, portMax, open_ports)

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

    







