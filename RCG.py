#[MLFT] Candidate Question1
#Author: Yi Yang
#Date: 2018/08/02
#Version: python 3.5

import random,queue,time,threading

class Random_Count_Generator(threading.Thread):#The thread to generate numbers
    def __init__(self,name,delay):
        threading.Thread.__init__(self)
        global history
        global logs
        self.name=name
        self.probs=[0.5,0.25,0.15,0.05,0.05]
        self.lock=threading.Lock()
        self.delay=delay
    def run(self):
        for i in range(2000):#Assume each thread will generate 2000 numbers
            time.sleep(self.delay)
            with self.lock:
                r=random.random()
                timestamp=time.time()
                index=0
                while(r>=0 and index<len(self.probs)):
                  r-=self.probs[index]
                  index+=1
                if history.full():
                    history.get()
                history.put(index)      
                logs.put("Number generated:"+str(index)+"  Time:"+str(timestamp)+"  Thread name:"+str(threading.current_thread().name)+"\n")      
#            print(index)   
                
class Write(threading.Thread):#The thread to write into disk
    def __init__(self,name):
        threading.Thread.__init__(self)
        global history
        global logs 
        self.file=open("data.txt","a+")
        self.name=name          
    def run(self):
        try:                
            while True:
                text=logs.get(True,1)#time_out==1s
                self.file.write(text)
        except:#All data has been written into the file
            self.file.close()
            print ("Frequency percentages of each number for the last 100 numbers:",self.return_frequency())
    def return_frequency(self):#Return the frequency percentages of each number for the last 100 numbers
        fq={}
        count_list=[0]*5
        while not history.empty():
            get=history.get()
            if get==1:
                count_list[0]+=1
            elif get==2:
                count_list[1]+=1
            elif get==3:
                count_list[2]+=1
            elif get==4:
                count_list[3]+=1
            elif get==5:
                count_list[4]+=1           
        total=sum(count_list)      
        for idx,val in enumerate(count_list,start=1):
            fq[idx]=float(val)/total
        return fq                 
        
if __name__ == "__main__":  
    open('data.txt', 'w').close()
    history=queue.Queue(maxsize=100)#The queue to store the most last 100 numbers, used in part 2
    logs=queue.Queue(maxsize=0)#The queue to store numbers, timestamps and the thread name(for convenience)
    thread1=Random_Count_Generator("Thread-1",0)#Assume the delay time for each generation is 0s
    thread2=Random_Count_Generator("Thread-2",0)
    thread3=Random_Count_Generator("Thread-3",0)
    thread4=Random_Count_Generator("Thread-4",0)
    thread5=Random_Count_Generator("Thread-5",0)
    threadW=Write("Thread-W")
    #Run the threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    threadW.start()
