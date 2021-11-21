## 2. JavaScriptの基礎

プログラミングで最も基本的な「演算」（計算）の方法とデータの型（種類）を説明します。

- [2.4 変数](https://ja.javascript.info/variables)
- [2.5 データ型](https://ja.javascript.info/types)
- [2.7 型変換](https://ja.javascript.info/type-conversions)
- [2.8 演算子](https://ja.javascript.info/operators)
- [2.9 比較](https://ja.javascript.info/comparison)
- [2.11 論理演算子](https://ja.javascript.info/logical-operators)
- [5.1 プリミティブのメソッド](https://ja.javascript.info/primitives-methods)
- [5.2 数値](https://ja.javascript.info/number)
- [5.3 文字列](https://ja.javascript.info/string)

### 2.4 変数

変数宣言のキーワードには`let`、`var`、`const`の3種類あります。慣れてくるまでは、よほどのことがない限り`let`で問題ありません（`var`はお勧めしません。[6.4 古い "var"](https://ja.javascript.info/var)参照）。

変数名はなんでもかまいませんが、いわゆる*lowerCamelCase*で記述するのが美しいとされています（[Google JavaScript Style Guideの第6章](https://google.github.io/styleguide/jsguide.html#naming)参照）。

> キーワードなしでも変数宣言はできますが、その変数は「グローバル」の扱いになります（けっこう細かい話です）。また、`"use strict";`ディレクティブ（[2.3 "use strict"](https://ja.javascript.info/strict-mode)）が指定されていると、エラーになることもあります（[template.html](./codes/template.html)から試してみましょう）。


### 演習

1. [2.4 変数ータスク](https://ja.javascript.info/variables#tasks)の3つのタスクを完了しなさい。
