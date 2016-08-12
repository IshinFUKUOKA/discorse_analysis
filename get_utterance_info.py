# -*-coding: utf-8-*-
"""発話節ごとのF0に関する特徴を抽出するプログラム
 Author:               Ishin Fukuoka  Waseda University
"""
import ConfigParser
from article import Article
import discourse_analysis as da

def print_header():
  print 'utterance_id',
  for tname in ['first', 'last', 'whole']:
    for pname in ['average', 'variance', 'dynamic_range', 'max_value']:
      print '{0}-{1}'.format(tname, pname),
  print ''

if __name__ == '__main__':
    inifile = ConfigParser.SafeConfigParser()
    inifile.read('./config.ini')

    dlg_list_file = inifile.get('data', 'dlg_list')
    with open(dlg_list_file) as fp:
        dlg_list = sorted([line.rstrip() for line in fp])

    utt_list_file = inifile.get('data', 'utt_list')
    with open(utt_list_file) as fp:
        utt_list = [line.rstrip() for line in fp]

    root_path = inifile.get('data', 'root')
    text_dir_path = root_path + inifile.get('data', 'text')
    hira_dir_path = root_path + inifile.get('data', 'hira')
    phon_dir_path = root_path + inifile.get('data', 'phon')
    algn_dir_path = root_path + inifile.get('data', 'algn')
    f0_dir_path = root_path + inifile.get('data', 'f0')

    f0_analysis_unit = inifile.get('analysis', 'f0_width')

    print_header()

    for dlg in dlg_list:
        utts = [utt for utt in utt_list if dlg in utt]
        article = Article(dlg, utts)
        article.load_text(text_dir_path)
        article.load_hira(hira_dir_path)
        article.load_phon(phon_dir_path)
        article.load_algn(algn_dir_path)
        article.load_pitch(f0_dir_path, f0_analysis_unit)
        for utterance in sorted(article.utterances.values()):
          time_get_funcs = [utterance.get_first_mora_time, utterance.get_last_mora_time, utterance.get_whole_time]
          property_get_funcs = [da.average, da.variance, da.dynamic_range, da.max_value]
          print utterance.utterance_id,
          for tfunc in time_get_funcs:
            for pfunc in property_get_funcs:
              print da.get_f0_property(utterance, tfunc, pfunc),
          print ''
