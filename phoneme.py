# -*-coding: utf-8-*-
"""音素クラス
    self.phoneme: 音素名
        - ショートポーズはpau
    self.config_file: 設定ファイル(algn_sec)
    self.begin: 音素の開始時間(sec)
    self.end: 音素の終了時間(sec)
"""
import ConfigParser

class Phoneme:
  def __init__(self, phoneme):
    if phoneme == ':': phoneme = 'pau'
    self.phoneme = phoneme
    self.config_file = './config.ini'
    self.begin = None
    self.end = None

  def set_tmstmp(self, line):
    b, e, phoneme = line.rstrip().split(' ')
    if phoneme != self.phoneme:
      raise ValueError("ValueError: {0} doesn't match {1}".format(self.phoneme, phoneme))
    
    inifile = ConfigParser.SafeConfigParser()
    inifile.read(self.config_file)
    algn_sec = int(inifile.get('analysis', 'algn_sec'))
    self.begin = float(b) / algn_sec
    self.end = float(e) / algn_sec

  def __str__(self):
    return '{0}: {1}~{2}'.format(self.phoneme, self.begin, self.end)
