This project analizes all the ports you want per console
There are three files:
  - analizadorDePuertos.py
      This file doesn't use paralelism,
      Use a progress bar so the user can see how much time is left until the scan is complete.

  - analizadorDePuertosParalelismo.py
      This file uses paralelism
      All the process scans the same number of ports --> used pool.map
    
  - analizDePuertosParalelConBarraDeTiempo.py
      This file uses paralelism
      One process is used to keep the progress bar updated, all processes send it their process scaning ports.
      When the port scanning process finishes, it sends a message, the message is saved to a queue and the progress bar process get out of the queue and add to the progress bar.

      The other processes are used to scan de ports.

      To place in a .txt file we use a shared memory. All the process add to dictionary the ports filtered or open. After all process have
        finished, the parent process sort the dictionary and places in the .txt
