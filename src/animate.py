import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
plt.style.use('ggplot')
import matplotlib.animation as animation
import time
import pandas as pd
import numpy as np

def plot():
    fig = plt.figure()
    ax1 = fig.add_subplot(1,1,1)

    def animate(i):
        pullData = open("sampleText.txt","r").read()
        dataArray = pullData.split('\n')
        xar = []
        yar = []
        for eachLine in dataArray:
            if len(eachLine)>1:
                x,y = eachLine.split(',')
                xar.append(int(x))
                yar.append(int(y))
        ax1.clear()
        ax1.plot(xar,yar)


    def animate(i):
        dataframe = pd.read_csv('test.csv', engine='c')
        dataframe.Time = dataframe.Time.apply(lambda x: pd.to_datetime(x))
        dataframe = dataframe.set_index('Time')
        # print( dataframe )
        dataframe = dataframe.sort_index()
        predict = dataframe['Predicted']
        actual = dataframe['Actual']

        window = 5

        ma = actual.rolling(window).mean()
        mstd = actual.rolling(window).std()

        dataframe['signal'] = np.sign(abs(actual-ma)-2*mstd)
        markers = dataframe[ dataframe.signal > 0 ]['Actual']

        ax1.clear()
        ax1.plot(actual.index, actual, label='Actual Value', color='b')
        ax1.fill_between(mstd.index, ma-mstd, ma+mstd, color='b', alpha=0.2)
        ax1.scatter(markers.index, markers, facecolors='none', edgecolors='r', label='Fault Detected')

        handles, labels = ax1.get_legend_handles_labels()
        color_block = mpatches.Patch(color='b', alpha=0.2)
        display = [0,1]

        ax1.set_title('Fault Detection for Overall Energy Usage')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('kWh')
        ax1.legend( [handle for i,handle in enumerate(handles) if i in display]+[color_block],
                  [label for i,label in enumerate(labels) if i in display]+['Predicted Range'] )
        plt.tight_layout()

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()

plot()