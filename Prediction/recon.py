import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

hrir_est = pd.read_csv('hrir_sub_9.csv')
delay_est = pd.read_csv('sub_9_delay.csv')

hrir_left = hrir_est.loc[0:1249]
hrir_right = hrir_est.loc[1250:2499]

hrir_right['azi'] = hrir_right['azi'].apply(lambda x: -1*x)

hrir_right = hrir_right.drop(['azi', 'ele'], axis=1)
hrir_left = hrir_left.drop(['azi', 'ele'], axis=1)

hrir_right = hrir_right.reset_index(drop=True)
hrir_left = hrir_left.reset_index(drop=True)



for i in range(0, 1250, 100):
    fg = plt.plot(hrir_left.iloc[i, 0:199])
    fg = plt.plot(hrir_right.iloc[i, 0:199])
    plt.show(fg)
    plt.clf()


for i in range(0, 1250, 1):
    print(i)
    hrir_right.loc[i] = np.roll(hrir_right.iloc[i], 20)
    hrir_left.loc[i] = np.roll(hrir_left.iloc[i], 20)


for i in range(0, 1250, 1):
    print(i)
    delay = int(np.round(delay_est['est_itd'][i], 0))
    if delay >= 0:
        hrir_right.loc[i] = np.roll(hrir_right.iloc[i], delay)
    else:
        hrir_left.loc[i] = np.roll(hrir_left.iloc[i], -delay)


for i in range(0, 1250, 100):
    fg = plt.plot(hrir_left.iloc[i, 0:199])
    fg = plt.plot(hrir_right.iloc[i, 0:199])
    plt.show(fg)
    plt.clf()


hrir_left.to_csv('sub9_est_left.csv', index=None, header=None)
hrir_right.to_csv('sub9_est_right.csv', index=None, header=None)



#############################
hrir_left= pd.read_csv('sub2_est_left.csv', header=None)
hrir_left_r = pd.read_csv('sub4_est_left.csv', header=None)
for i in range(0, 1250, 100):
    fg = plt.plot(hrir_left.iloc[i, 0:199])
    fg = plt.plot(hrir_left_r.iloc[i, 0:199])
    plt.show(fg)
    plt.clf()



plt.figure()
plt.xticks(np.arange(0, 220, step=10))
#plt.title('Complete HRIR for subject 3 at -45 azi, 45 ele', fontsize=18)
#plt.xlabel('Sample', fontsize=14)
#hrir_right.loc[166] = np.roll(hrir_right_r.iloc[166], 1)
#hrir_left_r.loc[166] = np.roll(hrir_left_r.iloc[166], 9)
plt.plot(hrir_left.loc[166], label='Est. Left HRIR', lw=2)
plt.plot(hrir_right.loc[166], label='Est. Right HRIR', lw=2)
plt.plot(hrir_left_r.loc[166], label='Actual Left HRIR', lw=2)
plt.plot(hrir_right_r.loc[166], label='Actual Right HRIR', lw=2)
plt.plot([0,0],[-4,4],lw=2, color='black')
plt.plot([0,210],[0,0],lw=2, color='black')
legend = plt.legend(loc='upper right', shadow=True, prop={'size': 16})
plt.grid(True, which='Major')
plt.grid(True, which='Minor')
plt.ylim((-1.4, 1))
plt.xlim((0,200))
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.axis()
plt.show()
