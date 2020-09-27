# importing all the needed libraries
# Process and Pipe - for implementing multiprocess communicationg
# datetime to see the real time of process execution

from multiprocessing import Process, Pipe
from datetime import datetime

# function to represent the real and Lamport times 
# in a more visual way

def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter,
                                                     datetime.now())

# digit by digit generating and assigning
# a new timestamp for a new event or action
# in a specific process

def calc_recv_timestamp(recv_time_stamp, counter):
    for id  in range(len(counter)):
        counter[id] = max(recv_time_stamp[id], counter[id])
    return counter

# implementing a simple event function
# which moves the counter[pid] by 1

def event(pid, counter):
    counter[pid] += 1
    print('Something happened in {} !'.\
          format(pid) + local_time(counter))
    return counter

# implementing function to send data through
# pipe between two processes
# with increasing the vector stamp

def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter

# implementing function to recieve data through
# pipe between two processes
# with increasing the vector stamp

def recv_message(pipe, pid, counter):
    counter[pid] += 1
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid)  + local_time(counter))
    return counter

# defining the behaviour of processes
# so that it corelates with the picture
# from the assignment

# also not forgetting to assign custom 0, 1, and 2 
# PIDs to the processes and nullifying the initial vector stamps

def process_one(pipe12):
    pid = 0
    counter = [0,0,0]
    
    counter = send_message(pipe12, pid, counter)
    counter = send_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    counter = event(pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe12, pid, counter)
    
def process_two(pipe21, pipe23):
    pid = 1
    counter = [0,0,0]
    
    counter = recv_message(pipe21, pid, counter)
    counter = recv_message(pipe21, pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = recv_message(pipe23, pid, counter)
    counter = event(pid, counter)
    counter = send_message(pipe21, pid, counter)
    counter = send_message(pipe23, pid, counter)
    counter = send_message(pipe23, pid, counter)
    
def process_three(pipe32):
    pid = 2
    counter = [0,0,0]
    
    counter = send_message(pipe32, pid, counter)
    counter = recv_message(pipe32, pid, counter)
    counter = event(pid, counter)
    counter = recv_message(pipe32, pid, counter)

# defining pipes that we are going to use 
# to enable multiprocess communication

oneandtwo, twoandone = Pipe()
twoandthree, threeandtwo = Pipe()

# creating the processes with the defined behaviour

process1 = Process(target=process_one, 
                   args=(oneandtwo,))
process2 = Process(target=process_two, 
                   args=(twoandone, twoandthree))
process3 = Process(target=process_three, 
                   args=(threeandtwo,))

# starting the processes

process1.start()
process2.start()
process3.start()

# waiting till all processes are completed
# before quitting

process1.join()
process2.join()
process3.join()
