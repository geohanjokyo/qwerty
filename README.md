# 딥러닝 & 테스트 자동화 with 가상키보드
https://youtu.be/Dn19RQ6Loqw
<-- 실행하는 영상입니다.

딥러닝 사물인식 기술을 응용하여 가상키보드를 대상으로 자동화를 진행하였습니다.   
국민은행 APP으로 공인인증서 로그인 시 가상키보트로 인증서암호를 입력합니다.   
학습 및 인식에는 yolo v5모델(https://github.com/ultralytics/yolov5)을 이용하였습니다.   
가상키보드의 화면은 캡쳐가 불가능하여 미라캐스르를 이용하여 화면을 미러링하여 캡쳐하였고   
가상키보드에서 위치가 고정된 버튼은 고정 좌표로 누르도록 제어 하였습니다.   
   
   
## 실행환경
-	OS : Windows 10 Education(bootcamp)
-	python 3.7
- Appium v1.17.1
- apache-ant-1.10.8
-	H/W : macbook pro 13.3(2018)
        LG V50
        AVerMedia LIVE GAMER PORTABLE2(영상 캡쳐 장비)
        Coms ST045 미라캐스트 동글

   
   
## 주요 파일 설명
- kbd.py : 자동화 수행을 위한 appium 스크립트 파일(유튜브 영상은 이 파일을 실행한 결과입니다.)   
- last_temp.pt : 학습결과(가중치) 파일    
- kbkbd.ipynb : 학습 실행하였던 주피터노트북 파일   
- train.py : 학습 code(yolo v5)   
- detect.py : 인식 code(yolo v5)   
- test.py : 학습결과 test code(yolo v5)   
- data.yaml : 학습데이터(이미지) 위치 및 클래스(레이블) 설정 파일    
   
   
## 실행 방법
1. 아나콘다 설치 후 가상환경 생성   
2. appium 설치 및 환경 설정   
3. 필요 라이브러리 설치(pytourch & requirements.txt파일 내 라이브러리)   
4. 영상 캡쳐 장비 및 미라캐스트 동글 설치   
5. 안드로이드 단말기에 국민은행 APP을 설치하고 공인인증서 로그인을 1회 수행   
6. kbd.py 파일을 실행   
   
   
## 커스텀 데이터 학습
제가 학습한 앱(가상키보드)이 아닌 다른 앱의 오브젝트를 제어하고 싶으시면   
아래와 같이 데이터 학습을 진행해 주세요.   
1. 아나콘다 설치 후 가상환경 생성   
2. yolo v5(https://github.com/ultralytics/yolov5) 클론   
3. 학습 데이터셋(이미지)준비
4. labelimg(https://github.com/tzutalin/labelImg)를 이용하여 학습데이터(이미지) 라벨링(yolo 포맷)   
5. data.yaml에 라벨링한 클래스 수와 이름을 입력   
6. 학습용 이미지와 라벨링 파일을 ./train/images, ./train/label 폴더에 복사   
7. validation용 이미지와 라벨링 파일을 ./valid/images, ./valid/label 폴더에 복사   
8. test용  이미지와 라벨링 파일을 ./test/images, ./test/label 폴더에 복사   
(학습 시 자동으로 test 수행)
9. train.py로 학습 실행   
```
$ python train.py --data data.yaml --cfg yolov5s.yaml --weights '' --batch-size 64
                                         yolov5m                                40
                                         yolov5l                                24
                                         yolov5x                                16
``` 
10. 생성된 가중치 파일(.runs\exp*_****\weights\****.pt)파일을 복사 하여 detect.py 실행 시 이용
커스텀 데이터 에 맞게 appium 스크립트 수정이 필요합니다.   
(app name, app activity, 오브젝트 ID, 고정 버튼 좌표 등등)
