import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
timestamp = np.load("timestamp.npy")
y = np.load("lables.npy")
with open("vocab.json", "r") as fin:
    vocab = json.load(fin)
fig = plt.figure()
font = {'family':'sans-serif',
        'weight' : 'bold',
        'size'   : 18}
matplotlib.rc('font', **font)
classes = vocab['city']
for index, c in enumerate(classes):
    tz = timestamp[y==index]
    tx = np.linspace(np.min(tz), np.max(tz), 200)
    fit_ty = stats.norm.pdf(tx, np.mean(tz), np.std(tz))
    plt.plot(tx, fit_ty, lw=3, color=np.random.rand(3), label='(City=%s, mean=%.2f, std=%.2f)' % (c, np.mean(tz), np.std(tz)))

tz = timestamp
tx = np.linspace(np.min(tz), np.max(tz), 200)
fit_ty = stats.norm.pdf(tx, np.mean(tz), np.std(tz))
plt.plot(tx, fit_ty, lw=4, color='k', linestyle='--', label='(Mean, mean=%.2f, std=%.2f)' % (np.mean(tz), np.std(tz)))
plt.xlabel('Time(Minutes pass 0:0 UTC)')
plt.ylabel('Frequency(Normed)')
plt.title('Tweets\' time distribution')
plt.legend(loc="lower right")
plt.show()
plt.show()