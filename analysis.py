# -*- coding: utf-8 -*-
# --------------------------------------------------------------------
#
# 呼気段落ごとの各韻律情報をまとめる
#
# Author:               Ishin Fukuoka  Waseda University
#
#
# ヘッダー情報
# utterance_id,content,f0average_on_first,f0average_on_last,f0range_on_first,f0range_on_last,maxf0_on_first,maxf0_on_last,rate_on_first,rate_on_last,subsequent_pause
#
# --------------------------------------------------------------------
import matplotlib.pyplot as plt
import csv
import numpy as np

if __name__ == '__main__':
  input_file = '/home/fukuoka/dialogue/M2/7July/DiscourseData/First3MoraSTYM.csv'
  colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
  data = []
  with open(input_file) as fp:
    reader = csv.reader(fp, delimiter=' ')
    header = next(reader)
    # print ','.join(header)
    for row in reader:
      data.append(row)

  ndata = np.array(data)[:,2:]
  # 呼気段落ごとのF0average
  average_data = np.array([ (float(f), float(l)) for (f, l) in zip(ndata[:, 0], ndata[:, 1]) if 'None' not in [f, l]])
  fig = plt.figure()
  ax = fig.add_subplot(1, 1, 1)
  ax.hist(average_data[:, 0], bins=50, normed=True, color='red', alpha=0.5, label='first3mora')
  ax.hist(average_data[:, 1], bins=50, normed=True, color='blue', alpha=0.5, label='last3mora')
  ax.set_xlabel('Hz')
  ax.set_ylabel('freq')
  ax.legend()
  plt.savefig('fig/f0average_in_bg.png')

  plt.clf()

  # 呼気段落間でのF0Average
  utterances = {}
  for d in data:
    uid = d[0]
    first_ave = float(d[2]) if d[2] != 'None' else 0
    last_ave = float(d[3]) if d[3] != 'None' else 0
    if uid not in utterances:
      utterances[uid] = [first_ave, last_ave]
    else:
      utterances[uid] += [first_ave, last_ave]

  # 呼気段落数ごとに分布を表示
  average_total = { 1:0, 2:0, 3:0, 4:0, 5:0, 6:0 }
  breath_count = { 1:[], 2:[], 3:[], 4:[], 5:[], 6:[] }
  for uid, utterance in utterances.items():
    bg_len = len(utterance) / 2
    if (bg_len > 6): continue
    breath_count[bg_len].append(uid)

  for bg_count, uids in breath_count.items():
    averages = []
    for i in range(bg_count * 2):
      utts = [ value for key, value in utterances.items() if key in uids ]
      pitches = [u[i] for u in utts]
      averages.append(np.average([p for p in pitches if p > 0]))

    plt.plot(range(len(averages)), averages, colors[bg_count-1] +'o-', label=bg_count)

    plt.xlim(-0.5, 13.5)
    plt.ylim(50, 220)
    plt.xlabel('breath position')
    plt.ylabel('Hz')
    plt.legend()
    plt.savefig('fig/f0average_between_bg{0}.png'.format(bg_count))
    plt.clf()

  # 発話内のF0Averageを冒頭と末尾で比較
  utterance_first_pitches = [u[0] for u in utterances.values()]
  utterance_last_pitches = [u[-1] for u in utterances.values()]
  plt.hist(utterance_first_pitches, bins=50, normed=True, color='red', alpha=0.5, label='first3mora')
  plt.hist(utterance_last_pitches, bins=50, normed=True, color='blue', alpha=0.5, label='last3mora')
  plt.xlabel('Hz')
  plt.ylabel('freq')
  plt.legend()
  plt.savefig('fig/f0average_in_utterance.png')
  plt.clf()

  # 発話間でのF0Average
  dialogues = [line.rstrip() for line in open('dialogue.list')]
  utt_counts = { d:len([uid for uid in utterances.keys() if d in uid]) for d in dialogues }
  for utt_count in set(utt_counts.values()):
    pitches = [[] for i in range(utt_count * 2)]
    dids = [did for did, ucount in utt_counts.items() if ucount == utt_count]
    for did in dids:
      for idx, uid in enumerate(sorted([uid for uid in utterances.keys() if did in uid])):
        pitch = utterances[uid]
        if pitch[0] > 0:
          pitches[idx*2].append(pitch[0])

        if pitch[-1] > 0:
          pitches[idx*2+1].append(pitch[-1])

    pitches_average = [ sum(p) / len(p) for p in pitches ]
    plt.plot(range(utt_count * 2), pitches_average, 'o-', label='utterances: {0}'.format(utt_count), color=colors[utt_count -2])
    plt.xlim(-0.5, 15.5)
    plt.ylim(50, 350)
    plt.xlabel('utterance position')
    plt.ylabel('Hz')
    plt.legend()
    plt.savefig('fig/f0average_between_utt{0}.png'.format(utt_count))
    plt.clf()
