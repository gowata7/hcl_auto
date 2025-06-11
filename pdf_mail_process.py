from time import sleep
import sys
from createPDF import *
from SMTP import *
# from x_config import *
# from vm_1  import *
# from volume_2 import *
# from capture_3 import *
# from proxmox_4 import *
# from lb_5 import *

def main(arg):

     if arg == "KR":
          # createpdf("KR")
          # sleep(3)
          # createpdf("Jennifer")
          # send_email(arg)
          return arg

     else:
          createpdf(arg)
          sleep(10)
          send_email(arg)
          return arg

if __name__ == '__main__':
     arg = sys.argv[1]
     main(arg) 
     #a()