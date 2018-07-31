import random,queue,time


class Random_Count_Generator:
    def __init__(self):
        self.generator=0
        self.history=queue.Queue(maxsize=100)
        self.probs=[0.5,0.25,0.15,0.05,0.05]
        
    def print_random_num(self):
        if self.history.full():
            self.history.get()
        r=random.random()
        index=0
        while(r>=0 and index<len(self.probs)):
          r-=self.probs[index]
          index+=1
        self.history.put(index)
#        print(index)
        self.write_to_disk(index)
    def write_to_disk(self,number):
        self.file=open("data.txt","w+")
#        print(number)
        text=str(number)+"__"+str(time.time())+"\n"
#        print(text)
        self.file.write(text)
        self.file.close()
    def return_frequency(self):
        count1=0
        count2=0
        count3=0
        count4=0
        count5=0
        while self.history.empty()==False:
            get=self.history.get()
            if get==1:
                count1+=1
            elif get==2:
                count2+=1
            elif get==3:
                count3+=1
            elif get==4:
                count4+=1
            elif get==5:
                count5+=1    
        self.last=get
        total=count1+count2+count3+count4+count5
#        print(total)
        print (count1/total,count2/total,count3/total,count4/total,count5/total)
#        print("last:",self.last)
    

    
RCG=Random_Count_Generator()
for i in range(5000):
    RCG.print_random_num()
    
RCG.return_frequency()

#print("$$$$$$$")
#print(RCG.history.get())
#print(RCG.history.get())
#print(RCG.history.get())
