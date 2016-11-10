# !/usr/bin/python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Name:        recorctrl.py
# Purpose:     In README.md
#
# Author:      Kilo11
#
# Created:     02/11/2016
# Copyright:   (c) SkyDog 2016
# Licence:     SDS10015
# -----------------------------------------------------------------------------
# TODO:
# カメラの複数台ハンドリング

# モジュールインポート

# !!!: "*.exe" 化する時にこの import 順は必須
import numpy
import cv2
import cv2.cv as cv

import sys
import datetime

import recordvideo as rv

# sysモジュール リロード
reload(sys)

# デフォルトの文字コード 出力
sys.setdefaultencoding("utf-8")


class LoopRecord:
    """ 録画ループ時間管理クラス """
    def __init__(self, time_unit="min"):
        self.time_unit = time_unit

        self.now = datetime.datetime.today()
        self.now = self.now.strftime("%Y%m%d_%H-%M-%S")

        print("Now/Sekarang: {}".format(self.now))
        print("")

    def run(self):
        """ 録画 ループ """
        # fps 指定  # {{{
        print("Input record frame par sec( * [fps])")
        print("Masukan record frame par sec( * [fps])")

        print("<<<")
        fps = int(raw_input())
# }}}

        # 録画インターバル時間 指定  # {{{
        print("Input record interval time [{}]".format(self.time_unit))
        print("Input under 0, not split video")
        print("")
        print("Masukan waktu interval  /per [{}]".format(self.time_unit))

        print("Jika masukan kurang dari 0, video tdk dipotong")

        print("<<<")
        interval = float(raw_input())
# }}}

        while(True):
            rec = rv.Record(fps=fps, interval=interval)
            rec.run("REC loop (\"q\"key: quit)")

        if cv2.waitKey(1) == ord("e"):
            print("Press \"e\" Key")
            sys.exit()


def main():
    lrc = LoopRecord()
    lrc.run()

if __name__ == "__main__":
    main()
