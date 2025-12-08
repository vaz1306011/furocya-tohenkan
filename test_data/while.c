#include <stdio.h>

int main() {
  int i = 0;       // カウンタ変数を初期化
  while (i < 10) { // i が 10 未満の間、繰り返し
    printf("カウント回数: %d\n", i);
    i++; // i の値を1増やす
  }
  return 0;
}
