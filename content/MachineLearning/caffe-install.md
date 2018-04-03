Title: Caffe環境の導入
Date: 2017-10-29 18:00
Tags: programming, caffe, DeepLearning
Slug: caffe-install
Author: tok41
Summary: 深層学習ライブラリcaffeをインストールする。


深層学習をする場合、私は普段chainerを使って書いているわけですが、
仕事でcaffeが必要になったので環境構築しました。

なんだかんだ調べてやってたらえらい時間がかかりました。
chainerやtensorflowなら一瞬なのに。。。

既にweb上には日本語でも英語でも同様の記事が大量に溢れていますが、
備忘録を兼ねてまとめておきます。

誰かの参考になれば。


# 環境
- OS : Ubuntu 16.04.2 LTS
- CPU : Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz
- GPU : GeForce GTX 1070
- RAM : 8GB
- Python : Python 2.7.13 :: Anaconda custom (64-bit)
- CUDA-8.0
- OpenCV : 3.1


# インストール
## 手順概要
環境構築については、[公式git](https://github.com/BVLC/caffe/wiki/Ubuntu-16.04-or-15.10-Installation-Guide)を参考にすればよいです。
ここに記載の通りに進めていけば問題ないかと。

以下の手順で進めていきます。
- OpenCVのインストール（本稿では記載しない）
- CUDA関連のインストール（本稿では記載しない）
- aptで必須パッケージをインストール
- caffeのリポジトリのclone
- caffeのビルド


## aptで必須パッケージをインストール
[公式git](https://github.com/BVLC/caffe/wiki/Ubuntu-16.04-or-15.10-Installation-Guide)に記載の通り、
はじめにaptで必須パッケージを導入します。
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install -y build-essential cmake git pkg-config
sudo apt-get install -y libprotobuf-dev libleveldb-dev libsnappy-dev libhdf5-serial-dev protobuf-compiler
sudo apt-get install -y libatlas-base-dev 
sudo apt-get install -y --no-install-recommends libboost-all-dev
sudo apt-get install -y libgflags-dev libgoogle-glog-dev liblmdb-dev
```

## caffeのリポジトリのclone
gitでcaffeを入手します。
gitが使えないならzipファイルでダウンロードしてきても良いはずですが、未確認です。
```
$ git clone https://github.com/BVLC/caffe.git
```

## caffeのビルド
いよいよcaffeをビルドします。
Makeconfigを環境に合わせて書き換え、makeを実行します。

CMakeでmakefileを作る方法もありますが、私は試していません。

### Makefile.config作成
caffeのリポジトリの中に、Makefile.config.exampleがあるので、これを自分の環境に合わせて書き換えます。

私の環境では以下のように変更しました。


```
$ diff Makefile.config Makefile.config.example 

5c5
< USE_CUDNN := 1
---
> # USE_CUDNN := 1

21c21
< OPENCV_VERSION := 3
---
> # OPENCV_VERSION := 3

28c28
< CUDA_DIR := /usr/local/cuda-8.0
---
> CUDA_DIR := /usr/local/cuda

68,69c68,69
< #PYTHON_INCLUDE := /usr/include/python2.7 \
< #		/usr/lib/python2.7/dist-packages/numpy/core/include
---
> PYTHON_INCLUDE := /usr/include/python2.7 \
> 		/usr/lib/python2.7/dist-packages/numpy/core/include

72,75c72,75
< ANACONDA_HOME := $(HOME)/.pyenv/versions/anaconda2-4.3.0
< PYTHON_INCLUDE := $(ANACONDA_HOME)/include \
< 	       $(ANACONDA_HOME)/include/python2.7 \
< 	       $(ANACONDA_HOME)/lib/python2.7/site-packages/numpy/core/include
---
> # ANACONDA_HOME := $(HOME)/anaconda
> # PYTHON_INCLUDE := $(ANACONDA_HOME)/include \
> 		# $(ANACONDA_HOME)/include/python2.7 \
> 		# $(ANACONDA_HOME)/lib/python2.7/site-packages/numpy/core/include

83,84c83,84
< # PYTHON_LIB := /usr/lib
< PYTHON_LIB := $(ANACONDA_HOME)/lib
---
> PYTHON_LIB := /usr/lib
> # PYTHON_LIB := $(ANACONDA_HOME)/lib

91c91
< WITH_PYTHON_LAYER := 1
---
> # WITH_PYTHON_LAYER := 1
```

### pythonのパッケージをインストール

公式に案内の通り、以下のパッケージを導入。

```
$ cd python
$ for req in $(cat requirements.txt); do pip install $req; done
```


### ライブラリのリンク貼るなど

公式の通り、以下のコマンドでhdf5関連のライブラリのリンクを張る。

```
$ cd /usr/lib/x86_64-linux-gnu
$ sudo ln -s libhdf5_serial.so.10.1.0 libhdf5.so
$ sudo ln -s libhdf5_serial_hl.so.10.0.2 libhdf5_hl.so
```

次いで、Ubuntu16を使っているので、以下のコマンド実行。
```
$ find . -type f -exec sed -i -e 's^"hdf5.h"^"hdf5/serial/hdf5.h"^g' -e 's^"hdf5_hl.h"^"hdf5/serial/hdf5_hl.h"^g' '{}' \;
```


### Makefileの修正
公式の通り、以下の部分を変更する。

```
$ git diff Makefile
diff --git a/Makefile b/Makefile
index 4d32416..cf37bd0 100644
--- a/Makefile
+++ b/Makefile
@@ -193,6 +193,9 @@ ifeq ($(USE_LMDB), 1)
 endif
 ifeq ($(USE_OPENCV), 1)
        LIBRARIES += opencv_core opencv_highgui opencv_imgproc
+       LIBRARIES += glog gflags protobuf leveldb snappy \
+               lmdb boost_system boost_filesystem hdf5_hl hdf5 m \
+               opencv_core opencv_highgui opencv_imgproc opencv_imgcodecs opencv_videoio
 
        ifeq ($(OPENCV_VERSION), 3)
                LIBRARIES += opencv_imgcodecs
@@ -412,7 +415,8 @@ CXXFLAGS += -MMD -MP
 # Complete build flags.
 COMMON_FLAGS += $(foreach includedir,$(INCLUDE_DIRS),-I$(includedir))
 CXXFLAGS += -pthread -fPIC $(COMMON_FLAGS) $(WARNINGS)
-NVCCFLAGS += -ccbin=$(CXX) -Xcompiler -fPIC $(COMMON_FLAGS)
+#NVCCFLAGS += -ccbin=$(CXX) -Xcompiler -fPIC $(COMMON_FLAGS)
+NVCCFLAGS += -D_FORCE_INLINES -ccbin=$(CXX) -Xcompiler -fPIC $(COMMON_FLAGS)
 # mex may invoke an older gcc that is too liberal with -Wuninitalized
 MATLAB_CXXFLAGS := $(CXXFLAGS) -Wno-uninitialized
 LINKFLAGS += -pthread -fPIC $(COMMON_FLAGS) $(WARNINGS)
```


### いよいよビルド

ここまででビルドの準備ができたので、ビルドします。

```
$ make all -j $(($(nproc) + 1))
```

以下のエラーに遭遇。
```
fatal error: pyconfig.h: No such file or directory
```

python関連のヘッダファイルのパスを通しておく必要があるようです。
（[参照](https://github.com/BVLC/caffe/issues/410)）

```
$ export CPLUS_INCLUDE_PATH=/usr/include/python2.7
$ make all -j $(($(nproc) + 1))
```

これでmakeが通ったので、以下の通りビルドする。

```
$ make test -j $(($(nproc) + 1))
$ make pycaffe -j $(($(nproc) + 1))
$ make distribute -j $(($(nproc) + 1))
```


### pycaffeのインポートでエラー
pythonでimportする際に以下のエラーに遭遇。

```
ImportError: ${HOME}/.pyenv/versions/anaconda2-4.3.0/envs/test/bin/../lib/libstdc++.so.6: version `GLIBCXX_3.4.21' not found (required by ${HOME}/etc/caffe/python/caffe/_caffe.so)
```

condaでlibgccをインストールすれば良いらしい([参照](https://github.com/BVLC/caffe/issues/4953))。

```
$ conda install libgcc
```


# テスト
caffeのexampleがあるので、そちらを実行すると良いです。

example/00-classification.ipynbで画像分類を試行できます（jupyter notebookを立てることが必要）。

