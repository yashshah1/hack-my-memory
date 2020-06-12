// Ignore all these files.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <unistd.h>

int main() {

  char s[] = "ThisIsAGoodStart";
  char *ptr = malloc(sizeof(char) * 17);
  int i = 0;

  printf("The process id is: %d\n", (int) getpid());

  strcpy(ptr, s);

  while(++i) {
    printf("#%d - %s : %z\n", i, ptr, ptr);
    sleep(1);
  }

  return 0;
  
}
