from multiprocessing import Process, Pool, Queue
import random

def main():
    
    p = Pool(processes=3) #Starts a pool of 3 processes that can work asyncronously
    result = p.apply_async(count, [0]) #Evaluates count(0), stores to result
    print result.get(timeout=1) #Prints the results of the previous operation
    
    print p.map(count, [0, 10, 20]) #Prints count(0), count(10), count(20)
                                    #I think this method blocks...?    
    print '--------------------------------'
    
    p1 = Process(target=count, args=(1,))
    p1.start()  #Runs the thread; doesnt seem to do print statements or be
                #capable of returning, but still runs the self-contained method
    print p1 #Prints process name and status (started)
    p1.join()
    print p1 #Prints process name and status (started)

    q = Queue() #Fun with queues! Just to make sure the Process is executing
    p2 = Process(target=queueIt, args=(q,))
    p2.start()
    print q.get()
    p2.join()
    print q.get()
    

def count(start):
    l = []
    for num in range(10):
        l.append(start + num)
        print(start + num) #Doesn't execute when done in a thread??
    return l

def queueIt(q):
    q.put([random.randint(1, 10), None, 'It worked!'])

if __name__ == '__main__':
    main()
    
    
