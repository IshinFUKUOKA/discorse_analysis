# -*-coding: utf-8-*-
"""談話(要点段落)分析でよく使うメソッド群"""
import csv
import numpy as np


def get_f0_property(utterance, time_get_func, property_get_func):
  """引き数に取った関数で取得できた範囲でF0平均を求める
    time_get_func: utteranceインスタンス中の何かしらの範囲時間を取ってくる関数
  """
  begin, end = time_get_func()
  pitches = utterance.get_pitch(begin, end)
  return property_get_func(pitches)


def average(pitches):
  """ピッチの平均を返す
  受け取ったピッチ配列から0以上の箇所で平均を計算する
  """
  if is_sparse(pitches): return None
  substantial_pitches = [p for p in pitches if p > 0]
  return round(np.average(substantial_pitches), 3)

def variance(pitches):
  """ピッチの分散を返す
  受け取ったピッチ配列から0以上の箇所で分散を計算する
  """
  if is_sparse(pitches): return None
  substantial_pitches = [p for p in pitches if p > 0]
  return round(np.var(substantial_pitches), 3)

def dynamic_range(pitches):
  """ピッチのダイナミックレンジを返す"""
  if is_sparse(pitches): return None
  substantial_pitches = [p for p in pitches if p > 0]
  return round(np.max(substantial_pitches) / np.min(substantial_pitches), 3)

def max_value(pitches):
  """ピッチの最大値を返す"""
  if is_sparse(pitches): return None
  substantial_pitches = [p for p in pitches if p > 0]
  return round(np.max(substantial_pitches), 3)

def is_sparse(pitches):
  return False if len([p for p in pitches if p > 0]) > 5 else True

def load_csv_header(csv_file_path):
  """発話ごとの各種統計値が記載されたcsvのヘッダーを読む"""
  with open(csv_file_path) as fp:
    reader = csv.reader(fp, delimiter=' ')
    header = next(reader)
  return header

def load_csv_data(csv_file_path):
  """発話ごとの各種統計値が記載されたデータを読み込む
  csvの形式: ヘッダあり, 空白(' ')区切り
  1行のデータ: 発話節ID データ1 データ2...
  返り値：発話節IDをkey，データ配列をvalueとするdict
  値がNoneの箇所は-1e-10
  """
  with open(csv_file_path) as fp:
    reader = csv.reader(fp, delimiter=' ')
    header = next(reader)
    data_dic = {}
    for row in reader:
      data = []
      for r in row[1:]:
        if r != 'None':
          data.append(float(r))
        else:
          data.append(-1e-10)
      data_dic[row[0]] = data
  return data_dic
