Title: jupyterでHaskellを使うための第一歩
Date: 2017-07-09 22:50
Tags: programming, Haskell, jupyter
Slug: haskell-jupyter
Author: tok41
Summary: Haskellをjupyterで使う手順の解説をしてみる。

Haskellという言語がすごく良いらしい。

ということで、まずはHaskellの実行環境を構築することにした。
普段は主に、Python+Jupyterでデータ分析系のプログラムを書いて生活しているので、JupyterにHaskellカーネルを導入することにした。

自分のための備忘録と、初めてHaskell触るという人の参考になれば。
超初心者向けなので新しい知見は特に無いです。


# はじめに
Haskellをやってみるにあたって、たぶん最も有名であろう
「[すごいHaskell](https://www.amazon.co.jp/%E3%81%99%E3%81%94%E3%81%84Haskell%E3%81%9F%E3%81%AE%E3%81%97%E3%81%8F%E5%AD%A6%E3%81%BC%E3%81%86-Miran-Lipova%C4%8Da/dp/4274068854)」を読んでいる(以下、「すごいH本」と略記する)。
本書では、Haskellの実行環境としてGHC（The Glasgow Haskell Compiler）をインストールし、インタラクティブなHaskell実行環境であるGHCiを使っている。

しかし、GHCiでは変数の定義にlet句をつけなきゃいけないなどちょっと面倒だったので、jupyterにHaskellカーネルを導入して学習することにした。

本記事では、はじめに私の実行環境を説明する。
そして、GHCをインストールしてGHCiをまずは使ってみる手順を紹介する。
次に、jupyterのHaskellカーネルであるiHaskellのインストール手順を紹介し、jupyter上での実際のHaskellプログラミングについて簡単に解説する。

なお、iHaskellだけを使いたい場合、最初のGHCのインストールはたぶん不要。
また、Dockerを利用するとiHaskellの導入はすごく簡単らしいし日本語の解説も多いので、
Dockerを使ったほうが良いかもしれない（この記事ではDockerについては一切触れない）。


# 1 環境
- OS : Ubuntu 16.04.2 LTS
- CPU : Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz
- RAM : 8GB
- jupyter : 4.3.0 (Anacondaで導入済み)
 	- jupyterの拡張機能はすでにインストール済み


# 2 GHCのインストール
- まずは[公式ページ](https://www.haskell.org/platform/#linux-ubuntu)を参照。
  - 「Haskell ubuntu」あたりをクエリとしてググった
- 上記ページから「Choose your distribution」で「Ubuntu」を選択
- apt-getでインストールできるぜと書いてあるのでそのまま素直に実行
```
$ sudo apt-get install haskell-platform
```

## 2.1 GHCiを触ってみる
- インストールしたんだから触ってみよう
- ghciコマンドを実行するだけ
```
$ ghci
GHCi, version 7.10.3: http://www.haskell.org/ghc/  :? for help
Prelude> 
```
- インタラクティブなHaskell実行環境が立ち上がった
	- プロンプトが出ているので、ここにコードを書いていけば良い
	- 実際にはすごいH本にある例をいくつか書いてみたが、ここでは割愛
- 終了するには":q" or ":quit"を入力
```
Prelude> :q
Leaving GHCi.
```
- とりあえず動いた

## 2.2 GHCのバージョン
- apt-getでインストールすると、7.10.3がインストールされる
```
$ ghc --version
The Glorious Glasgow Haskell Compilation System, version 7.10.3
```
- しかし、本記事作成時点(2017/07/09)ではすでに8系がリリースされている
    - これがすぐ後で問題になる


# 3 iHaskellのインストール
- jupyterにHaskellカーネルを導入するために、IHaskellをインストールする。
- [公式ページ](https://github.com/gibiansky/IHaskell)を確認
  - UbuntuへのインストールなのでLinuxの項目を確認すると、(1)apt-getでpythonなどのライブラリをいくつか導入し、(2)jupyter関連のパッケージをインストール、(3)stackをインストール、(4)IHaskellのインストール。という手順らしい。

## 3.1 諸々のライブラリのインストール
- 上記のページの指示にそのまま従い、以下のコマンドを実行
```
$ sudo apt-get install -y python3-pip git libtinfo-dev libzmq3-dev libcairo2-dev libpango1.0-dev libmagic-dev libblas-dev liblapack-dev
```

## 3.2 jupyter関連のパッケージをインストール
- 次の指示では、requirements.txtの中身を入れろとある
- requirementsを確認すると、jupyterと関連のパッケージを入れることになっているが、全て既存環境にインストール済みなのでここでは無視

## 3.3 stackのインストール
- stackというのは、Haskellパッケージの管理をするためのツールらしい
  - ビルドとかインストールとか、別バージョンのHaskellの管理などもできるらしいが、詳しいことはまだよくわかっていないので、調べたら別に記事を書こう。
```
$ curl -sSL https://get.haskellstack.org/ | sh
```

## 3.4 IHaskellのインストール
- IHaskellのgitリポジトリをclone
```
$ git clone https://github.com/gibiansky/IHaskell
$ cd IHaskell
```
- stackでアプリのインストール
```
$ stack install gtk2hs-buildtools

No compiler found, expected minor version match with ghc-8.0.2 (x86_64) (based on resolver setting in /home/yoichi/work/training/haskell/IHaskell/stack.yaml).
To install the correct GHC into /home/yoichi/.stack/programs/x86_64-linux/, try running "stack setup" or use the "--install-ghc" flag.
```
- GHCのバージョンが合ってないと怒られた
  - stackを使ってビルドしたりインストールするには、stack.yamlにコンパイラ（GHC）のバージョンを書いたり、関連パッケージを書いたりするらしいのだが、「resolver: lts-8.22」と書かれている
  - 先のGHCのインストールではapt-getでインストールすると7系が入ったので、当然8系は入っていない
- でもstackなら問題なし
  - stack.yamlの設定で不足があれば、`stack setup`コマンドで自動で環境を構築できる
```
$ stack setup

Preparing to install GHC to an isolated location.
This will not interfere with any system-level installation.
Downloaded ghc-8.0.2.                                      
Installed GHC.
stack will use a sandboxed GHC it installed
For more information on paths, see 'stack path' and 'stack exec env'
To use this GHC and packages outside of a project, consider using:
stack ghc, stack ghci, stack runghc, or stack exec
```
- 再度install作業開始
```
$ stack install gtk2hs-buildtools
$ stack install --fast
  # 結構時間かかる
$ stack exec ihaskell -- install --stack
```
できた！


# 4 jupyter+Haskell
## 4.1 Haskellカーネルのjupyter notebookを作成
- stackを使ってjupyterを立ち上げる
```
$ stack exec jupyter -- notebook
```
- いつものjupyterが立ち上がるので、新規ノートブック作成時にカーネルをpythonではなくHaskellを選択

![jupyter-haskell-kernel](/images/jupyter-haskell-kernel.png)


## 4.2 使ってみる
- GHCiに記入するのと同じ要領でセルに関数を記入
  - セル毎にコンパイルしてメモリ空間に展開するようなので、すごいH本にあるように、let式で名前を定義したりしないで良いみたい（？）

![jupyter-first-sample](/images/jupyter-haskell-notebook-firstsample.png)


# 終わりに
ここまでで、jupyter上でHaskellコードを書く環境の構築をやってみた。
とはいっても、ほぼ公式の指示に従っただけなので、新しい知見は特に無い。

IHaskell、ざっと使ってみたところ、
エディタを立ち上げて別ファイルに関数を書いてそれをロードしてといった手間が無いので、
ちょっとだけ効率的かなと感じている。
あとは、すごいH本を読みながら使ってみて何かアップデートがあれば追記していく。

## 今後の課題
- stackについて調べて何をやっているのか解説を追記
- IHaskellの利用例が貧弱なのでもう少し何か書いた例を追記


# 参考
- [Haskellプラットフォーム](https://www.haskell.org/platform/#linux-ubuntu)
- [IHaskell(GitHub)](https://github.com/gibiansky/IHaskell)
