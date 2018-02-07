import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.style.use('ggplot')
import numpy as np

filename = 'results/results_2015_roof.csv'
filename = 'results/results_2015_overallutilities.csv'
data = pd.read_csv(filename, index_col=False)
data.DATE = data.DATE.apply(lambda x: pd.to_datetime(x) )
data = data.set_index('DATE')
compare_results = data[['Utility Subtotal', 'Scored Labels']].dropna()

plt.close('all')

fig = plt.figure(figsize=(10,4))
ax = fig.add_subplot(1,1,1)
compare_results['Utility Subtotal'].plot(linestyle='-', label='Actual Value')
compare_results['Scored Labels'].plot(linestyle='--', label='Predicted Value')

handles, labels = ax.get_legend_handles_labels()
ax.set_title('Actual vs. Predicted Energy Usage')
ax.set_xlabel('Date')
ax.set_ylabel('kWh')
ax.legend()
plt.savefig('roof_2015_predict.pdf', format='pdf')
plt.show()



# plt.figure()
# predict = compare_results['Scored Labels']
# predict = predict.sort_index()
# ma = predict.rolling(10).mean()
# mstd = predict.rolling(10).std()
# plt.plot(ma.index, ma)
# plt.fill_between(mstd.index, ma-2*mstd, ma+2*mstd, color='b', alpha=0.2)
# plt.show()





fig = plt.figure(figsize=(10,4))
ax = fig.add_subplot(1,1,1)
compare_results = compare_results.sort_index()
predict = compare_results['Scored Labels']
actual = compare_results['Utility Subtotal']
ma = predict.rolling(10).mean()
mstd = predict.rolling(10).std()
compare_results['signal'] = np.sign(abs(actual-ma)-2*mstd)
markers = compare_results[ compare_results.signal > 0 ]['Utility Subtotal']

ax.plot(actual.index, actual, label='Actual Value', color='b')
ax.fill_between(mstd.index, ma-2*mstd, ma+2*mstd, color='b', alpha=0.2)
ax.scatter(markers.index, markers, facecolors='none', edgecolors='r', label='Fault Detected')

handles, labels = ax.get_legend_handles_labels()
color_block = mpatches.Patch(color='b', alpha=0.2)
display = [0,1]

ax.set_title('Fault Detection for Overall Energy Usage')
ax.set_xlabel('Date')
ax.set_ylabel('kWh')
ax.legend( [handle for i,handle in enumerate(handles) if i in display]+[color_block],
          [label for i,label in enumerate(labels) if i in display]+['Predicted Range'] )
plt.tight_layout()
plt.savefig('figures/demo_roof_2015.png', format='png')
plt.savefig('../HVAC-master/engine/saved_images/predicts/demo_overall_2015.png', format='png')
plt.show()

