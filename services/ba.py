"""
背景评估
"""
import os
import pandas as pd

from .background_map import background_map

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


def get_replay_rate(data, chr_id):
    length = 0
    if data[0] == 1 and data[1] == 1:
        length += cenPosition[chr_id-1]
    elif data[0] == 1 and data[1] == 0:
        length += cenPosition[chr_id-1] / 2
    elif data[0] == 0 and data[1] == 1:
        length += cenPosition[chr_id-1] / 2

    if data[1] == 1 and data[2] == 1:
        length += chr_length[chr_id-1] - cenPosition[chr_id-1]
    elif data[1] == 0 and data[2] == 1:
        length += (chr_length[chr_id-1] - cenPosition[chr_id-1]) / 2
    elif data[1] == 1 and data[2] == 0:
        length += (chr_length[chr_id-1] - cenPosition[chr_id-1]) / 2

    return round(length / chr_length[chr_id-1], 5)


def background_assessment(ped_fp, map_fp):
    ped_df = pd.read_csv(ped_fp, sep="\t", header=None)
    map_df = pd.read_csv(map_fp, sep="\t", header=None)

    # ped 文件的第一行为亲本，群体都跟他比较
    ped_df.columns = ["Family ID", "Individual ID", "Paternal ID", "Maternal ID", "Sex", "Phenotype"] + map_df[1].tolist()

    result_data = []
    result_rate_data = []

    headers = []
    for chr_id in range(1, 11):
        for region in ["CTLR", "CCR", "CTRR"]:
            headers.append(f"Chr{chr_id}-{region}")
    
    for index, row in ped_df.iterrows():
        if index == 0:
            continue
        else:
            row_data = []
            row_rate_data = []
            for chr_id in range(1, 11):
                chr_data = []
                for region in ["CTLR", "CCR", "CTRR"]:
                    markers = map_df[(map_df[0] == chr_id) & (map_df[4]==region)][1].tolist()
                    if len(markers) > 0:
                        if row[markers[0]] == ped_df.iloc[0][markers[0]]:
                            chr_data.append(1)
                        else:
                            chr_data.append(0)
                    else:
                        chr_data.append(0)

                row_data += chr_data
                chr_replay_rate = get_replay_rate(chr_data, chr_id)
                row_rate_data.append(chr_replay_rate)

            result_data.append([row["Individual ID"]] + row_data )
            result_rate_data.append([row["Individual ID"]] + row_rate_data )

    result_df = pd.DataFrame(result_data, columns = ["ID"] + headers)
    result_rate_df = pd.DataFrame(result_rate_data, columns = ["ID"] + [f"Chr{i}" for i in range(1, 11)])

    result_df.to_csv(
        os.path.join(os.getcwd(), "output/background_assessment.txt"),
        index=False,
        sep="\t"
    )

    result_rate_df.to_csv(
        os.path.join(os.getcwd(), "output/background_assessment_rate.txt"),
        index=False,
        sep="\t"
    )
    
    # 简化标记背景图
    background_map(result_df)

    return result_rate_df
