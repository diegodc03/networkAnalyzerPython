import socket
import sys
import multiprocessing
import time

PORT_MAX = 65535
PORT_MIN = 0

s = None

def scan_ports(queue, sharedDict, ip, portMin, portMax, protocol):
    
    
    for port in range(portMin,portMax+1):
        if protocol == 'TCP':
            status = scan_tcp_port(ip, port)
        else:
            status = scan_udp_port(ip, port)
       
        if status != "closed":
            #dicPorts[port] = status
            sharedDict[port] = status

        
        queue.put(1)

        
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

    print(f"\nThe execution time is: {executionTime}\n")
    print("The ports open and filtered are in the .txt file on the same folder of this program was executed")

    #for port in dicPorts:
    #    print(f"Port {port}/{protocol} on {ip} is {dicPorts[port]}")


def fileWithTheAccesiblePorts(ip, protocol, portMin, portMax, dicPorts, executionTime, numProcess):
    f = open (f"{ip}_{protocol}_NumProcess_{numProcess}_Ports_{portMin}_{portMax}Paralel.txt",'w')
    
    f.write(f"All the ports open between {portMin}-{portMax}\n\n")
    f.write(f"Execution time: {executionTime}\n")
    for port in dicPorts:
        f.write(f"Port {port}/{protocol} on {ip} is {dicPorts[port]}\n")
    
    f.close()


# q es el puntero a la cola
def porcentajeUsed(q,portMax, portMin):
    print("porcentaje Completed")

    totalPorts = portMax - portMin + 1

    progressList = []
    total = portMin


    # Read results from the queue
    while True:
        var = q.get()  
        total = total + 1

        portAnalyzing = total - portMin + 1
        portcent = portAnalyzing/totalPorts
       
        num_hashes = int(50 * portcent)
    
        # Rellena la lista de progreso con '#'
        progressList = ['#'] * num_hashes + ['-'] * (50 - num_hashes)

        stringProgress = "".join(progressList)

        print(f"[{stringProgress}]{num_hashes*2}%", end='\r')

        if num_hashes >= 50:
            break


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


        if PORT_MIN < portMin < portMax < PORT_MAX and num_process >= 2:
            if protocol in {"TCP", "UDP"}:
                    
                # Declaramos la cola, para asi poder comunicarnos entre procesos
                q = multiprocessing.Queue()
                # Declaramos la memoria compartida, en este caso un diccionario compartido
                manager = multiprocessing.Manager()
                sharedDict = manager.dict()

                # Primer proceso lo usamos para el porcentaje
                processPercent = multiprocessing.Process(target=porcentajeUsed, args=(q, portMax, portMin))
                processPercent.start()
                    
                processes = []

                rangePorts = portMax - portMin + 1
                step = rangePorts // num_process

                for i in range(num_process):

                    startPort = portMin + i * step
                    endPort = portMin + (i + 1) * step - 1
                        
                    if i == num_process-1:
                        endPort = portMax
                            
                    args = (q, sharedDict, ip, startPort, endPort, protocol)
                    p = multiprocessing.Process(target=scan_ports, args=args)
                    p.start()
                    processes.append(p)

                # Esperamos a que todos los procesos terminen
                for proc in processes:
                    proc.join()

                processPercent.join()
                   
                #ordenamos el diccionario
                sharedDict_Ord = dict(sorted(sharedDict.items()))
                finalExecutionTime = time.time()
                executionTime = finalExecutionTime - executionStartTime
                    
                printListOfPorts(sharedDict_Ord, protocol, ip, executionTime)
                fileWithTheAccesiblePorts(ip,protocol, portMin, portMax, sharedDict_Ord, executionTime, num_process)

                sys.exit()

            else:
                print("Put correct arguments, only TCP or UDP must be on the fifth argument\n")
                print("./nameOfProgramm <ipToAnalize> <PortMin> <PortMax> <Protocolo TCP/UDP> <numProcess >=2 >\n\n")

        else:
            print("Put correct arguments, the portMin number mast be less than maxPort\n")
            print("./nameOfProgramm <ipToAnalize> <PortMin> <PortMax> <Protocolo TCP/UDP> <numProcess >=2 >\n\n")
            
    else:
        print("Put correct arguments, the arguments have to be 6\n")
        print("./nameOfProgramm <ipToAnalize> <PortMin> <PortMax> <Protocolo TCP/UDP> <numProcess>\n\n")
    
# Verificación si este archivo se ejecuta como el programa principal
if __name__ == "__main__":
    main()

    
