#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <dirent.h>
#include <string.h>
#include <time.h>
 
int main(int argc, char *argv[])
{
    char path[50] = "/sys/bus/w1/devices/";
    char rom[20];
    char buf[100];
    DIR *dirp;
    struct dirent *direntp;
    int fd =-1;
    char *temp;
    float value;
    // These tow lines 
//mount the device:
    system("sudo modprobe w1-gpio");
    system("sudo modprobe w1-therm");
    // Check if /sys/bus/w1/devices/ exists.
    if((dirp = opendir(path)) == NULL)
    {
        printf("opendir error\n");
        return 1;
    }
    // Reads the directories or files in the current directory.
    while((direntp = readdir(dirp)) != NULL)
    {
        // If 28-00000 is the substring of d_name,
        // then copy d_name to rom and print rom.  
        if(strstr(direntp->d_name,"28-00000"))
        {
            strcpy(rom,direntp->d_name);
            //printf(" rom: %s\n",rom);
        }
    }
    closedir(dirp);
    // Append the String rom and "/w1_slave" to path
    // path becomes to "/sys/bus/w1/devices/28-00000xxxx/w1_slave"
    strcat(path,rom);
    strcat(path,"/w1_slave");
        // Open the file in the path.
        if((fd = open(path,O_RDONLY)) < 0)
        {
            printf("open error\n");
            return 1;
        }
        // Read the file
        if(read(fd,buf,sizeof(buf)) < 0)
        {
            printf("read error\n");
            return 1;
        }
        // Returns the first index of 't'.
        temp = strchr(buf,'t');
        // Read the string following "t=".
        sscanf(temp,"t=%s",temp);
        // atof: changes string to float.
        value = atof(temp)/1000;
        printf(" temp : %3.3f °C\n",value);
 
    return 0;
}
