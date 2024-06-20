
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


def printListOfPorts(dicPorts, protocol, ip, executionTime):

    print(f"The execution time is: {executionTime}")

    #for port in dicPorts:
    #    print(f"Port {port}/{protocol} on {ip} is {dicPorts[port]}")


def fileWithTheAccesiblePorts(ip, protocol, portMin, portMax, dicPorts, executionTime, numProcess):
    f = open (f"{ip}_{protocol}_NumProcess{numProcess}_Ports{portMin}_{portMax}.txt",'w')
    
    f.write(f"All the ports open between {portMin}-{portMax}\n\n")
    f.write(f"Execution time: {executionTime}\n")
    for port in dicPorts:
        f.write(f"Port {port}/{protocol} on {ip} is {dicPorts[port]}\n")
    
    f.close()


def main():

    executionStartTime = time.time()

    num_process = 0
    
    if len(sys.argv) == 6:
        ip=sys.argv[1] 
        portMin=int(sys.argv[2])
        portMax=int(sys.argv[3])
        protocol = sys.argv[4]
        num_process = int(sys.argv[5])

        protocol = protocol.upper()

        ranges = []

        if PORT_MIN < portMin < portMax < PORT_MAX and num_process >= 2:
            if protocol in {"TCP", "UDP"}:
                    
                #Dividimos el rango de puertos en 4 partes
                rangePorts = portMax - portMin + 1
                #Tenemos el numero de rango puertos a escanear por cada proceso
                step = rangePorts // num_process

                #usamos una lista que tiene dentro una tupla cada elemento
                ranges = [(ip, portMin + i * step, portMin + (i + 1) * step - 1, protocol) for i in range(num_process)] 
                ranges[-1] = (ip, portMin + (num_process - 1) * step, portMax, protocol)

                with multiprocessing.Pool(processes=num_process) as pool:
                    dicOfPorts = pool.map( scan_ports, ranges)

                # Conseguimos tener un único diccionario
                openPorts = {}
                for result in dicOfPorts:
                   openPorts.update(result)

                finalExecutionTime = time.time()

                executionTime = finalExecutionTime - executionStartTime
                    
                printListOfPorts(openPorts, protocol, ip, executionTime)

                #Añadir a un fichero .txt
                fileWithTheAccesiblePorts(ip,protocol, portMin, portMax, openPorts, executionTime, num_process)

                sys.exit()

            else:
                print("Put correct arguments, only TCP or UDP must be on the fifth argument\n")
                print("./nameOfProgramm <ipToAnalize> <PortMin> <PortMax> <Protocolo TCP/UDP> <numProcess >=2 >\n\n")

        else:
            print("Put correct arguments, the portMin number mast be less than maxPort and numProcess >= 2\n")
            print("./nameOfProgramm <ipToAnalize> <PortMin> <PortMax> <Protocolo TCP/UDP> <numProcess >=2 >\n\n")
            
    else:
        print("Put correct arguments, the arguments have to be 6\n")
        print("./nameOfProgramm <ipToAnalize> <PortMin> <PortMax> <Protocolo TCP/UDP> <numProcess>\n\n")

    
# Verificación si este archivo se ejecuta como el programa principal
if __name__ == "__main__":
    main()

    







