# !/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        recordvideo.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     02/11/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10014
# -----------------------------------------------------------------------------
# TODO:

# FIXME:

# DONE:
# "print"文 関数化
# "frame_size_error" が出る
# -> 未接続カメラの "imshow" と "write" のエラー
# 接続していないカメラも保存される
# cam2以降が1フレームしか保存されない
# sec -> min
# *.exe化

# モジュールインポート

# !!!: "*.exe" 化する時にこの import 順は必須
import numpy
import cv2
import cv2.cv as cv

import os
import sys
import time
import datetime
import platform

# sysモジュール リロード
reload(sys)

# デフォルトの文字コード 出力
sys.setdefaultencoding("utf-8")


class Record:
    """ 録画クラス """
    def __init__(self, fps=None, interval=None, time_unit="min"):
        self.fps = fps
        self.interval = interval

        self.camera = False
        self.camera2 = False
        self.camera3 = False
        self.camera4 = False

        self.unit = time_unit
        if time_unit == "min":
            self.time_unit = 60
        else:
            self.time_unit = 1

        self.now = datetime.datetime.today()
        self.now = self.now.strftime("%Y%m%d_%H-%M-%S")

        self.host = platform.uname()[1]

        self.cap = cv2.VideoCapture(0)
        self.cap2 = cv2.VideoCapture(1)
        self.cap3 = cv2.VideoCapture(2)
        self.cap4 = cv2.VideoCapture(3)

        if self.cap.isOpened():
            self.camera = True

            # コーデック 選択  # {{{
            # OpenCV バージョン差の吸収
            cv_ver = cv2.__version__  # {{{
            if cv_ver[0] == "2":
                cvf = cv.CV_FOURCC
            else:
                cvf = cv2.VideoWriter_fourcc
                # }}}

            if os.name != "nt":
                self.fourcc = cvf("m", "p", "4", "v")

            elif os.name == "nt":
                fourccs = [
                        # {{{
                        cvf(*"DIB "),  # No compress
                        cvf(*"PIM1"),  # MPEG-1
                        cvf(*"MJPG"),  # Motion-JPEG
                                    # (Not so good)
                        cvf(*"MP42"),  # MPEG-4.2
                        cvf(*"DIV3"),  # MPEG-4.3
                        cvf(*"DIVX"),  # MPEG-4
                        cvf(*"U263"),  # H263
                        cvf(*"I263"),  # H263I
                        cvf(*"FLV1"),  # FLV1

                        cvf(*"MP4V"),  # MPEG-4
                        cvf(*"MP4S"),  # MPEG-4
                        cvf(*"XVID"),  # XVID MPEG-4
                        # http://www.fourcc.org/codecs.php

                        # }}}
                        0,
                        1,
                        -1]            # Show dialog

                self.fourcc = fourccs[-2]
# }}}

            # fps 指定  # {{{
            if self.fps is None:
                print("Input record frame par sec( * [fps])")
                print("Masukan record frame par sec( * [fps])")
                print("<<<")
                print("")

                self.fps = int(raw_input())
# }}}

            # 画角 指定  # {{{
            if os.name != "nt":
                width = int(self.cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
                height = int(self.cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))

            elif os.name == "nt":
                width = int(self.cap.get(3))
                height = int(self.cap.get(4))

            self.size = (width, height)
            # Memo
            # キャプチャより保存画角が大きい場合、自動でスケーリング
# }}}

            # 録画インターバル時間 指定  # {{{
            if self.interval is None:
                print("Input record interval time [{}]".format(self.unit))
                print("Input under 0, not split video")
                print("")
                print("Masukan waktu interval  /per [{}]".format(self.unit))
                print("Jika masukan kurang dari 0, video tdk dipotong")
                print("<<<")
                print("")

                self.interval = float(raw_input()) * self.time_unit

            else:
                self.interval = self.interval * self.time_unit
# }}}

            # 保存名 指定  # {{{
            self.cvw = cv2.VideoWriter
            sht = self.host
            sow = self.now

            try:
                if os.name != "nt":
                    filename = "cam01_{}_{}_{}.avi".format(sht, sow)
                    filename2 = "cam02_{}_{}_{}.avi".format(sht, sow)
                    filename3 = "cam03_{}_{}_{}.avi".format(sht, sow)
                    filename4 = "cam04_{}_{}_{}.avi".format(sht, sow)

                elif os.name == "nt":
                    filename = "..\\cam01_{}_{}.avi".format(sht, sow)
                    filename2 = "..\\cam02_{}_{}.avi".format(sht, sow)
                    filename3 = "..\\cam03_{}_{}.avi".format(sht, sow)
                    filename4 = "..\\cam04_{}_{}.avi".format(sht, sow)

            except Exception as vwerror:
                print("=== Video write error ===")
                print("Type: " + str(type(vwerror)))
                print("Args: " + str(vwerror.args))
                print("Message: " + vwerror.message)
                print("Error: " + str(vwerror))
                print("")

            self.save = self.cvw(filename, self.fourcc, self.fps, self.size)

            print("Open CV: {}".format(cv2.__version__))
            print("PC name/Nama PC: {}".format(self.host))
            print("")

            sfur = self.fourcc

            if self.cap2.isOpened():
                self.save2 = self.cvw(filename2, sfur, self.fps, self.size)
                self.camera2 = True

            if self.cap3.isOpened():
                self.save3 = self.cvw(filename3, sfur, self.fps, self.size)
                self.camera3 = True

            if self.cap4.isOpened():
                self.save4 = self.cvw(filename4, sfur, self.fps, self.size)
                self.camera4 = True
# }}}

        else:
            print("No camera")
            sys.exit()

    def run(self, windowname):
        """ 動画 録画 """
        start = time.time()

        while(self.cap.isOpened()):
            try:
                ret, frame = self.cap.read()
                ret2, frame2 = self.cap2.read()
                ret3, frame3 = self.cap3.read()
                ret4, frame4 = self.cap4.read()

            except Exception as gverror:
                print("=== Get video error ===")
                print("Type: " + str(type(gverror)))
                print("Args: " + str(gverror.args))
                print("Message: " + gverror.message)
                print("Error: " + str(gverror))
                print("")

            if ret is True:
                try:
                    cv2.imshow(windowname, frame)
                    self.save.write(frame)

                        if self.camera2 is True:
                            cv2.imshow(windowname + " 2", frame2)
                            self.save2.write(frame2)

                        if self.camera3 is True:
                            cv2.imshow(windowname + " 3", frame3)
                            self.save3.write(frame3)

                        if self.camera4 is True:
                            cv2.imshow(windowname + " 4", frame3)
                            self.save4.write(frame4)

                except Exception as sverror:
                    print("=== Show video error ===")
                    print("Type: " + str(type(sverror)))
                    print("Args: " + str(sverror.args))
                    print("Message: " + sverror.message)
                    print("Error: " + str(sverror))
                    print("")

            if self.interval > 0:
                past = round(time.time() - start, 2)
                print("{0:.2f}/{1:.2f} [sec]".format(past, self.interval))
                if past > self.interval:
                    break

            if cv2.waitKey(1) == ord("q"):
                # self.save.write(frame)
                print("Press \"q\" Key")
                sys.exit()

        # 全ストリーム 解放
        self.cap.release()
        self.save.release()

        if self.camera2 is True:
            self.cap2.release()
            self.save2.release()
            self.camera2 = False

        if self.camera3 is True:
            self.cap3.release()
            self.save3.release()
            self.camera3 = False

        if self.camera4 is True:
            self.cap4.release()
            self.save4.release()
            self.camera4 = False

        cv2.destroyAllWindows()


def main():
    # rec1 = Record()
    # rec1 = Record(fps=1, interval=1)
    rec1 = Record(fps=1, interval=0.05)
    # rec2 = Record(fps=1, interval=0.05)

    rec1.run("REC (\"q\"key: quit)")
    # rec2.run("REC2 (\"q\"key: quit)")

if __name__ == "__main__":
    main()
