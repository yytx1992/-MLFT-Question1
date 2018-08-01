import random,queue,time,threading


class Random_Count_Generator:
    def __init__(self):
        self.generator=0
        self.history=queue.Queue(maxsize=100)
        self.probs=[0.5,0.25,0.15,0.05,0.05]
        self.logs=queue.Queue(maxsize=0)
    def print_random_num(self):
        if self.history.full():
            self.history.get()
        r=random.random()
        timestamp=time.time()
        index=0
        while(r>=0 and index<len(self.probs)):
          r-=self.probs[index]
          index+=1
        self.history.put(index)
        timestamp=time.time()        
        print(index)
        self.logs.put(str(index)+"__"+str(timestamp)+"\n")
        
#        self.write_to_disk(index)
        
    def write_to_disk(self):
        self.file=open("data.txt","a+")
#        print(number)
#        text=str(number)+"__"+str(time.time())+"\n"
#        print(text)
        if not self.logs.empty():
            text=self.logs.get()
            self.file.write(text)
        self.file.close()
        
    def return_frequency(self):
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
#        self.last=get
        total=sum(count)
        print(total)
        for i in count:
            print(i/total)
#        print("last:",self.last)
        
        

if __name__ == "__main__":  
    open('data.txt', 'w').close()
    RCG=Random_Count_Generator()
    for i in range(101):
        RCG.print_random_num()
        RCG.write_to_disk()
        
    RCG.return_frequency()
    
    #print("$$$$$$$")
    #print(RCG.history.get())
    #print(RCG.history.get())
    #print(RCG.history.get())
