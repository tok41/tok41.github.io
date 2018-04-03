Title: Caffeを使ったC++コードのビルド
Date: 2017-10-31 01:00
Tags: programming, caffe, DeepLearning
Slug: caffe-first-build
Author: tok41
Summary: 深層学習ライブラリcaffeを使ったC++コードをビルドする手順（初心者向け）

[以前の記事](https://tok41.github.io/caffe-install.html)では、
githubからcaffeリポジトリをcloneしてビルドし、
サンプルコードを走らせてみるところをやりました。
モデルファイルやソルバーの設定ファイルを書き換えれば、
基本のcaffeのコードでいろいろ深層学習を試すことができます。

しかし、自分で書いたアプリケーションで深層学習するためには
caffeをライブラリとして読み込んで利用することになります。
（条件が合えばcaffeの実行ファイルを呼ぶということもできると思うが）

そこで本記事では、caffeをライブラリとしてimportし、
学習と推論を実行するコードを書いてみます。
コードは[github](https://github.com/tok41/simple_caffe_samples/tree/master)に
上げてあります。

初めてcaffeを触る人向け。
誰かの参考になれば。

# 環境
- OS : Ubuntu 16.04.2 LTS
- CPU : Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz
- GPU : GeForce GTX 1070
- RAM : 8GB
- Python : Python 2.7.13 :: Anaconda custom (64-bit)
- CUDA-8.0
- OpenCV : 3.1


# 参考にさせて頂いたページ
- http://d.hatena.ne.jp/muupan/20141010/1412895321
  - 参考というレベルではなく、参考にさせていただきました
- [caffe公式](http://caffe.berkeleyvision.org/)
  - Makefileやtools/caffe.cppが参考になります


# 対象にする問題
ここでは、最もシンプルな線形回帰問題を対象にしてcaffeを使ったコードを
ビルドする方法を練習します。

## 1次元線形回帰モデル
以下の図に示すモデルを対象とします。

![simplest_regression_model](/images/simplest_regression_model.png)

入力が1次元(x)で出力も1次元、いわゆる`y=ax+b`のモデルで、
未知パラメータである`a`（重み）と`b`（バイアス）の2つのパラメータを
学習したいというものです。

学習としてはできて当たり前、というか最小二乗法などで解いたほうが速いですが、
あくまで練習と割りきってやってみます。

## データ
データは、`a`と`b`を適当に決めたモデル式に従って、
小さいガウスノイズを載せた形で生成しました（下図）。
データを生成するためのコードも[github](https://github.com/tok41/simple_caffe_samples/blob/master/ipynb/generate-sample-data.ipynb)にアップしています。
ipynbなので、jupyterで実行してください。

![simplest_sample_data](/images/sample_data_linear_regression_simplest.png)


また、ラベルが離散的に与えられるようなデータも作ってみました(下図)。
が、結局一次線形なモデルなので、学習できて当たり前です。

![descrete_sample_data](/images/sample_data_linear_regression_descrete.png)


# Caffeを使ったコード
私の[github](https://github.com/tok41/simple_caffe_samples/tree/master)を
参照してください。

- caffe-1d-regression.cpp : メイン
- net.prototxt : networkの定義
- solver.prototxt : solver定義

というか、
上記の[こちらのページ](http://d.hatena.ne.jp/muupan/20141010/1412895321)のコードを
ほぼ使わせていただいています。

## Solver
solver定義(solver.prototxt)は完全にコピーです。

## Network
net.prototxtですが、
まず1変数の線形回帰をするので、入力層を以下のように定義しています。
```
layers {
    name : "input"
	type: MEMORY_DATA
	top: "input"
	top: "dummy_label1"
	memory_data_param {
	    batch_size: 10
		channels: 1
		height: 1
		width: 1
	}
}								
```

外部ファイルのでーたをメモリに展開して入力するつもりなので、
LayerのtypeはMEMORY_DATAです。
回帰をするので、ラベルデータは存在しません。
なので、dummy_label1として、適当な値を入力することにします。

FullConnect層で、出力を1つ、重みとバイアスを定義しています。
```
layers {
    name: "ip"
	type: INNER_PRODUCT
	bottom: "input"
	top: "ip"
	inner_product_param {
	    num_output: 1
		weight_filler {
		    type: "constant"
			value: 0
		}
		bias_filler {
		    type: "constant"
			value: 0
		}
	}
}
```

lossを計算するために、targetを定義する層を定義します。
```
layers {
    name: "target"
	type: MEMORY_DATA
	top: "target"
	top: "dummy_label2"
	memory_data_param {
	    batch_size: 10
		channels: 1
		height: 1
		width: 1
	}
}
```

回帰問題なので、targetには`y=ax+b`の`y`を入力します。
これもラベルデータは存在せず、適当なデータを入力します。


## Main(caffe-1d-regression.cpp)
コードは[ちら](https://github.com/tok41/simple_caffe_samples/blob/master/caffe-1d-regression.cpp)を参照してください。

### データのメモリへの展開
main関数内の29行から60行まででCSVデータを取り込んでいます
（main関数の半分以上の行数!）。
なお、CSVファイルを取り込むために、split関数を定義しています。
```
void split(const std::string &s, char delim, std::function< void(int, std::string& )> f) {
  std::string token;
  std::istringstream stream(s);
  int i=0;
  while(getline(stream, token, ',')){
    f(i, token);
	i++;
  }
}
```
この関数は、csv文字列(s)と分割文字(delim)、
切り出した文字列に適用する関数を受け取ります。
以下のようにして使います。
```
split(line, ',', [&](int i, std::string & token) {
        dataMap[i].push_back(std::stof(token));
    }
);
```

### Solver
prototxtを取り込んでSolverを作成します。
```
caffe::SolverParameter solver_param;
caffe::ReadSolverParamsFromTextFileOrDie("solver.prototxt", &solver_param);
std::shared_ptr<caffe::Solver<float>> solver(caffe::SolverRegistry<float>::CreateSolver(solver_param));
const auto net = solver->net();
```

### データの入力
取り込んだデータを入力層にinputする設定を書きます。
```
const auto input_layer =
    boost::dynamic_pointer_cast<caffe::MemoryDataLayer<float>>(net->layer_by_name("input"));
assert(input_layer);
input_layer->Reset(dataMap[0].data(), dummy_data.data(), dataMap[0].size());
```

目標データも同様に設定します。
```
const auto target_layer =
    boost::dynamic_pointer_cast<caffe::MemoryDataLayer<float>>(net->layer_by_name("target"));
assert(target_layer);
target_layer->Reset(dataMap[1].data(), dummy_data.data(), dataMap[1].size());
```

### 学習
solverに従って学習を実施します。
```
solver->Solve();
```

### テスト
学習済みのモデルを利用して、テストデータから出力を予測します。

テストデータはsample_inputという変数にします。
一様分布に従う乱数を入力しています。

```
std::vector<float> sample_input;
for(int i=0 ; i<batch_size ; i++) { // バッチ分のデータを入力
    sample_input.push_back(dist(mt));
}
```

そして、評価データを入力層にinputします
```
input_layer->Reset(sample_input.data(), dummy_data.data(), sample_input.size());
```

Forwardメソッドで入力したデータでforward計算を実施します。
```
const auto result = net->Forward();
```


# ビルド
上記のコードをビルドするために、以下のビルドコマンドを実行します。
```
$ g++ -std=c++11 -I${HOME}/caffe/include -L${HOME}/caffe/build/lib caffe-sample.cpp -lcaffe -lglog -lboost_system -lhdf5 -lhdf5_hl
```

caffeのインストールディレクトリが`${HOME}/caffe`の場合です。


## トラブルシュート

### caffe/proto/caffe.pb.h が存在しないと怒られる
[こちら](https://github.com/muupan/dqn-in-the-caffe/issues/3)を参考にcaffe.pb.hを作る。
```
$ cd ~/caffe
$ protoc src/caffe/proto/caffe.proto --cpp_out=.
$ mkdir include/caffe/proto
$ mv src/caffe/proto/caffe.pb.h include/caffe/proto
```

### cublas_v2.hが見つからない
[こちら](https://github.com/mhauskn/dqn-hfo)を参考にすると、
includeディレクトリのパスを通しておけと。
```
$ export CPLUS_INCLUDE_PATH=/usr/local/cuda/include:$CPLUS_INCLUDE_PATH
```

### libcaffe.so.1.0.0が見つからない
LD_LIBRARY_PATHにパスを追加。
```
$ export LD_LIBRARY_PATH=/home/yoichi/work/caffe/distribute/lib/:$LD_LIBRARY_PATH
```

### 実行時にライブラリが読めない
```
$ ./a.out

./a.out: error while loading shared libraries: libhdf5_hl.so.100: cannot open shared object file: No such file or directory
```

詳しい人教えてください。

とりあえずリンクをa.outと同じディレクトリに張ったら通りました。

```
$ ln -s ~/.pyenv/versions/anaconda2-4.4.0/lib/libhdf5_hl.so.100
$ ln -s ~/.pyenv/versions/anaconda2-4.4.0/lib/libhdf5_hl.so
$ ln -s ~/.pyenv/versions/anaconda2-4.4.0/lib/libhdf5.so.101
```



# おわりに
ここまでで、caffeをライブラリC++コードで呼び出して使うための基礎を試行しました。
ビルドコマンドで四苦八苦したり、ライブラリがリンクできなかったりと
いろいろありましたがなんとかビルドできるところまで行きました。

今後、ネットワークを作って遊んでいこうと思います。
（Chainerは簡単だな〜と実感）


# おまけ
githubのコードを走らせると予測結果がcsvファイルで吐かれます
(data/sampledata_discrete_target.csv)。
また、学習済みのモデルファイルが出力されているはずです(_iter_4000.caffemodel)。

これらを読み込んで結果を確認してみます。

ipynbで[確認用のスクリプト](https://github.com/tok41/simple_caffe_samples/blob/master/ipynb/visualize_regression_result.ipynb)を
作成したのでご参照ください。

![regression_result](/images/regression_result_linear_regression_descrete.png)

狙い通りに飛び飛びの離散的な目的変数でも、
間を補完する予測ができたの図。
