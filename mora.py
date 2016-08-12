# -*-coding: utf-8-*-
from phoneme import Phoneme

class Mora:
  def __init__(self, mora_str):
    self.mora = mora_str
    self.phonemes = [Phoneme(p) for p in self.mora.split('~')]

  def add_long_vowel(self):
    self.mora += '%'
    self.phonemes[-1].phoneme += '%'

  def get_tmstamp(self):
    return (self.phonemes[0].begin, slef.phonemes[-1].end)

  def get_begin(self):
    return self.phonemes[0].begin

  def get_end(self):
    return self.phonemes[-1].end

  def get_duration(self):
    return round((self.phonemes[-1].end - self.phonemes[0].begin), 3)

  def __str__(self):
    return self.mora
    # return '{0}, {1}'.format(self.mora, [ str(p) for p in self.phonemes])
