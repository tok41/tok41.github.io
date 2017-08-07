Title: PythonでWebカメラを使ってみる
Date: 2017-08-06 22:00
Tags: programming, python
Slug: python-WebCamera
Author: tok41
Summary: PythonでWebカメラをつかってみる

Python＋OpenCVですごく簡単にWebカメラを扱うことができる。

カメラ映像を取り込んで、画像処理をテストしていくために、
Webカメラ操作の超基本をまとめておく。


# はじめに
画像処理で遊ぶために、Webカメラの画像をキャプチャして簡単なフィルタを実装してみる。

はじめに、OpenCVでカメラ画像をキャプチャするための基本を述べ、
次いで今回実装したフィルタを説明する。

OpenCVはインストール済みであることを前提にするが、
インストールしてあると、この記事に書いてあるようにトラブるかもしれない。

今回実装したコードは
[ここ](https://github.com/tok41/ObjectTracker/tree/master/videoCapture)
に上がっているので、
誰かの参考になれば幸いです。


# 環境
- OS : Ubuntu 16.04.2 LTS
- CPU : Intel(R) Core(TM) i7-3770 CPU @ 3.40GHz
- RAM : 8GB
- Python : Python 2.7.13 :: Anaconda custom (64-bit)
- webカメラ : Microsoft LifeCam Studio for Business

## Webカメラ
WebカメラはUVC(USB Video Class)タイプのWebカメラなら何でも良い。
私はMicrosoft LifeCam StudioというのをAmazonで入手。
HD映像が撮れるというので購入。

ちなみに、UVCタイプというのは良くわからなかったので、
[ここ](http://www.ideasonboard.org/uvc/)で対応の
製品を探した。
初めて購入するなら、上記のサイトで探してWebカメラを手に入れるのが良いんじゃないかな。

## OpenCV
画像処理用のライブラリが超充実しているライブラリである「OpenCV」を使う。
予め、以下のコマンドでcondaでインストールしていた。

```
$ conda install -c https://conda.binstar.org/jjhelmus opencv
```

ソースからコンパイルするとmakeにむちゃくちゃ時間がかかる。
依存関係のエラーも出る場合があるし。
でも、Anacondaを導入していれば上記のコマンド一発。
しかも、インストールもすぐ終わる。


# Webカメラの動作確認
Webカメラを繋いで、まずは既存のアプリケーションでOSがカメラを認識してくれるのか、
カメラが正しく動作するのかを確認。
cheeseというアプリケーションを使う。
私の環境には最初から入っていたが、apt-getで入手もできる。

```
$ cheese
```

アプリケーションウィンドウが立ち上がって映像が表示されればOK。
いくつかのフィルタをかけたり、録画ができる。


# Webカメラ画像のキャプチャ
## import
opencvをimportする必要がある。
他にもnumpyなどimportしておくと、キャプチャ画像を使って遊べる。

```python
import cv2
```

## キャプチャ
ビデオキャプチャ用のインスタンスを生成する。
カメラがopenされていなければ、IO Errorを上げて終了。

```python
cap = cv2.VideoCapture(0)
if cap.isOpened() is False:
   raise("IO Error")
```

↑で作成したインスタンスを使って
1フレームの画像をキャプチャしてframeに格納する。
retは画像取得の可否を示すフラグ。

```python
ret, frame = cap.read()
cv2.imshow('camera capture', frame)
```

最後にキャプチャ用のインスタンスを開放する。
```python
cap.release()
```

## エラーが！？

上記のコードでキャプチャできるはず。
なのに、以下のエラーが。

```
​​OpenCV Error: Unspecified error (The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Carbon support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script) in cvShowImage, file /opt/conda/conda-bld/opencv_1491943414359/work/opencv-3.1.0/modules/highgui/src/window.cpp, line 545
​​Traceback (most recent call last):
​​  File "<stdin>", line 1, in <module>
​​cv2.error: /opt/conda/conda-bld/opencv_1491943414359/work/opencv-3.1.0/modules/highgui/src/window.cpp:545: error: (-2) The function is not implemented. Rebuild the library with Windows, GTK+ 2.x or Carbon support. If you are on Ubuntu or Debian, install libgtk2.0-dev and pkg-config, then re-run cmake or configure script in function cvShowImage
```

とりあえずググったところ、エラーメッセージにあるように、
OpenCVの再インストールが必要らしい。
（[参考](http://qiita.com/SE96UoC5AfUt7uY/items/ea5ad55736e3e9470b6a)）
ターミナルで以下のコマンドを実行。

```
$ conda install -c menpo opencv
```

## これでキャプチャはできた
しかし、まだエラー（警告？）がでている。

```
​​HIGHGUI ERROR: V4L/V4L2: VIDIOC_S_CROP
```

ググッてみるとv4lというライブラリが必要らしい。
ならばとapt-getしても最新版が入っていると怒られる。

影響含め今後の課題として、先に進むことにしよう。

[ここまでのコード](https://github.com/tok41/ObjectTracker/blob/master/videoCapture/simpleVideoCapture.py)をgithubにアップしているので、
必要な方は参考にしていただけたらと。


# カラーフィルタを作ってみる
## やること
カメラからキャプチャした映像の中で、特定の色以外をマスクするフィルタを作る。
そして、リアルタイムでフィルタ処理した映像を表示する。

↓こんな画像を

![base_image](/images/raw_image.png)

↓こんな感じにする。元画像の赤成分のピクセルだけが残る。

![filtered_image](/images/filtered_image.png)

以下で説明するフィルタを実装して、webカメラ画像にフィルタを当てるコードを
githubにコードをアップしているので、
必要な方は参考にしていただけたらと。
（[ここ](https://github.com/tok41/ObjectTracker/blob/master/videoCapture/simpleColorTracker.py)）

## 色の認識

```cap.read()```でキャプチャした画像は[hight, width, color-channel]の
3次元配列になっている。
OpenCVでキャプチャした画像は、color-channelがBGRの3チャネル分なので、
color-channelを使えば、色の認識はできそうに思える。

しかし、光の当たり方など考慮した色の範囲を定義するのは難しい。
```[B,G,R]=[0, 0, 255]```なら赤として良いであろうが、
各チャネルの値の範囲をどこまで許すかは一概に決めるのはちょっと難しい
（適当に決めればできるだろうけど）。

そこで、
[HSV表現（Wikipedia）](https://ja.wikipedia.org/wiki/HSV%E8%89%B2%E7%A9%BA%E9%96%93)を
使って、色を定義する。

### HSV表現とは
すごーくざっくり言うと、
色をRGBじゃなくて、
色相(Hue)、彩度(Saturation)、明度(Brightness)の
三つの成分で定義する。

色相が0度から360度の範囲で色を定義する。
連続値で色を表現できるので、大きさ（範囲）を適当に決めれば
ちょっと色合いが違っていても赤なら赤と認識できる。

HSVの色相では、赤は0度、青は120度、緑は240度になる。


### HSV表現の計算
OpenCVで取得したBGR画像のHSV表現への変換はOpenCVで一発。

```python
frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
frame_h = frame_hsv[:,:,0] # 色相
frame_s = frame_hsv[:,:,1] # 彩度
frame_v = frame_hsv[:,:,2] # 明度
```

## フィルタの作成
ここで作成するフィルタは、指定範囲の色以外を真っ黒に塗りつぶす。
指定範囲の色部分だけをそのまま原画像を表示するというもの。

カラーフィルタ作成の手順は以下の通り

- 中央の色を指定（RGBで指定）
- HSV表現の範囲を計算
- キャプチャ画像の中で範囲に収まるピクセルを定義するROI（RegionOfInterest）を計算
- キャプチャ画像にROIをかける

### 中央の色を指定（RGBで指定）
RGBの値を3次元のタプルで指定する。
```python
color_map = (1,0,0)
```

### HSV表現の範囲を計算
Wikipediaのページを参考に、以下の関数getHueRangeを作成した。
getHueRangeは、color_mapにRGBで指定する中央の色を入力し、
そのcolor_mapから色相でh_widthの範囲までの色相の範囲を計算する。

```python
def getHueRange(color_map, h_width = 30):
    """
    Args:
      color_map : tuple(R,G,B), 0.0~1.0
      h_width : Hの範囲(degree)
    Returns:
      min_range_h : hの範囲の最小値
      max_range_h : hの範囲の最大値
    """
    # HSV表現の色相を計算する
    if np.argmin(color_map) == 0:
        # min=R
        h = 60.0 * ( (color_map[2] - color_map[1])
                         / (np.max(color_map) - np.min(color_map)) ) + 180.0
    elif np.argmin(color_map) == 1:
        # min=G
        h = 60.0 * ( (color_map[0] - color_map[2])
                         / (np.max(color_map) - np.min(color_map)) ) + 300.0
    else:
        # min=B
        h = 60.0 * ( (color_map[1] - color_map[0]) 
                    / (np.max(color_map) - np.min(color_map)) ) + 60.0
	# 0~255の整数に収める
    min_range_h = ((h-h_width)) * 255.0/360.0
    max_range_h = ((h+h_width)) * 255.0/360.0
    return (min_range_h, max_range_h)
```

定義に従ってRGBから色相を計算する。
色相の範囲は単純に幅（h_width）の足し引きしたものになる。
そして、OpenCVでの色相の範囲が0~255なので値を調整する。

彩度や明度も定義が必要だが、ここでは指定しない。

### ROI（RegionOfInterest）を計算
ここで作るROIは、キャプチャ画像の各ピクセルが、
上記で計算したHSV表現の色の範囲に収まっているのかを判定し、
範囲に収まっていれば1とし、それ以外を0とするもの。

gituhubに[アップしているコード](https://github.com/tok41/ObjectTracker/blob/master/videoCapture/simpleColorTracker.py)では、
getColorROIという関数に実装している。

まずは、キャプチャ画像をHSV表現に変換する。
```python
# BGRイメージをHSV表現に変換する
frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV_FULL)
frame_h = frame_hsv[:,:,0] # 色相
frame_s = frame_hsv[:,:,1] # 彩度
frame_v = frame_hsv[:,:,2] # 明度
```

次に、キャプチャ画像と同じサイズの0ベクトルを作成。
opencvでのキャプチャ画像がuint8なので、
型を揃えておくと後で計算が楽。
```python
roi = np.zeros_like(frame_h, dtype=np.uint8)
```

上記の手順で計算したHSV表現の範囲を```h_range```としておく。
ここまで彩度は定義して来なかったが、128以上としておく。
これらを使って、画像の各ピクセルが範囲内であれば1となるように
roiを設定する。
```python
roi[( ((frame_h>min_range_h)&(frame_h<=max_range_h))
	  | ((frame_h+255>min_range_h)&(frame_h+255<=max_range_h))
      ) & (frame_s>=saturation)] = 1
```
ここで、色相の範囲は0~255だが、getHueRangeで計算した色相の範囲は
単純に中央の値から範囲を±しているものなので、
範囲を超えることがある。
そのため、範囲を超えることを想定して、orで追加で範囲を指定。

### キャプチャ画像にROIをかける
キャプチャ画像にフィルタをかける。
単純に、3チャネル分の2次元配列に、ROIの値を掛ければ良い。

```python
# ROIを3チャネルに拡張
roi3 = np.concatenate(
	 (roi[:,:,np.newaxis], roi[:,:,np.newaxis], roi[:,:,np.newaxis])
     , axis=2)
frame_masked = frame * roi3

cv2.imshow('ColorTracker', frame_masked)
```

## 全体のコード
[github](https://github.com/tok41/ObjectTracker/blob/master/videoCapture/simpleColorTracker.py)にアップしています。

上記コードでは最初は原画像を表示しておき、
キー入力によって表示するカラーを指定する。

- r：赤だけを表示するフィルタを設定
- g：緑だけを表示するフィルタを設定
- b：青だけを表示するフィルタを設定
- p：原画像を表示
- q：終了



# 終わりに
OpenCVを使ってPythonでWebカメラの画像をキャプチャする手順を紹介した。
また、画像処理の簡単な例として、カラーフィルタを作成した。

## 今後の課題
ここまでで画像処理をやっていくための基礎ができたので、
今後は物体のトラッキングや認識などをやっていきたい

また、以下の警告の対応を検討する。

- V4L問題


# 参考
