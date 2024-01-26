"""
生成筛选简化标记的入口文件
"""
import pandas as pd

dp_name = "C19_FYMP017_P56B10_CX101"
rp_name = "C21_FYMP017_P56B11_CX102"


dp_df = pd.read_csv(f"/Users/zyl/Workspace/dataset/Inbreds/5822/samples/{dp_name}.txt", sep="\t")
rp_df = pd.read_csv(f"/Users/zyl/Workspace/dataset/Inbreds/5822/samples/{rp_name}.txt", sep="\t")

gt_df = pd.merge(dp_df, rp_df, on="locus")
individuals = gt_df.columns.tolist()[1:]

probeset_df = pd.read_csv("/Users/zyl/Workspace/dataset/Probeset/230710/NUCLEAR_SNP_PROBESET.csv")
snp_ids = probeset_df["probeset_id"].tolist()
probeset_df.set_index("probeset_id", inplace=True)

gt_df = gt_df[gt_df["locus"].isin(snp_ids)]

ped_data = []

for index, value in enumerate(individuals):
    row_data = [index+1, index+1, 0, 0, 0, 0]
    item_gts = gt_df[value].tolist()
    for gt in item_gts:
        if gt == "---":
            row_data.append("0 0")
        else:
            row_data.append(" ".join(gt.split("/")))
    ped_data.append(row_data)

map_data = []
for index, row in gt_df.iterrows():
    id_info = probeset_df.loc[row["locus"]]
    map_data.append([id_info["Chr_id"], row["locus"], 0, id_info["Start"]])


ped_df = pd.DataFrame(ped_data)
map_df = pd.DataFrame(map_data)

ped_df.to_csv("./test.ped", index=False, sep="\t", header=None)
map_df.to_csv("./test.map", index=False, sep="\t", header=None)
