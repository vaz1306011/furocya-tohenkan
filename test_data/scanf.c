#include <stdio.h>

int main(void) {
  int n;
  printf("整数を入力してください: ");
  scanf_s("%d", &n); // 整数を読み込み、変数nに格納する
  printf("入力された整数は %d です。\n", n);
  return 0;
}
