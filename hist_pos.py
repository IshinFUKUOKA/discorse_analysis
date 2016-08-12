# -*-coding: utf-8-*-
"""要点段落内の発話説の位置ごとに統計を取る
要点段落内ごとのデータを書きだしたcsvファイルを読み込み
各フィールドの値の分布をヒストグラムで表示
"""
import discourse_analysis as da
import itertools as ite
import matplotlib.pyplot as plt

csv_file = '/home/fukuoka/dialogue/M2/8August/recording_data/F0Data.csv'
data_dir = '/home/fukuoka/data/GCS_recording201608'
output_dir = './pos_fig'

def position_color(position):
    colors = ['g', 'r', 'b', 'y', 'c']
    return colors[int(position)]

if __name__ == '__main__':
  f0data = da.load_csv_data(csv_file)
  header = da.load_csv_header(csv_file)

  with open('/home/fukuoka/data/GCS_recording201608/list/utterance.list') as fp:
    utterances = [line.rstrip() for line in fp]
    utt_positions = { utt: utt.split('_')[-1] for utt in utterances }

  # headerの値(first_average等)ごとにヒストグラムをプロット
  for idx, h in enumerate(header[1:], start=0):
    # 二組ずつ比較
    positions = [r for r in set(utt_positions.values())]
    for pair in ite.combinations(positions, 2):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        for position in pair:
            position_data = [f0data[key][idx] for key, value in utt_positions.items() if value == position]
            position_data = [ data for data in position_data if data > 0] # 取れていない値を削除
            ax.hist(position_data, bins=50, color=position_color(position), alpha=0.5, label=str(position))
        ax.set_xlabel('value')
        ax.set_ylabel('freq')
        ax.legend()
        plt.title(h)
        plt.savefig('{0}/{1}_{2}and{3}.png'.format(output_dir, h, pair[0], pair[1]))
        plt.clf()
