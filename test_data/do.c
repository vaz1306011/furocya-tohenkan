#include <stdio.h>

int main() {
  int num;

  do {
    printf("³‚Ì®”‚ğ“ü—Í‚µ‚Ä‚­‚¾‚³‚¢: ");
    scanf_s("%d", &num);
  } while (num <= 0); // num‚ª0ˆÈ‰º‚Å‚ ‚éŠÔAŒJ‚è•Ô‚·

  printf("“ü—Í‚³‚ê‚½³‚Ì®”: %d\n", num);

  return 0;
}
