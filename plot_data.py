import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import ttest_ind

def table_maker(df):
    fig, ax = plt.subplots()

    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')


    ax.table(cellText=df.values, colLabels=df.columns, loc='center')

    fig.tight_layout()

    return fig

def do_ttest(df,z, cluster_1, cluster_2):
    labels = z.predict(df)
    list_features=df.columns.to_list()
    df['cluster'] = labels
    same_list=[]
    different_list=[]
    for feature in list_features:
        cls1 = df[df['cluster']==cluster_1][feature]
        cls2 = df[df['cluster']==cluster_2][feature]
        ttest, pval = ttest_ind(cls1,cls2)
        if pval <0.05:
            different_list.append(feature)
        else:
            same_list.append(feature)
    return different_list,same_list
