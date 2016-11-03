# !/usr/bin/python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        recordvideo.py
# Purpose:     Record video
#
# Author:      Kilo11
#
# Created:     02/11/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS1001*
# -------------------------------------------------------------------------------

# TODO: *.exe化

# モジュールインポート

# !!!: "*.exe" 化する時にこの import 順は必須
import numpy
import cv2

import os
import time
import datetime
import platform


class Record:
    """ 録画クラス """
    def __init__(self):
        self.now = datetime.datetime.today()
        self.now = self.now.strftime("%Y%m%d_%H-%M-%S")
        self.host = platform.uname()[1]

        print("Now: {}".format(self.now))
        print("PC name: {}".format(self.host))

        if os.name != "nt":
            self.fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')

        elif os.name == "nt":
            # fourccs = [  #{{{
            #         cv2.VideoWriter_fourcc(*"DIB "),  # No compress
            #         cv2.VideoWriter_fourcc(*"PIM1"),  # MPEG-1
            #         cv2.VideoWriter_fourcc(*"MJPG"),  # Motion-JPEG
            #                                           # (Not so good)
            #         cv2.VideoWriter_fourcc(*"MP42"),  # MPEG-4.2
            #         cv2.VideoWriter_fourcc(*"DIV3"),  # MPEG-4.3
            #         cv2.VideoWriter_fourcc(*"DIVX"),  # MPEG-4
            #         cv2.VideoWriter_fourcc(*"U263"),  # H263
            #         cv2.VideoWriter_fourcc(*"I263"),  # H263I
            #         cv2.VideoWriter_fourcc(*"FLV1"),  # FLV1
            #
            #         cv2.VideoWriter_fourcc(*"MP4V"),
            #         # cv2.VideoWriter_fourcc(*"MP4S"),
            #         # cv2.VideoWriter_fourcc(*"XVID")
            #
            #         -1                                # Show dialog
            #
            #         ]
            #
            # # http://www.fourcc.org/codecs.php
            # }}}

            # self.fourcc = 1
            # self.fourcc = fourccs[-2]
            # self.fourcc = fourccs[1]
            self.fourcc = cv2.VideoWriter_fourcc(*"PIM1")

        self.cap = cv2.VideoCapture(0)

        print("Input record frame par sec")

        self.fps = int(raw_input())

        if os.name != "nt":
            width = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))
            height = int(self.cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))

        elif os.name == "nt":
            width = int(self.cap.get(3))
            height = int(self.cap.get(4))

        self.size = (width, height)
        # Memo
        # キャプチャより保存画角が大きい場合、自動でスケーリング

        cvw = cv2.VideoWriter
        filename = "rec_{}_{}.avi".format(self.host, self.now)
        self.save = cvw(filename, self.fourcc, self.fps, self.size)

    def run(self, windowname):
        """ 動画 録画 """
        print("Input record interval time [sec]")
        print("Input under 0, not split video")

        interval = raw_input()

        start = time.time()

        while(self.cap.isOpened()):
            ret, frame = self.cap.read()

            if ret is True:
                cv2.imshow(windowname, frame)
                self.save.write(frame)

            if interval > 0:
                interval = int(interval) * 1.00
                past = round(time.time() - start, 2)
                print("{0:.2f}/{1:.2f} [sec]".format(past, interval))
                if past > interval:
                    break

            if cv2.waitKey(1) == ord("q"):
                break

        # 全ストリーム 解放
        self.cap.release()
        self.save.release()
        cv2.destroyAllWindows()


def main():
    rec = Record()
    rec.run("REC")

if __name__ == "__main__":
    main()
