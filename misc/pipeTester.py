from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    var = parent_conn.recv()
    print var
    if(var == None):
        print "Confirmed"
    else:
        print "Nope"
    #p.start()
    #print parent_conn.recv()   # prints "[42, None, 'hello']"
    #p.join()
