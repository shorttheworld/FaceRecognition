import os

if __name__ == '__main__':
    if(os.path.isdir(os.getcwd() + "\\test")):
        print "Check"
    else:
        os.mkdir(os.getcwd() + "\\test");
