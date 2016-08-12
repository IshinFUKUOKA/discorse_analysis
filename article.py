# -*-coding: utf-8-*-

import glob
import numpy as np
from utterance import Utterance

class Article:
  def __init__(self, article_id, utterances):
    self.article_id = article_id
    self.utterances = { u:Utterance(u) for u in utterances}
  
  # 漢字表記テキストの読み込み
  def load_text(self, text_dir_path):
    self.texts = []
    text_files = glob.glob(text_dir_path + '/{0}*'.format(self.article_id))
    for txt_file in text_files:
      utterance_id = txt_file.split('/')[-1].split('.')[0]
      with open(txt_file) as fp:
        self.utterances[utterance_id].set_text(fp.read().rstrip())

  # ひらがな表記テキストの読み込み
  def load_hira(self, hira_dir_path):
    self.hiras = []
    hira_files = glob.glob(hira_dir_path + '/{0}*'.format(self.article_id))
    for hira_file in hira_files:
      utterance_id = hira_file.split('/')[-1].split('.')[0]
      with open(hira_file) as fp:
        self.utterances[utterance_id].set_hira(fp.read().rstrip())

  # 音素表記テキストの読み込み
  def load_phon(self, phon_dir_path):
    self.phons = []
    phon_files = glob.glob(phon_dir_path + '/{0}*'.format(self.article_id))
    for phon_file in phon_files:
      utterance_id = phon_file.split('/')[-1].split('.')[0]
      with open(phon_file) as fp:
        self.utterances[utterance_id].set_phon(fp.read().rstrip())

  # 音素アライメントデータの読み込み
  def load_algn(self, algn_dir_path):
    self.algns = []
    algn_files = glob.glob(algn_dir_path + '/{0}*'.format(self.article_id))
    for algn_file in algn_files:
      utterance_id = algn_file.split('/')[-1].split('.')[0]
      with open(algn_file) as fp:
        phonemes = fp.read().rstrip().split('\n')
        self.utterances[utterance_id].set_algn(phonemes)

  # f0データの読み込み
  def load_pitch(self, f0_dir_path, unit):
    self.f0_analysis_unit = unit
    self.pitches = []
    pitch_files = glob.glob(f0_dir_path + '/{0}*.f0'.format(self.article_id))
    pitch_files.sort()
    for pitch_file in pitch_files:
      utterance_id = pitch_file.split('/')[-1].split('.')[0]
      pitch_data = np.loadtxt(pitch_file)
      self.utterances[utterance_id].set_pitch(pitch_data)

  # 境界情報の分析
  def analyze_boundaries(self):
    sorted_uid = sorted(self.utterances.keys())
    for uid in sorted_uid:
      utterance = self.utterances[uid]
      utterance.breath_group_boundary(3)

  # 全体情報の分析
  def analyze_whole(self):
    sorted_uid = sorted(self.utterances.keys())
    for uid in sorted_uid:
      utterance = self.utterances[uid]
      utterance.breath_group_whole()
