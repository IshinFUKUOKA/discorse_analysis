# -*-coding: utf-8-*-

import sys
import glob
import numpy as np
import ConfigParser
from mora import Mora

class Utterance:
  def __init__(self, utterance_id):
    self.utterance_id = utterance_id 
    self.moras = []
    self.breath_groups = []
    self.pauses = []
    self.config_file = './config.ini'

  def set_text(self, text):
    self.text = text

  def set_hira(self, hira):
    self.hira = hira

  def set_phon(self, phon):
    self.phon = phon
    for mora in self.phon.split(' '):
      if mora in ['/', '//', '@']: continue
      if mora == '%':
        self.moras[-1].add_long_vowel()
        continue

      self.moras.append(Mora(mora))

  def set_algn(self, algn):
    self.algn = algn
    algn = algn[1:-1] # sil削除
    for phonemes in [m.phonemes for m in self.moras]:
      for p in phonemes:
        p.set_tmstmp(algn[0])
        algn = algn[1:]

  def set_pitch(self, pitch):
    self.pitch = pitch

  # 指定した区間のF0を取得する
  # begin, end: msec
  def get_pitch(self, begin, end):
    inifile = ConfigParser.SafeConfigParser()
    inifile.read(self.config_file)
    f0_width = int(inifile.get('analysis', 'f0_width')) / 1000.0
    b_idx = int(begin / f0_width)
    e_idx = int(end / f0_width)
    return self.pitch[b_idx:e_idx]
  
  def get_pauses(self):
    real_pauses = [m for m in self.moras if m.mora == ':']
    dummy = Mora(':')
    dummy.phonemes[0].set_tmstmp('0 0 pau')
    return real_pauses + [dummy]

  def get_first_mora_time(self):
    """冒頭3モーラの時間を取得
    返り値: (begin, end)のタプル
    """
    num = 3
    begin = self.moras[0].get_begin()
    end = self.moras[num -1].get_end()
    return (begin, end)

  def get_last_mora_time(self):
    """末尾3モーラの時間を取得
    返り値: (begin, end)のタプル
    """
    num = 3
    begin = self.moras[-num].get_begin()
    end = self.moras[-1].get_end()
    return (begin, end)

  def get_whole_time(self):
    begin = self.moras[0].get_begin()
    end = self.moras[-1].get_end()
    return (begin, end)

  def __str__(self):
    s = 'text: ' + self.text
    s += ', hira: ' + self.hira
    s += ', phon: ' + self.phon
    return s
