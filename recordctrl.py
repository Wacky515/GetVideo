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
# Licence:     SDS1001* + 1
# -------------------------------------------------------------------------------

# モジュールインポート
import sys

# !!!: "*.exe" 化する時にこの import 順は必須
import numpy
import cv2

import time
import recordvideo as rv


class LoopRecord:
    """ 録画ループ時間管理クラス """
    def __init__(self):
        pass

    def run(self, interval=10):
        """ 録画 ループ """
        while(True):
            start = time.time()
            print(start)

            rec = rv.Record()
            rec.run("REC loop")

            past = time.time()
            print(past)

            if start - past > interval:
                continue

        if cv2.waitKey(1) == ord("e"):
            sys.exit()


def main():
    lrc = LoopRecord()
    lrc.run()

if __name__ == "__main__":
    main()
