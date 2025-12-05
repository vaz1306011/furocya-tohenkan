#include <stdio.h>

int main() {
  int i; // カウンタ変数の宣言

  for (i = 1; i <= 10; ++i) {
    printf("%d ", i); // iの値を表示
  }
  printf("\\n"); // 改行

  return 0;
}
// 出力結果: 1 2 3 4 5 6 7 8 9 10
