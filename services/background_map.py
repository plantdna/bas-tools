"""
绘制背景图谱
"""
import os
import numpy as np
import matplotlib.pyplot as plt

chr_length = [
    247.5756395,
    180.8876703,
    164.3111897,
    164.6151669,
    147.8024434,
    95.50410522,
    141.9072593,
    125.9549803,
    127.2027897,
    99.95405161,
]

cenPosition = [
    104.869669,
    84.33541827,
    53.57084721,
    63.67119774,
    67.96612259,
    17.85268,
    40.04706669,
    36.5435281,
    41.47136257,
    26.24598153,
]

color_map = {
    0: np.array([255, 255, 255]), # write
    1: np.array([4, 128, 1]), # green
    3: np.array([255, 1, 0]),  # red
    2: np.array([0, 0, 0]),  # black
}

def get_plot_data(row_data):
    max_len = 0

    plot_data = []
    for chr_id in range(1, 11):
        chr_data = []
        chr_len = int(chr_length[chr_id-1])
        chr_cen = int(cenPosition[chr_id-1])

        l1_len = int(chr_cen / 2)
        l2_len = int(chr_cen / 2)
        l3_len = 2
        l4_len = int((chr_len - chr_cen) / 2)
        l5_len = int((chr_len - chr_cen) / 2)

        if row_data[f"Chr{chr_id}-CTLR"] == 1:
            chr_data+=[1]*l1_len
        else:
            chr_data+=[3]*l1_len

        if row_data[f"Chr{chr_id}-CCR"] == 1:
            chr_data+=[1]*l2_len
            chr_data+=[2]*l3_len
            chr_data+=[1]*l4_len

        else:
            chr_data+=[3]*l2_len
            chr_data+=[2]*l3_len
            chr_data+=[3]*l4_len

        if row_data[f"Chr{chr_id}-CTRR"] == 1:
            chr_data+=[1]*l5_len
        else:
            chr_data+=[3]*l5_len

        if len(chr_data) > max_len:
            max_len = len(chr_data)

        plot_data.append(chr_data)

    for i in range(10):
        if len(plot_data[i]) < max_len:
            plot_data[i] = plot_data[i] + [0]*(max_len-len(plot_data[i]))

    return plot_data

def background_map(df):

    if not os.path.exists(os.path.join(os.getcwd(), "output/sample_image")):
        os.makedirs(os.path.join(os.getcwd(), "output/sample_image"))

    for inded, row in df.iterrows():
        plot_data = get_plot_data(row)
        fig, ax = plt.subplots(figsize=(20, 20))
        heatmap_data = np.array(plot_data)

        data_3d = np.ndarray(shape=(heatmap_data.shape[0], heatmap_data.shape[1], 3), dtype=int)

        for i in range(0, heatmap_data.shape[0]):
            for j in range(0, heatmap_data.shape[1]):
                data_3d[i][j] = color_map[heatmap_data[i][j]]

        ax.imshow(data_3d, interpolation=None)
        ax.set_aspect('auto')

        ax.set_xticks([])
        ax.set_yticks(np.arange(heatmap_data.shape[0]))

        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)


        ax.set_yticklabels(['Chr{}'.format(i) for i in range(1, 11)], fontsize=36)
        ax.set_yticks(np.arange(heatmap_data.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=20)
        ax.tick_params(which="minor", bottom=False, left=False)
        ax.set_title("", fontsize=36)

        plt.savefig(
            os.path.join(os.getcwd(), f"output/sample_image/{row['ID']}.png"), 
            format='png', 
            dpi=300
        )
        plt.close()
