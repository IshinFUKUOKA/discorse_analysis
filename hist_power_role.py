# -*-coding: utf-8-*-
"""要点段落内の役割ごとにパワーの統計を取る
"""
import matplotlib.pyplot as plt

def load_utterance_role():
  utterance_roles = {}
  with open('{0}/list/role.list'.format(data_dir)) as fp:
    for line in fp:
      utt, role = line.rstrip().split(' ')
      utterance_roles[utt] = role
  return utterance_roles

if __name__ == '__main__':
  utterance_roles = load_utterance_role()
  pass
