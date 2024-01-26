"""
Simplified Marker Design
"""
import os
import random
import pandas as pd
import fitz
from .chromosome import draw_chromosome

regions = {
    "chr1": {
        "CTLR": [0, 33219878],
        "CCR": [85346682, 191122494],
        "CTRR": [267016781, 301476924],
    },
    "chr2": {
        "CTLR": [0, 19240297],
        "CCR": [52070996, 169617226],
        "CTRR": [209941624, 237917468],
    },
    "chr3": {
        "CCR": [58713211, 156855978],
        "CTLR": [0, 35745722],
        "CTRR": [199364097, 232245527]
    },
    "chr4": {
        "CCR": [57973158, 155831675],
        "CTLR": [0, 17435166],
        "CTRR": [210151293, 242062272]
    },
    "chr5": {
        "CCR": [74684221, 145254799],
        "CTLR": [0, 28106888],
        "CTRR": [196072773, 217959525]
    },
    "chr6": {
        "CCR": [31005493,82927670],
        "CTLR": [0, 21886231],
        "CTRR": [142027682, 169407836]
    },
    "chr7": {
        "CCR": [33021003, 108282097],
        "CTLR": [0, 15468060],
        "CTRR": [159447195, 176826311]
    },
    "chr8": {
        "CCR": [27638759,105760682],
        "CTLR": [0, 21638759],
        "CTRR": [156637954, 175377492]
    },
    "chr9": {
        "CCR": [30856396, 104358235],
        "CTLR": [0, 20879206],
        "CTRR": [131922655, 157038028]
    },
    "chr10": {
        "CCR": [30861790,93698582],
        "CTLR": [0, 19859054],
        "CTRR": [116696221, 149632204]
    }
}


def gt_compare(s1, s2) -> bool:
    """
    True: 纯合差异
    """
    if "0" not in s1 and "0" not in s2:
        s1_list = s1.split(" ")
        r = True
        for v in s1_list:
            if v in s2:
                r = False
                break
        return r
    else:
        return False


def find_polymorphism_markers(df) -> list:
    target_markers = []
    markers = df.columns.tolist()[1:]
    for marker in markers:
        marker_gt = df[marker].tolist()[:2]
        if gt_compare(marker_gt[0], marker_gt[1]):
            target_markers.append(marker)
    return target_markers



def simplified_marker_design(ped_fp, map_fp, marker_num):
    """
    ped_fp: 基因型数据（ped格式）
    map_fp: 标记信息数据 （map格式）
    marker_num: 单染色体使用的标记个数
    """
    ped_df = pd.read_csv(ped_fp, sep="\t", header=None)
    map_df = pd.read_csv(map_fp, sep="\t", header=None)

    ped_df.columns = ["Family ID", "Individual ID", "Paternal ID", "Maternal ID", "Sex", "Phenotype"] + map_df[1].tolist()

    map_group = map_df.groupby(0)

    selected_map_df = pd.DataFrame()

    for chr_id, chr_map_df in map_group:
        chr_ccr_markers = []
        chr_ctlr_markers = []
        chr_ctrr_markers = []
        for index, row in chr_map_df.iterrows():
            if int(row[3]) >= regions[f"chr{chr_id}"]["CCR"][0] and int(row[3]) <= regions[f"chr{chr_id}"]["CCR"][1]:
                chr_ccr_markers.append(row[1])
            elif int(row[3]) >= regions[f"chr{chr_id}"]["CTLR"][0] and int(row[3]) <= regions[f"chr{chr_id}"]["CTLR"][1]:
                chr_ctlr_markers.append(row[1])
            elif int(row[3]) >= regions[f"chr{chr_id}"]["CTRR"][0] and int(row[3]) <= regions[f"chr{chr_id}"]["CTRR"][1]:
                chr_ctrr_markers.append(row[1])

        chr_ccr_df = ped_df[["Individual ID"]+chr_ccr_markers]
        chr_ctlr_df = ped_df[["Individual ID"]+chr_ctlr_markers]
        chr_ctrr_df = ped_df[["Individual ID"]+chr_ctrr_markers]

        chr_ccr_markers = find_polymorphism_markers(chr_ccr_df)
        chr_ctlr_markers = find_polymorphism_markers(chr_ctlr_df)
        chr_ctrr_markers = find_polymorphism_markers(chr_ctrr_df)

        if len(chr_ccr_markers) >= marker_num:
            selected_markers = random.sample(chr_ccr_markers, marker_num)
            chr_ccr_selected_df = map_df[map_df[1].isin(selected_markers)].copy()
        else:
            chr_ccr_selected_df = map_df[map_df[1].isin(chr_ccr_markers)].copy()
        
        chr_ccr_selected_df[4] = "CCR"
        selected_map_df = pd.concat([selected_map_df, chr_ccr_selected_df])

        if len(chr_ctlr_markers) >= marker_num:
            selected_markers = random.sample(chr_ctlr_markers, marker_num)
            chr_ctlr_selected_df = map_df[map_df[1].isin(selected_markers)].copy()
        else:
            chr_ctlr_selected_df = map_df[map_df[1].isin(chr_ctlr_markers)].copy()
        
        chr_ctlr_selected_df[4] = "CTLR"
        selected_map_df = pd.concat([selected_map_df, chr_ctlr_selected_df])

        if len(chr_ctrr_markers) >= marker_num:
            selected_markers = random.sample(chr_ctrr_markers, marker_num)
            chr_ctrr_selected_df = map_df[map_df[1].isin(selected_markers)].copy()
        else:
            chr_ctrr_selected_df = map_df[map_df[1].isin(chr_ctrr_markers)].copy()
        
        chr_ctrr_selected_df[4] = "CTRR"
        selected_map_df = pd.concat([selected_map_df, chr_ctrr_selected_df])

    selected_map_df.to_csv(
        os.path.join(os.getcwd(), "output/selected_markers.map"),
        index=False,
        sep="\t", 
        header=None
    )

    # 绘制染色体图
    draw_chromosome(
        selected_map_df, 
        os.path.join(os.getcwd(), "output/selected_markers.pdf")
    )
    # pdf 转图片
    pdfDoc = fitz.open(os.path.join(os.getcwd(), "output/selected_markers.pdf"))
    page = pdfDoc.load_page(0)
    mat = fitz.Matrix(6, 6)
    pix = page.get_pixmap(matrix=mat, dpi=None, colorspace='rgb', alpha=False)
    # 保存图片
    pix.save(os.path.join(os.getcwd(), "output/selected_markers.png"))
