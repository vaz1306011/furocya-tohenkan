#include <stdio.h>

int main(void) {
  int *p; // ポインタ変数の宣言（int型の変数アドレスを格納）
  int i = 10;

  p = &i;  // 変数iのアドレスをポインタpに代入
  *p = 20; // ポインタpが指す値（i）を20に変更

  printf("i = %d\n", i);   // iの値が表示される
  printf("*p = %d\n", *p); // ポインタpが指す値が表示される
  printf("p = %p\n", p);   // ポインタpが持つアドレス値が表示される

  return 0;
}
