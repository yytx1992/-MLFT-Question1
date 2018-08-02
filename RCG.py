#[MLFT] Candidate Question1
#Author: Yi Yang
#Date: 2018/08/01
#Version: python 3.5
import random,queue,time,threading
class Random_Count_Generator:
    def __init__(self):
        self.generator=0
        self.history=queue.Queue(maxsize=100)#The queue to store the most last 100 numbers, used in part 2
        self.probs=[0.5,0.25,0.15,0.05,0.05]
        self.logs=queue.Queue(maxsize=0)#The queue to store numbers, timestamps and the thread name(for convenience)
        self.lock=threading.Lock()
    def print_random_num(self,delay):#The thread to generate numbers
        for i in range(2000):#Assume each thread will generate 2000 numbers
            time.sleep(delay)
            with self.lock:
                r=random.random()
                timestamp=time.time()
                index=0
                while(r>=0 and index<len(self.probs)):
                  r-=self.probs[index]
                  index+=1
                if self.history.full():
                    self.history.get()
                self.history.put(index)      
                self.logs.put("Number generated:"+str(index)+"  Time:"+str(timestamp)+"  Thread name:"+str(threading.current_thread().name)+"\n")      
#            print(index)               
    def write_to_disk(self):#The thread to write into disk
        self.file=open("data.txt","a+")
        count=0
        try:                
            while True:
                text=self.logs.get(True,1)#time_out==1s
                self.file.write(text)
                count+=1
        except:#All data has been written into the file
#            print ("Total count:",count)
            self.file.close()
            print ("Frequency percentages of each number for the last 100 numbers:",self.return_frequency())
    def return_frequency(self):#Return the frequency percentages of each number for the last 100 numbers
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
        for idx,val in enumerate(count,start=1):
            fq[idx]=float(val)/total
        return fq          
    def run(self):#Build threads and run them
        t1=threading.Thread(target=self.print_random_num,name="t1",args=(0,))#Assume the delay time for each generation is 0s
        t2=threading.Thread(target=self.print_random_num,name="t2",args=(0,))
        t3=threading.Thread(target=self.print_random_num,name="t3",args=(0,))
        t4=threading.Thread(target=self.print_random_num,name="t4",args=(0,))
        t5=threading.Thread(target=self.print_random_num,name="t5",args=(0,))    
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
