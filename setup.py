# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe, sys

sys.argv.append("py2exe")

setup(
        options={"py2exe": {"bundle_files": 3}},
        zipfile=None,
        console=[{"script": "recordvideo.py"}]
<<<<<<< HEAD
=======
        # console=[{"script": "recordctrl.py"}]
>>>>>>> 70cb26cd34f68fd51deb10aeacf57f2b9ae11875
)
