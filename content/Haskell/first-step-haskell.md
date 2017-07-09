Title: jupyterでHaskellを使うための第一歩(WIP)
Date: 2017-07-09 22:50
Tags: programming, Haskell, jupyter
Slug: haskell-jupyter
Author: tok41
Summary: Haskellをjupyterで使う手順の解説をしてみる。

Haskellという言語がすごく良いらしい。

ということで、まずはHaskellの実行環境を構築することにした。
普段は主に、Python+Jupyterでデータ分析系のプログラムを書いて生活しているので、JupyterにHaskellカーネルを導入することにした。

自分のための備忘録と、初めてHaskell触るという人の参考になれば。
超初心者向け。


# はじめに
Haskellをやってみるにあたって、たぶん最も有名であろう
「[すごいHaskell](https://www.amazon.co.jp/%E3%81%99%E3%81%94%E3%81%84Haskell%E3%81%9F%E3%81%AE%E3%81%97%E3%81%8F%E5%AD%A6%E3%81%BC%E3%81%86-Miran-Lipova%C4%8Da/dp/4274068854)」を読んでいる。
本書では、Haskellの実行環境としてGHC（The Glasgow Haskell Compiler）をインストールし、インタラクティブなHaskell実行環境であるGHCiを使っている。

しかし、GHCiでは変数の定義にlet句をつけなきゃいけないなどちょっと面倒だったので、jupyterにHaskellカーネルを導入して学習することにした。

本記事では、はじめに著者の実行環境を説明する。
そして、GHCをインストールしてGHCiをまずは使ってみる手順を紹介する。
次に、jupyterのHaskellカーネルであるiHaskellのインストール手順を紹介し、jupyter上での実際のHaskellプログラミングについて簡単に解説する。

なお、iHaskellだけを使いたい場合、最初のGHCのインストールはたぶん不要。


# 環境
- OS : Ubuntu 16.04.2 LTS
- CPU : Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz
- RAM : 8GB
- jupyter :
  - jupyterはAnacondaでPython環境作ってる時にインストール済み
  - jupyterの拡張機能はすでにインストール済み（後述）

# GHCのインストール
- まずは[公式ページ](https://www.haskell.org/platform/#linux-ubuntu)を見る
  - 「Haskell ubuntu」あたりをクエリとしてググった
- 上記ページから「Choose your distribution」で「Ubuntu」を選択
- apt-getでインストールできるぜと書いてあるのでそのまま素直に実行
```
$ sudo apt-get install haskell-platform
```

## GHCiを触ってみる
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

## GHCのバージョン
- apt-getでインストールすると、7.10.3がインストールされる
```
$ ghc --version
The Glorious Glasgow Haskell Compilation System, version 7.10.3
```
- しかし、本記事作成時点(2017/07/09)ではすでに8系がリリースされている
  - これがすぐ後で問題になる

# iHaskellのインストール
- jupyterにHaskellカーネルを導入するには、IHaskellを使う


# jupyter+Haskell
# 終わりに
# 参考
- [Haskellプラットフォーム](https://www.haskell.org/platform/#linux-ubuntu)
- [IHaskell(GitHub)](https://github.com/gibiansky/IHaskell)
