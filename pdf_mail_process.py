from time import sleep
import sys
from createPDF import *
from SMTP import *



def main(arg):

     if arg == "KR":
          createpdf("KR")
          
          sleep(3)
          
          createpdf("Jennifer")
       
          send_email(arg)
         
          return arg

     
     else:
               
          createpdf(arg)

          sleep(10)

          send_email(arg)
          
          return arg

def a():

     createpdf("CN")
     send_email("CN")


if __name__ == '__main__':
    
     arg = sys.argv[1]
     main(arg) 
     #a()