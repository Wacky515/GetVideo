# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe, sys

sys.argv.append("py2exe")

setup(
        options={"py2exe": {"bundle_files": 3}},
        zipfile=None,
<<<<<<< HEAD
        # console=[{"script": "recordvideo.py"}]
        console=[{"script": "recordctrl.py"}]
=======
        console=[{"script": "recordvideo.py"}]
<<<<<<< HEAD
=======
        # console=[{"script": "recordctrl.py"}]
>>>>>>> 70cb26cd34f68fd51deb10aeacf57f2b9ae11875
>>>>>>> a7fce23a4fc32a82b1a1c70dd6a2f149e7c100e0
)
