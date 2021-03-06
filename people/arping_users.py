#!/usr/bin/python
import subprocess,re,logging,sys

from arping import arpingy
from multiprocessing import Pool
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("main")
DEV='eth0'
MAC_NAMES='mac_names.lst'
data = []
my_addr = False
my_names = {}
ret = {}
quiet=False

if len(sys.argv) > 1 and sys.argv[1] == 'q':
  quiet=True
def get_own_addr():
  data = subprocess.Popen(['/sbin/ifconfig',DEV], 
      stdout=subprocess.PIPE).communicate()[0].replace('\n','')
  return re.sub(r'.*HWaddr ([0-9A-Fa-f:]*).*inet addr:([0-9.]*).*' ,
      r'\1 \2',data).split()

def load_names(mac_file):
  names = {}
  f = open(mac_file)
  for l in f:
    mac,name = l.split(' ',1)
    names[mac] = name.replace('\n','')
  f.close()
  return names
def print_config():
  log.info("My Addr : %s" %str(my_addr))
  log.info("MAC Names file: %s " %MAC_NAMES)
  log.debug("Loaded names : ")
  for mac,name in my_names.iteritems():
    log.debug("%s => %s" %(mac,name))
def init():
  my_addr = get_own_addr()
  my_names = load_names(MAC_NAMES)

def main():
  init()
  print_config()
  exit(0)
  def arping_helper(dic):
    return arpingy(**dic)

for first in range(1,4):
  for second in range(256):
    data.append({'iprange':'10.42.'+str(first)+'.'+str(second),'iface':DEV})

  try:
    p = Pool(20)
    ret = filter(lambda x:x , p.map(arping_helper, data))
    myip,mymac = get_own_addr()
    ret.append([mymac,myip])
    p.terminate()
  except Exception as e:
    print 'you fail '+str(e)



  for p in ret:
    if not quiet:
      print p[0] + " => " + p[1]
    if p[1] in names:
      print names[p[1]]+ " is online"
if __name__ == "__main__":
  log.debug("starting arping_users")
  main()
