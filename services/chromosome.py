import pandas as pd
from reportlab.lib.units import cm
from Bio.Graphics import BasicChromosome
from reportlab.graphics.shapes import Line

class CentromereSegment(BasicChromosome.ChromosomeSegment):


    def __init__(self, inverted=0):

          BasicChromosome.ChromosomeSegment.__init__(self)
    
          self._inverted = inverted 


    def _draw_segment(self, cur_drawing):

        # set the coordinates of the segment -- it'll take up the MIDDLE part
          
        width = (self.end_x_position - self.start_x_position) * self.chr_percent
        height = self.start_y_position - self.end_y_position
        
        
                
        # 画缺口
        segment_width = (self.end_x_position - self.start_x_position) \
              * self.chr_percent 
        segment_height = self.start_y_position - self.end_y_position 
        segment_x = self.start_x_position \
              + 0.5 * (self.end_x_position - self.start_x_position - segment_width) 

        segment_y = self.end_y_position
        right_line1 = Line(segment_x, segment_y, 
                          segment_x+5, segment_y + segment_height/2) 
        right_line2 = Line(segment_x+5, segment_y+ segment_height/2, 
                          segment_x, segment_y + segment_height)
        
        left_line1 = Line(segment_x + segment_width, segment_y, 
                         segment_x + segment_width - 5, segment_y + segment_height/2) 
        left_line2 = Line(segment_x + segment_width - 5 , segment_y + segment_height/2, 
                         segment_x + segment_width, segment_y + segment_height) 

        cur_drawing.add(right_line1) 
        cur_drawing.add(right_line2) 
        cur_drawing.add(left_line1)         
        cur_drawing.add(left_line2)


# 着丝粒区
cenPosition = [
    [134400000, 135000000],
    [92900000, 94700000],
    [99700000, 100700000],
    [105300000, 106100000],
    [102300000, 109200000],
    [49600000, 50000000],
    [54600000, 62500000],
    [49000000, 51400000],
    [72200000, 72700000],
    [50100000, 52400000],
]


def getFeatures(chr_df, chr_id):
    '''
    获取标记数据
    '''
    result = [[], [], []]
    position = cenPosition[chr_id-1]
    result[1] = (position)

    for index, row in chr_df.iterrows():
        lr = 0
        if (int(row[3]) < position[0]):
            result[0].append((int(row[3]), int(row[3])+1, lr, row[1],  "Red"))

        if (int(row[3]) > position[1]):
            result[2].append((int(row[3])- position[1], int(row[3])- position[1] +1, lr, row[1], "Red"))

    return result



def draw_chromosome(df, OUTPUT_PATH):
    entries = [
        ('Chr01', 301476925),
        ('Chr02', 237917469),
        ('Chr03', 232245528),
        ('Chr04', 242062273),
        ('Chr05', 217959526),
        ('Chr06', 169407837),
        ('Chr07', 176826312),
        ('Chr08', 175377493),
        ('Chr09', 157038029),
        ('Chr10', 149632205),
    ]

    max_len = 301476924
    telomere_length = 9000000

    chr_diagram = BasicChromosome.Organism()
    chr_diagram.page_size = (25*cm, 20*cm)


    for name, length in entries:
        chr_id = int(name[3:])
        
        cur_chromosome = BasicChromosome.Chromosome(name, )
        cur_chromosome.title_size = 8
        cur_chromosome.scale_num = max_len + 2 * telomere_length

        # 绘制上弧
        start = BasicChromosome.TelomereSegment()
        start.scale = telomere_length
        cur_chromosome.add(start)

        features = getFeatures(
            df[df[0].isin([chr_id, str(chr_id)])],
            chr_id
        )

        # 绘制染色体上臂+标记
        # 第一个参数：表示标记的宽度的开始位置   
        # 第二个参数：表示标记的宽度的结束位置
        # 第三个参数：‘-1’表示标记在左边 ‘+1’表示标记在右边 ‘0’表示全标记 

        body1 = BasicChromosome.AnnotatedChromosomeSegment(features[1][0],features[0])
        body1.scale = features[1][0]
        cur_chromosome.add(body1)


        # 绘制着丝粒
        centromere = CentromereSegment()
        
        # centromere.scale = features[1][1] - features[1][0]
        centromere.scale = 2500000

        cur_chromosome.add(centromere)

        # 绘制染色体下臂+标记

        body2 = BasicChromosome.AnnotatedChromosomeSegment(length - features[1][1], features[2])

        body2.scale = length - features[1][1]
        cur_chromosome.add(body2)

        # 绘制染色体下弧
        end = BasicChromosome.TelomereSegment(inverted=True)
        end.scale = telomere_length
        cur_chromosome.add(end)

        # This chromosome is done
        chr_diagram.add(cur_chromosome)
        
    chr_diagram.draw(OUTPUT_PATH, "Selected Markers")

    