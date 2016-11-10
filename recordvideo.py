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

# DONE:
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
    def __init__(self, cam_no=0, fps=None, interval=None, time_unit="min"):
        self.cam_no = cam_no
        self.fps = fps
        self.interval = interval

        self.unit = time_unit
        if time_unit == "min":
            self.time_unit = 60
        else:
            self.time_unit = 1

        print("Open CV: {}".format(cv2.__version__))

        self.now = datetime.datetime.today()
        self.now = self.now.strftime("%Y%m%d_%H-%M-%S")

        self.host = platform.uname()[1]
        print("PC name/Nama PC: {}".format(self.host))
        print("")

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

        self.cap = cv2.VideoCapture(int(cam_no))

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

        # fps 指定  # {{{
        if self.fps is None:
            print("Input record frame par sec( * [fps])")
            print("Masukan record frame par sec( * [fps])")

            print("<<<")
            self.fps = int(raw_input())
# }}}

        # 録画インターバル時間 指定
        if self.interval is None:
            print("Input record interval time [{}]".format(self.unit))
            print("Input under 0, not split video")
            print("")
            print("Masukan waktu interval  /per [{}]".format(self.unit))
            print("Jika masukan kurang dari 0, video tdk dipotong")

            print("<<<")
            self.interval = float(raw_input()) * self.time_unit
        else:
            self.interval = self.interval * self.time_unit

        print("Input: {}".format(self.interval))
# }}}

        # 保存名 指定  # {{{
        cvw = cv2.VideoWriter
        if os.name != "nt":
            filename = "rec_{}_{}.avi".format(self.host, self.now)
        elif os.name == "nt":
            filename = "..\\rec_{}_{}.avi".format(self.host, self.now)
        self.save = cvw(filename, self.fourcc, self.fps, self.size)
# }}}

    def run(self, windowname):
        """ 動画 録画 """

        start = time.time()

        while(self.cap.isOpened()):
            ret, frame = self.cap.read()

            if ret is True:
                cv2.imshow(windowname, frame)
                self.save.write(frame)

            if self.interval > 0:
                past = round(time.time() - start, 2)
                print("{0:.2f}/{1:.2f} [sec]".format(past, self.interval))
                if past > self.interval:
                    break

            if cv2.waitKey(1) == ord("q"):
                self.save.write(frame)
                print("Press \"q\" Key")
                sys.exit()

        # 全ストリーム 解放
        self.cap.release()
        self.save.release()
        cv2.destroyAllWindows()


def main():
    rec1 = Record(cam_no=0)
    # rec1 = Record(cam_no=0, fps=1, interval=0.05)
    rec1.run("REC (\"q\"key: quit)")

    # rec2 = Record(cam_no=6)
    # rec2.run("REC (\"q\"key: quit)")

if __name__ == "__main__":
    main()
