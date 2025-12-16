#include <stdio.h>

int main() {
  int i = 0;       // カウンタ変数を初期化
  while (i < 10) { // i が 10 未満の間、繰り返し
    printf("カウント回数: %d\n", i);
    int n=10;
    n=11;
    i++; // i の値を1増やす
  }
  printf("ループ終了後のカウント回数: %d\n", i);
  printf("終了します。\n");
  printf("完了。\n");
  return 0;
}
