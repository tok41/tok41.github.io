Title: GitHubPagesとPelicanで始めるブログ(WIP)
Date: 2017-07-17 22:50
Tags: python, pelican
Slug: how-to-start-pelicanblog
Author: tok41
Summary: Pelican（Pythonベースの静的webサイトジェネレータ）GitHubPages上でブログを始める方法の解説。


ということで、ブログをやろうと思う。
（これまでに何度も挫折しているので、今度こそ長続きすると良いな）

ここでは、ブログ初心者が無料でブログを開設するためにやったことをまとめます。
自分のための備忘録と、同じように悩んでる人の参考になれば。


# はじめに
ブログ初心者なので、ブログというのをどうやって始めたら良いのかわかっていない。
ずい分昔（10年以上前）には、HTMLを直接書いてwebサーバに上げるようなことはやっていたものの、ここ最近のツールには全くもって疎いのです。

どうやって運用するかちょっと調べたところ、
GithubにGithubPagesという静的なwebサイトをホスティングしてくれるサービスがあるということを知った。
無料で(ここ重要)。
静的なwebページを良い感じに作成するツールがいくつかあるということも知った。
無料で(ここ重要)。
静的サイトジェネレータとしては、いろいろあるみたいだが、
PythonとMarkdownで書けるということで、
[Pelican](http://docs.getpelican.com/en/stable/)というジェネレータを使うことにした。

そこで、GithubPages+Pelicanでブログを構築してみたので、
手順を紹介します。


# 1 手順の概要
GithubPages+Pelicanでブログを開設するための手順の概要

- GithubPages用のリポジトリ作成
	- Githubに公開用のリポジトリを作成する
	- すでにGithubにアカウントがあることが前提
- Pelicanのインストール
	- インストールと初期設定をする
- 記事の作成と公開
	- markdownで記事を作成し、htmlを作成してGithubPagesで公開するまでの手順
- （おまけ）ソース管理
	- markdownで書いたソースを管理するための手順
	- 外出用のマシンと家でコードを書いて実験するためのマシンとそれぞれ使いたいので、ソースをgithubで管理する

# 2 GithubPages用のリポジトリ作成
まず、公開用のリポジトリを作成する。
このリポジトリのmasterブランチにhtmlを置いておくことで、Webサイトを公開することができる。

- Githubの自分のアカウントで、`{username}.github.io`というリポジトリを作成
	- 私の場合は`tok41.github.io`
- このリポジトリを作ることで、グローバルに以下のURLでアクセスできる
	- `http://{username}.github.io`


# 3 Pelicanのインストール
## 3.1 Pelican用の仮想環境を用意
Pelicanはブログにしか使わないので、
他のPython環境と分けるために、virtualenvで環境を分離する。
気にしない人はこの手順を飛ばしても良い。

なお、pyenv, virtualenvが導入されていることを前提にします。
（無い場合には飛ばしても良いし、ググれば手順が公開されてます）

- python2.7をpyenvで別に用意する
```
$ pyenv install -l  # <- pyenvでインストールできるPythonを探す
$ pyenv install 2.7.11 # <- 導入時点で2.7.11が最新だった
```

- ~/{適当なディレクトリ}/Pelican-Blog を作成
    - ブログのソースを置いたりするためのディレクトリ
- pyenvで仮想環境を作成
```
cd ~/{適当なディレクトリ}/Pelican-Blog
$ pyenv virtualenv 2.7.11 PelicanBlog
  		# PelicanBlogという名前の環境を作る
$ pyenv local PelicanBlog
  		# Pelican-Blogに来たらPelicanBlog環境になるように設定
```

## 3.2 Pelicanのインストール
- pipでインストール
```
$ pip install pelican
$ pip install Markdown
  	  # Markdownで記事を書くために
$ pip install ghp-import
  	  # Github Pagesへの公開操作をやってくれるパッケージ
	  # 公開操作→masterブランチに各種htmlファイルなどをpush
```

## 3.3 pelican-quickstartで雛形の作成
- 対話形式でwebぺーじの初期設定をするためのツール
```
$ pelican-quickstart
```
- 基本はdefaultで答えていけばよいかと
- この設定が済めば以下のようなファイルが自動で生成されているはず
```
Pelican-Blog
  |- content/ <- このディレクトリ以下に記事を書いていく
  |- output/  <- 生成されたhtmlなどが配置される
  |- develop_server.sh
  |- fabfile.py
  |- Makefile
  |- pelicanconf.py  <-各種設定を書く
  |- publishconf.py
```


# 4 記事の作成と公開
## 4.1 記事の作成
記事はcontentディレクトリ以下に書く。
このとき、content以下にディレクトリを作成すると、
そのディレクトリがブログカテゴリと自動で認識される。
記事のソース中でカテゴリを指定することもできるが、
ディレクトリ分けたほうが管理の上でも良いでしょう。

また、pagesというディレクトリは、特殊なカテゴリで、
aboutmeなどのページを作成する目的で使われるらしい。
```
content/
  |- pages/
       |- Aboutme.mdなど
  |- Category1/
  |- Category2/
  |- ...
```

## 4.2 実際に記事を書く
contentディレクトリ以下に記事を書く。
先の手順でMarkdownパッケージをインストールしているため、
拡張子`.md`で作成する。
```
$ emacs first-post.md
```

サンプルのソース。
```
Title: 初めまして
Date: 2017-06-25 18:13
Modified: 2017-06-25 18:13
Category: Pelican
Tags: pelican, python
Slug: firstr-post
Authors: tok41
Summary: ブログ始めました

# 最初の投稿

ブログ作ってみたテスト。
Pelicanを使ってコンテンツを生成する。

- Markdownで書ける
- テスト
\```python            (実際はバックスラッシュはいらない)
print 'Hello World!'
\```                  (実際はバックスラッシュはいらない)

以上。
```

- ブログソースの先頭には、記事の情報を記載する
	- key:value という形式
	- keyの最新情報を確認するために、[公式ページ](http://docs.getpelican.com/en/stable/content.html)を参考にする

## 4.3 記事のコンパイル
- 記事を作成したらコンパイルする
	- pelican-quickstartでMakefileができているはずなので、以下のコマンドを使う
```
$ make html
```

- ローカルに記事のチェックをするためにwebサーバを立てる
```
$ make serve
```
- localhostの8000ポートにアクセスして記事をチェックする
	- http://localhost:8000

## 4.4 記事の公開
- チェックが済んだらいよいよ記事を公開する
```
$ make publish  # <-公開用にｈｔｍｌを作成
$ git init
$ ghp-import output  # <-ghp-importで公開用のディレクトリ指定
$ git push https://github.com/tok41/tok41.github.io.git gh-pages:master  # <- githubにpushする
```

- 実際にブラウザで確認すると、グローバルに公開されていることが確認できる
	- `http://{username}.github.io`
	- このブログでは[http://tok41.github.io](http://tok41.github.io)

## 4.5 日々の公開手順
日々の公開手順をまとめると以下のようになる。

- 記事をcontent以下に作成し、内容を確認する
```
$ emacs {article_name}.md
$ make html
$ make serve
```

- 公開用にコンパイル
```
$ make publish
```

- gh-pagesで公開操作
```
$ ghp-import output
$ git push https://github.com/{username}/{username}.github.io.git gh-pages:master
```


# 5 （おまけ）ソース管理
gh-pagesでは、生成したhtmlをgithubにpushするので、ソース自体はローカルに保存されたままである。
しかし、ブログのソースもgithubで管理して、複数のマシンで記事を作成したいと思っている。
なぜなら、外出用のマシンと、コードを書いて実験するためのマシンが別で、実験用マシンでも記事を書きたいので。

## 5.1 構成
- 構成としては、リポジトリを共通として、ブランチを分けることで対処することにした。
```
tok41.github.io
  |- master   <- 公開用のブランチ
  |- source   <- ソース管理用のブランチ
```



# おわりに
以上、簡単にGithubPages+Pelicanでブログを作成する手順を紹介しました。

まだまだわからないことが多いので、少しずつアップデートしていこうと思います。

## Future-Work
- ソース管理の詳細を追記
- テーマの適用について追記する
- 画像の貼り付けについて追記する
- コメント欄の設定について追記する

# 参考サイト
参考にさせていただいたサイト

- [Pelican](http://docs.getpelican.com/en/stable/)
- [Pelican + Markdown + GitHub Pagesで管理するブログの作り方](http://blog.sotm.jp/2014/01/04/Pelican-Markdown-GithubPages-install-guide/)
- [PELICAN + GITHUB PAGES でブログを作った話](http://daikishimada.github.io/pelican-start.html)
- [Pythonの静的サイトジェネレータ"Pelican"でお手軽にブログをはじめる手順](http://qiita.com/ogrew/items/ecef0a4700d5bd4d875d)
