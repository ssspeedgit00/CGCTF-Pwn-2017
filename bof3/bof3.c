#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

void you_cant_see_me(){
    system("sh");
}

int main(){
    char buf[20];
    puts( "Welcome to CGCTF 2017" );
    fflush(stdout);
    read( 0 , buf , 32 );

    if( strlen(buf) > 20 ) {
        puts("You can not pass. HA HA HA!!!");
        exit(0);
    }

    return 0;
}