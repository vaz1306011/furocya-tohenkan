#include <stdio.h>

int main() {
  int num;

  do {
    printf("正の整数を入力してください: ");               //平行四辺形    「正の整数を入力してください: 」と表示
    scanf_s("%d", &num);                                //平行四辺形     入力された値を[num]に入れる
  } while (num <= 0); // numが0以下である間、繰り返す     //ひし形         [num]が０以下かどうか   

  printf("入力された正の整数: %d\n", num);                //平行四辺形    「入力された正の整数: 」と[num]を出力する

  return 0;                                             
}
