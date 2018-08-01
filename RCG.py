#[MLFT] Candidate Question1
#Author: Yi Yang
#Date: 2018/08/01
#Version: python 3.5
import random,queue,time,threading
class Random_Count_Generator:
    def __init__(self):
        self.generator=0
        self.history=queue.Queue(maxsize=100)
        self.probs=[0.5,0.25,0.15,0.05,0.05]
        self.logs=queue.Queue(maxsize=0)
        self.lock=threading.Lock()
    def print_random_num(self,delay,stop):
        for i in range(2000):
            time.sleep(delay)
            with self.lock:
                r=random.random()
                timestamp=time.time()#time.ctime(time.time())
                index=0
                while(r>=0 and index<len(self.probs)):
                  r-=self.probs[index]
                  index+=1
                if self.history.full():
                    self.history.get()
                self.history.put(index)      
                self.logs.put("Number generated:"+str(index)+"  Time:"+str(timestamp)+"  Thread name:"+str(threading.current_thread().name)+"\n")   
#            print(index)
        stop.set()                
    def write_to_disk(self):
        self.file=open("data.txt","a+")
        count=0
        while not (self.logs.empty() and self.stop_event1.is_set() and self.stop_event2.is_set() and self.stop_event3.is_set() and self.stop_event4.is_set() and self.stop_event5.is_set()):
            while not self.logs.empty():
                text=self.logs.get()
                self.file.write(text)
                count+=1
        self.file.close()
        print(self.return_frequency())
    def return_frequency(self):
        fq={}
        count=[0]*5
        while not self.history.empty():
            get=self.history.get()
            if get==1:
                count[0]+=1
            elif get==2:
                count[1]+=1
            elif get==3:
                count[2]+=1
            elif get==4:
                count[3]+=1
            elif get==5:
                count[4]+=1           
        total=sum(count)
#        print("Amount of the last 100 number generated:",total)
        print ("Frequency percentages of each number for the last 100 numbers:")
        for idx,val in enumerate(count,start=1):
            fq[idx]=float(val)/total
        return fq
#        for i in count:
#            print(i/total)            
    def run(self):
        self.stop_event1=threading.Event()
        self.stop_event2=threading.Event()
        self.stop_event3=threading.Event()
        self.stop_event4=threading.Event()
        self.stop_event5=threading.Event()
        t1=threading.Thread(target=self.print_random_num,name="t1",args=(0,self.stop_event1))
        t2=threading.Thread(target=self.print_random_num,name="t2",args=(0,self.stop_event2))
        t3=threading.Thread(target=self.print_random_num,name="t3",args=(0,self.stop_event3))
        t4=threading.Thread(target=self.print_random_num,name="t4",args=(0,self.stop_event4))
        t5=threading.Thread(target=self.print_random_num,name="t5",args=(0,self.stop_event5))    
        w=threading.Thread(target=self.write_to_disk,name="w")
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        w.start()        
        
if __name__ == "__main__":  
    open('data.txt', 'w').close()
    RCG=Random_Count_Generator()
    RCG.run()
