
#import commands

addr='http://13.82.102.90:8080/ipfs/'

file1 = open('./static/avatar1.png', 'rb')
#os.system("ipfs add './static/avatar1.png")

#output=commands.getstatusoutput('ls')
#print(output)
import subprocess

#subprocess.check_output("dir",stderr=subprocess.STDOUT,shell=True)

from subprocess import Popen, PIPE
#subprocess.call("ipfs get "+ "" + "QmXfcjBHoXvLPvskjCYikGbC5TmUwE8BDr3WRVasRKaJ1x")

p = Popen(['ls', 'la'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate(b"ipfs get QmXfcjBHoXvLPvskjCYikGbC5TmUwE8BDr3WRVasRKaJ1x' stdin")
rc = p.returncode

print(output)
