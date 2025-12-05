#include <stdio.h>
int main(void) {
  int a;
  a = 4;
  if (a < 1) {
    printf("p1");
  }else if (a < 2) {
    printf("p2");
    printf("p3");
    if (a == 3) {
      printf("p4");
    }
  } else if (a == 4) {
    printf("p5");
  } else {
    printf("p6");
  }

  return 0;
}