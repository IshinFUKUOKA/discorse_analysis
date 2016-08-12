# -*-coding: utf-8-*-

from Tkinter import *
import tkSnack
import glob
import numpy as np
import os

if __name__ == '__main__':
  wavs = glob.glob('/home/fukuoka/data/GCS_recording201608/wave/*.wav')
  output_dir = '/home/fukuoka/data/GCS_recording201608/power'
  for wav in wavs[:4]:
    base = os.path.basename(wav)
    root = Tk()
    tkSnack.initializeSnack(root)
    mySound = tkSnack.Sound()
    mysound.read(wav)
    pwlist = mysound.power()
    np.savetxt('{0}/{1}'.format(output_dir, base))
