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
# Licence:     SDS1001* + 1
# -----------------------------------------------------------------------------

# モジュールインポート
import datetime
import recordvideo as rv


class LoopRecord:
    """ 録画ループ時間管理クラス """
    def __init__(self):
        self.now = datetime.datetime.today()
        self.now = self.now.strftime("%Y%m%d_%H-%M-%S")

        print("Now/Sekarang: {}".format(self.now))
        print("")

    def run(self):
        """ 録画 ループ """
        # fpc 指定  # {{{
        print("Input record frame par sec( * [fpc])")
        print("Masuk record frame par sec( * [fpc])")

        print("<<<")
        fps = int(raw_input())
# }}}

        # 録画インターバル時間 指定  # {{{
        print("Input record interval time [sec]")
        print("Input under 0, not split video")
        print("")
        print("Masuk waktu yg potong record")
        print("Kalau masuk kurang 0, tdk potong")

        print("<<<")
        interval = raw_input()
# }}}

        while(True):
            rec = rv.Record(fps, interval)
            rec.run("REC loop")


def main():
    lrc = LoopRecord()
    lrc.run()

if __name__ == "__main__":
    main()
