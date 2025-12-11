#include <stdio.h>

int main(void) {
  int a;
  a = 4;              // 平行四辺形      [a]に4を代入
  if (a < 1) {        // ひし形          [a]が1より小さいか
    printf("p1");     // 平行四辺形      「p1」を出力
  } else if (a < 2) { // ひし形          [a]が2より小さいか
    printf("p2");     // 平行四辺形      「p2」を出力
    printf("p3");     // 平行四辺形      「p3」を出力
    if (a == 3) {     // ひし形          [a]の値が3と等しいか
      printf("p4");   // 平行四辺形      「p4」を出力
    }
  } else if (a == 4) { // ひし形           [a]の値が4と等しいか
    printf("p5");      // 平行四辺形      「p5」を出力
  } else {
    printf("p6"); // 平行四辺形      「p6」を出力
  }

  return 0;
}