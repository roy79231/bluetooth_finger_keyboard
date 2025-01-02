# 藍芽手勢鍵盤

Made by Roy Yang

# 1. 介紹

這是個程式能夠讓raspberry pi4能夠透過鏡頭偵測手勢來模擬鍵盤輸入，那輸入的內容會透過藍芽傳到你想輸入的設備。

示意圖 (以下是輸入capslock的樣子) :　
![image](https://hackmd.io/_uploads/r1Vy3-ZU1e.png)


# 2. 所需設備

*  硬體
    1. raspberry pi4 (我使用的是model B)
    2. 攝像鏡頭模組
    * 組完示意圖

    ![471742449_570701075758329_6262762927944395521_n](https://hackmd.io/_uploads/Syvf5W781l.jpg)

* 作業系統 (x32位元)
    ![image](https://hackmd.io/_uploads/B1IqfzNLJl.png)


* 核心python套件
    1. mediapipe(手部辨識模型)
    2. openCV
    3. ffmpeg(一個組合包，為了能讓mediapipe正常運行)
    4. btferret(github上有人做的藍芽鍵盤輸入)

# 3. 安裝流程

## 1. 安裝openCV

1. 設定
```
sudo apt update && sudo apt upgrade -y
```

2. 安裝CMack3.14.4

```
cd ~/
wget https://github.com/Kitware/CMake/releases/download/v3.14.4/cmake-3.14.4.tar.gz
tar xvzf cmake-3.14.4.tar.gz
cd ~/cmake-3.14.4
cd ~/cmake-3.14.4
./bootstrap
make -j4
sudo make install
```

3. 安裝openCV

```
cd ~/
sudo apt install git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev libatlas-base-dev python3-scipy
git clone --depth 1 --branch 4.5.2-openvino https://github.com/opencv/opencv.git
cd opencv && mkdir build && cd build
cmake –DCMAKE_BUILD_TYPE=Release –DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j4
sudo make install
```

## 2. 安裝FFmpeg

1. 先安裝前置插件( fdk-aac, mp3lame, libass, x264 )，以確保後面下載能正常運行

```
sudo apt update
sudo apt install libfdk-aac-dev libmp3lame-dev libass-dev libx264-dev
```

2. 下載FFmpeg壓縮檔並解壓縮

```
wget https://ffmpeg.org/releases/ffmpeg-4.4.tar.bz2  -O ffmpeg.tar.bz2
tar xvf ffmpeg.tar.bz2
cd ffmpeg-*
```

3. 確認FFmpeg壓縮檔的內容

```
./configure \
--prefix=/usr \
--enable-gpl \
--enable-nonfree \
--enable-shared \
--enable-libtheora \
--enable-libvorbis \
--enable-omx \
--enable-omx-rpi \
--enable-mmal \
--enable-libxcb \
--enable-libfreetype \
--enable-libass \
--enable-gnutls \
--disable-opencl \
--enable-libcdio \
--enable-libbluray \
--extra-cflags="-march=armv8-a+crc+simd -mcpu=cortex-a72 -mfpu=neon-fp-armv8 -mtune=cortex-a72 -mfloat-abi=hard -O3" \
--enable-libx264 \
--enable-libfdk-aac \
--enable-libmp3lame \
--enable-avresample
```

4. 安裝FFmpeg
```
make -j4
sudo checkinstall -y --pkgname ffmpeg --pkgversion 4.4.0 make install
sudo dpkg -i ffmpeg_4.4.0-1_armhf.deb
```


常見的錯誤 : 
* configure那塊出現error -> 解法: 根據他哪個插件出現error就直接去install對應的插件( 那要注意載的環境對不對，sudo跟一般的環境是不同的，且要用pip3才會載到python3 )

## 3. 安裝mediapipe

1. 先安裝額外獨立的插件
    ```
    sudo apt install libxcb-shm0 libcdio-paranoia-dev libsdl2-2.0-0 libxv1  libtheora0 libva-drm2 libva-x11-2 libvdpau1 libharfbuzz0b libbluray2 libatlas-base-dev libhdf5-103 libgtk-3-0 libdc1394-22 libopenexr23
    ```

2. 安裝mediapipe
```
sudo pip3 install mediapipe-rpi4
```

## 4. 安裝btferret

1. 先安裝些基本的藍牙套件
```
sudo apt-get install libbluetooth-dev python-gobject bluez bluez-tools bluez-firmware python-bluez python-dev python-pip
pip install pybluez evdev pydbus future
```

2. 把btferret從github上抓下來
```
sudo git clone https://github.com/petzval/btferret.git
cd btferret
```

3. 建立btferret環境

    ```
    sudo apt-get install python3-setuptools
    sudo python3 btfpy.py build
    sudo python3 btferret.py
    ```

    * 常出現錯誤 : 
    * ![iot_error](https://hackmd.io/_uploads/BkTMFfNUye.png) -> 解法:去device.txt把DEVICE=MyPI TYPE=MESH  NODE=1  這行的ADDRESS改成ADDRESS=AA:AA:AA:AA:AA:AA

4. 測試
    ```
    sudo python3 keyboard.py
    ```
    * 這時其他設備可以在藍芽上看到有名為HID的鍵盤可以連線，連線後就可以透過樹莓派的鍵盤做輸入了

    * 常出現錯誤 :　
    * ![image](https://hackmd.io/_uploads/Bk3hnM4Lyg.png)-> 解法:去keyboard.txt把DEVICE=MyPI TYPE=MESH  NODE=1 這行的ADDRESS改成 ADDRESS=AA:AA:AA:AA:AA:AA
    * 有時也會要求00:00:00:00:00:00 -> 那就同樣一行改00:00:00:00:00:00


## 下載本程式並執行
1. 
    ```
    cd .. 
    sudo git clone https://github.com/roy79231/bluetooth_finger_keyboard.git
    ```

2. 將檔案(keyboard_finger.py)移至btferret資料夾裡面

3. 到資料夾並執行
    ```
    cd btferret
    sudo python3 keyboard_finger.py
    ```
    
# 4. 程式說明

# 參考文件
1. mediapipe安裝手冊( https://pypi.org/project/mediapipe-rpi4/ )
2. FFmpeg+openCV安裝手冊( https://github.com/superuser789/MediaPipe-on-RaspberryPi/blob/main/BuildingFFMPEG%26OpenCV.md ) 
3. openvino設置文件( https://hackmd.io/HV6hQ2PHSiWlrRsfxC10SA )
4. 透過樹莓派把連線鍵盤變藍芽鍵盤( https://schaepher.github.io/2021/01/31/raspberry-bluetooth-keyboard/ )
5. btferret插件( https://github.com/petzval/btferret )