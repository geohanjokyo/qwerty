import unittest
import os
import pandas as pd
from appium import webdriver
from time import sleep

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from appium.webdriver.common.touch_action import TouchAction
import time, datetime
import cv2
import subprocess
import detect

# 오브젝트 딕셔너리
qwerty_dic = {"cancle": "0", "confirm": "1", "1": "2", "2": "3", "3": "4", "4": "5", "5": "6", "6": "7",
              "7": "8", "8": "9", "9": "10", "0": "11", "q": "12", "w": "13", "e": "14", "r": "15", "t": "16",
              "y": "17", "u": "18", "i": "19", "o": "20", "p": "21", "a": "22", "s": "23", "d": "24", "f": "25",
              "g": "26", "h": "27", "j": "28", "k": "29", "l": "30", "z": "31", "x": "32", "c": "33", "v": "34",
              "b": "35", "n": "36", "m": "37", "Q": "38", "W": "39", "E": "40", "R": "41", "T": "42", "Y": "43",
              "U": "44", "I": "45", "O": "46", "P": "47", "A": "48", "S": "49", "D": "50", "F": "51", "G": "52",
              "H": "53", "J": "54", "K": "55", "L": "56", "Z": "57", "X": "58", "C": "59", "V": "60", "B": "61",
              "N": "62", "M": "63", "shift": "64", "sc": "65", "eng": "66", "!": "67", "@": "68", "#": "69",
              "$": "70", "%": "71", "^": "72", "&": "73", "*": "74", "(": "75", ")": "76", "-": "77", "=": "78",
              "+": "78", "{": "80", "}": "81", "[": "82", "]": "83", "\ ": "84", ":": "85", ";": "86",
              "qoute_L": "87", "qoute_S": "88", "<": "89", ">": "90", ",": "91", ".": "92", "/": "93",
              "?": "94", "|": "95", "~": "96", "`": "97", "_": "98"}
# 대소문자 리스트
small_list = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "q", "w", "e", "r", "t", "y", "u", "i", "o",
              "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m"]
large_list = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "Q", "W", "E", "R", "T", "Y", "U", "I", "O",
              "P", "A", "S", "D", "F", "G", "H", "J", "K", "L", "Z", "X", "C", "V", "B", "N", "M"]

class kbdtest_lowres(unittest.TestCase):

    def setUp(self):
        # Set up appium
        self.driver = webdriver.Remote(
            command_executor='http://localhost:4723/wd/hub',
            desired_capabilities={
                "platformName": "Android",
                "platformVersion": "10",
                "deviceName": "V50",
                "automationName": "Appium",
                "newCommandTimeout": 3000,
                "appPackage": "com.kbstar.kbbank", #국민은행 app 실행
                "appActivity": "com.kbstar.kbbank.view.Intro",
                "udid": "LMV500N3b70a631",
                "noReset": "True" #app 데이터(인증정보) 유지
            })

    def test_search_field(self):

        # appiun의 webdriver를 초기화 합니다.
        driver = self.driver
        # selenium의 WebDriverWait을 사용합니다. element가 나올때 까지 최고 20초까지 기다립니다.
        wait = WebDriverWait(driver, 20)
        # 테스트 시나리오에 따라 selenium 작성

        # 공인인증서 버튼을 찾아 누르기
        el = self.driver.find_element_by_xpath("/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.RelativeLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout/android.widget.LinearLayout")
        sleep(1)
        el.click()
        sleep(5)
        # 인증서 비밀번호 입력

        # 인증서 암호 입력
        cert_pass = ""  # 인증서 비빌번호
        cert_list = []  # 빈 리스트 선언
        # 비밀번호 인덱싱 하여 리스트 선언
        for i in range(len(cert_pass)):
            p = cert_pass[i]
            cert_list.append(p)
        # 인증서 비밀번호 입력
        for i in cert_list:
            # 소문자/숫자 일 경우
            if i in small_list:
                self.driver.tap([(290, 2110)])  # eng버튼 tap
                sleep(2)
                # 캡쳐보드에서 스크린샷 찍어 저장
                cam = cv2.VideoCapture(2) #스크립트 실행하려는 PC의 캡져 장비에 맞게 수정 필요
                cam.set(3, 1920)
                cam.set(4, 1080)
                ret, frame = cam.read()
                # 핸드폰 영역 자르기
                crop = frame.copy()
                crop = frame[0:1080, 720:1200]
                # png로 압축 없이 이미지 저장
                cv2.imwrite('temp.png', crop, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
                cam.release()
                # 저장한 스크린샷으로 detect
                os.system(
                    'python detect.py --weights last_temp.pt --img 1088 --conf 0.4  --save-txt --device cpu --source ./temp.png')
                # 딕셔너리에서 밸류값(학습시 부여한 오브젝트 아아이디) 추출
                i_val = int(qwerty_dic[i])
                # detect 결과에서 오브젝트 좌표 보정
                loc = pd.read_csv("./inference/output/temp.txt", sep=" ", header=None)
                loc = loc.drop([5], axis=1)
                loc.columns = ["classID", "x", "y", "width", "height"]
                loc["x_lo"] = loc["x"] * 720  # V50 낮음 해상도
                loc["y_lo"] = loc["y"] * 1560
                # 추출한 좌표로 tap
                x_loc = int(loc.x_lo[loc["classID"] == i_val])
                y_loc = int(loc.y_lo[loc["classID"] == i_val])
                sleep(5)
                self.driver.tap([(x_loc, y_loc)])
                # 현재 시간 선언
                timenow = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                # detect 결과 이미지를 불러와 현재시간을 파일명으로 저장
                dect = cv2.imread("./inference/output/temp.png")
                cv2.imwrite('./detected/' + timenow + '.png', dect)
                sleep(2)
            # 대문자일 경우
            elif i in large_list:
                self.driver.tap([(290, 2110)])  # eng버튼 tap
                sleep(2)
                self.driver.tap([(90, 1900)])  # shift버튼 tap
                sleep(2)
                # 캡쳐보드에서 스크린샷 찍어 저장
                cam = cv2.VideoCapture(2)
                cam.set(3, 1920)
                cam.set(4, 1080)
                ret, frame = cam.read()
                # 핸드폰 영역 자르기
                crop = frame.copy()
                crop = frame[0:1080, 720:1200]
                # png로 압축 없이 이미지 저장
                cv2.imwrite('temp.png', crop, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
                cam.release()
                # 저장한 스크린샷으로 detect
                os.system(
                    'python detect.py --weights last_temp.pt --img 1088 --conf 0.4  --save-txt --device cpu --source ./temp.png')
                # 딕셔너리에서 밸류값(학습시 부여한 오브젝트 아아이디) 추출
                i_val = int(qwerty_dic[i])
                # detect 결과에서 오브젝트 좌표 보정
                loc = pd.read_csv("./inference/output/temp.txt", sep=" ", header=None)
                loc = loc.drop([5], axis=1)
                loc.columns = ["classID", "x", "y", "width", "height"]
                loc["x_lo"] = loc["x"] * 720  # V50 낮음 해상도
                loc["y_lo"] = loc["y"] * 1560
                # 추출한 좌표로 tap
                x_loc = int(loc.x_lo[loc["classID"] == i_val])
                y_loc = int(loc.y_lo[loc["classID"] == i_val])
                sleep(5)
                self.driver.tap([(x_loc, y_loc)])
                # 현재 시간 선언
                timenow = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                # detect 결과 이미지를 불러와 현재시간을 파일명으로 저장
                dect = cv2.imread("./inference/output/temp.png")
                cv2.imwrite('./detected/' + timenow + '.png', dect)
                sleep(2)
            # 그 외 문자일 경우
            else:
                self.driver.tap([(290, 2110)])  # eng버튼 tap
                sleep(2)
                self.driver.tap([(100, 2100)])  # sc버튼 tap
                sleep(2)
                # 캡쳐보드에서 스크린샷 찍어 저장
                cam = cv2.VideoCapture(2)
                cam.set(3, 1920)
                cam.set(4, 1080)
                ret, frame = cam.read()
                # 핸드폰 영역 자르기
                crop = frame.copy()
                crop = frame[0:1080, 720:1200]
                # png로 압축 없이 이미지 저장
                cv2.imwrite('temp.png', crop, params=[cv2.IMWRITE_PNG_COMPRESSION, 0])
                cam.release()
                # 저장한 스크린샷으로 detect
                os.system(
                    'python detect.py --weights last_temp.pt --img 1088 --conf 0.4  --save-txt --device cpu --source ./temp.png')
                # 딕셔너리에서 밸류값(학습시 부여한 오브젝트 아아이디) 추출
                i_val = int(qwerty_dic[i])
                # detect 결과에서 오브젝트 좌표 보정
                loc = pd.read_csv("./inference/output/temp.txt", sep=" ", header=None)
                loc = loc.drop([5], axis=1)
                loc.columns = ["classID", "x", "y", "width", "height"]
                loc["x_lo"] = loc["x"] * 720  # V50 낮음 해상도
                loc["y_lo"] = loc["y"] * 1560
                # 추출한 좌표로 tap
                x_loc = int(loc.x_lo[loc["classID"] == i_val])
                y_loc = int(loc.y_lo[loc["classID"] == i_val])
                sleep(5)
                self.driver.tap([(x_loc, y_loc)])
                # 현재 시간 선언
                timenow = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
                # detect 결과 이미지를 불러와 현재시간을 파일명으로 저장
                dect = cv2.imread("./inference/output/temp.png")
                cv2.imwrite('./detected/' + timenow + '.png', dect)
                sleep(2)
        sleep(2)
        # 확인 버튼 tap
        self.driver.tap([(780, 1010)])
        sleep(20)
        # 이후 테스트 시나리오 추가 가능


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(kbdtest_lowres)
    unittest.TextTestRunner(verbosity=2).run(suite)