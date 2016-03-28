# rgb.py

# This script should help me build the red, green,blue visualizations.

import numpy  as np
import pandas as pd
import datetime
import matplotlib
import pdb

# I should check cmd line arg
import sys
if (len(sys.argv) < 3):
  print('Demo:')
  print('cd ~/ddata')
  print('python ~/sklearnem/multiyr/acc_eff 2010 2016')
  print('...')
  sys.exit()

startyr = int(sys.argv[1])
finalyr = int(sys.argv[2])

# I should create a loop which does train and test for each yr.
for yr in range(startyr,1+finalyr):
  predf   = 'predictions'+str(yr)+'.csv'
  pred_df = pd.read_csv(predf)
  # I should get leadp which is the price 1 ahead of cp:
  cp_l    = [p_f for p_f in pred_df['cp']]
  leadp_l = cp_l[1:] + [cp_l[-1]]
  # I should get lead_l which leadp - cp
  lead_l  = list(np.array(leadp_l)-np.array(cp_l))
  pred_df['lead']  = lead_l
  pred_df['rdelta']=pred_df['actual_dir']*pred_df['pdir_nb']*np.sign(pred_df['lead'])*pred_df['lead']
  # I should get initial red_l
  red_l = [cp_l[0]]
  rcount  = 0
  # I should grow red_l
  for rdelta in pred_df['rdelta']:
    rcount += 1
    red_l.append(red_l[rcount-1]+rdelta)
  # I should add red_l to df:
  pred_df['red'] = red_l[:-1]
  # matplotlib likes dates:
  cdate_l = [datetime.datetime.strptime(row, "%Y-%m-%d") for row in pred_df['cdate'].values]

  # I should plot
  matplotlib.use('Agg')
  # Order is important here.
  # Do not move the next import:
  import matplotlib.pyplot as plt
  plt.figure(figsize=(15,10))
  plt.plot(cdate_l, cp_l, 'b-', cdate_l, red_l[:-1], 'r-')

  plt.title('Red,Green,Blue Visualization (Blue: Long Only, Red: Naive-Bayes, Green: Logistic-Regression)')
  plt.grid(True)
  pngf = 'plot'+str(yr)+'.png'
  plt.savefig(pngf)
  plt.close()
  print('New png file: ')
  print(pngf)
'bye'
