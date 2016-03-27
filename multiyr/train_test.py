# train_test.py

# This script should use train and test CSV data in ~/ddata/
# to train and test.

# The results should get written to CSV files in ~/ddata/
import numpy  as np
import pandas as pd
import pdb

# I should check cmd line arg
import sys
if (len(sys.argv) < 3):
  print('Demo:')
  print('cd ~/ddata')
  print('python ~/sklearnem/multiyr/train_test.py 2010 2016')
  print('...')
  sys.exit()

startyr = int(sys.argv[1])
finalyr = int(sys.argv[2])

# I should create a loop which does train and test for each yr.
for yr in range(startyr,1+finalyr):
  trainf = 'train'+str(yr)+'.csv'
  train_df = pd.read_csv(trainf)
  train_a  = np.array(train_df)
  # I should declare some integers to help me navigate the Arrays.
  cdate_i   = 0
  cp_i      = 1
  pctlead_i = 2
  pctlag1_i = 3
  pctlag2_i = 4
  pctlag4_i = 5
  pctlag8_i = 6
  end_i     = 7
  x_train_a = train_a[:,pctlag1_i:end_i]
  y_train_a = train_a[:,pctlead_i]
  train_median  = np.median(y_train_a)
  label_train_a = y_train_a > train_median
  # I should learn from x_train_a,label_train_a:
  from sklearn import linear_model
  clf = linear_model.LogisticRegression()
  clf.fit(x_train_a, label_train_a)
  # Now that I have learned, I should predict:
  testf    = 'test'+str(yr)+'.csv'
  test_df  = pd.read_csv(testf)
  test_a   = np.array(test_df)
  x_test_a = test_a[:,pctlag1_i:end_i]
  y_test_a = test_a[:,pctlead_i]
  label_test_a  = y_test_a > train_median
  predictions_l = []
  xcount        = -1
  x_eff_l       = [0.0]
  recent_eff_l  = [0.0]
  acc_l         = []
  for xoos_a in x_test_a:
    xcount     += 1 # should == 0 1st time through
    xf_a        = xoos_a.astype(float)
    xr_a        = xf_a.reshape(1, -1)
    aprediction = clf.predict_proba(xr_a)[0,1]
    if (aprediction > 0.5):
      predictions_l.append(1)  # up   prediction
    else:
      predictions_l.append(-1) # down prediction
    # Note effectiveness of this prediction:
    pctlead = y_test_a[xcount]
    x_eff_l.append(predictions_l[xcount]*pctlead)
    # Note recent effectiveness of this prediction:
    if (xcount < 5):
      recent_eff_l.append(0.0)
    else:
      recent_eff_l.append(np.mean(x_eff_l[-5:]))
    # Note accuracy of this prediction
    if ((y_test_a[xcount] > 0) and (aprediction > 0.5)):
      acc_l.append('tp')
    if ((y_test_a[xcount] > 0) and (aprediction < 0.5)):
      acc_l.append('fn')
    if ((y_test_a[xcount] < 0) and (aprediction > 0.5)):
      acc_l.append('fp')
    if ((y_test_a[xcount] < 0) and (aprediction < 0.5)):
      acc_l.append('tn')
    

  # I should save predictions_l so I can report later.
  test_df['actual_dir'] = np.sign(test_df['pctlead'])
  test_df['pdir']       = predictions_l
  test_df['x_eff']      = x_eff_l[1:]
  test_df['recent_eff'] = recent_eff_l[1:]
  test_df['accuracy']   = acc_l
  pdb.set_trace()
  test_df.head()
  test_df.tail()

'bye'

