# -*-coding: utf-8-*-
"""要点段落内の役割ごとに統計を取る
要点段落内ごとのデータを書きだしたcsvファイルを読み込み
各フィールドの値の分布をヒストグラムで表示
"""
import discourse_analysis as da
import itertools as ite
import matplotlib.pyplot as plt

csv_file = '/home/fukuoka/dialogue/M2/8August/recording_data/F0Data.csv'
data_dir = '/home/fukuoka/data/GCS_recording201608'
output_dir = './role_fig'

def load_utterance_role():
  utterance_roles = {}
  with open('{0}/list/role.list'.format(data_dir)) as fp:
    for line in fp:
      utt, role = line.rstrip().split(' ')
      utterance_roles[utt] = role
  return utterance_roles

def role_color(role):
    colors = ['g', 'r', 'b']
    return colors[int(role)]

if __name__ == '__main__':
  utterance_roles = load_utterance_role()
  f0data = da.load_csv_data(csv_file)
  header = da.load_csv_header(csv_file)

  # headerの値(first_average等)ごとにヒストグラムをプロット
  for idx, h in enumerate(header[1:], start=0):
    # 二組ずつ比較
    roles = ''.join([r for r in set(utterance_roles.values())])
    for pair in ite.combinations(roles, 2):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        for role in pair:
            role_data = [f0data[key][idx] for key, value in utterance_roles.items() if value == role]
            role_data = [ data for data in role_data if data > 0] # 取れていない値を削除
            ax.hist(role_data, bins=50, normed=True, color=role_color(role), alpha=0.5, label=str(role))
        ax.set_xlabel('value')
        ax.set_ylabel('freq')
        ax.legend()
        plt.title(h)
        plt.savefig('{0}/{1}_{2}and{3}.png'.format(output_dir, h, pair[0], pair[1]))
        plt.clf()
