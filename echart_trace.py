import os.path
import traceback

from typing import List,Tuple
from PIL import Image


class EchartTrace:
    '''
    :returns 通过cavans图获取图表横坐标的间距
    '''
    def __init__(self, png: 'str filename',min_group=2,radius=5,minx_space=20,crops:Tuple=False):
        '''
        :param png:
        :param crops: (left, upper)
        :param min_group: 最小组数，指代该图表中的数据类别数量，尽量不小于2
        :param radius: 数据与坐标轴的交点，圆的半径
        :param minx_space: 最小间距，默认为20
        '''
        self.__ps = 'other.png'
        tmp=Image.open(png)
        # draw=ImageDraw.ImageDraw(tmp)
        # draw.line([(120, 0), (120, 1302)], fill=(0, 255, 255), width=2)
        # draw.line([(0, 70), (2560, 70)], fill=(0, 255, 255), width=2)
        # tmp.show()
        if crops:
            tmp=tmp.crop((*crops,*tmp.size))
        tmp.convert('L').save(self.__ps)
        self._im = Image.open(self.__ps)
        self.min_group, self.radius,self.minx_space=\
            min_group,radius,minx_space

    def __call__(self):
        return self.parse_space(
                                self.get_space(self.min_group,self.radius),
                                self.minx_space
                                )

    def get_space(self, min_group=2, radius=5) -> List:
        width, height = self._im.size
        im = self._im.convert('RGB')
        img_obj = im.load()
        ws = []
        for w in range(width):  # 先x轴在y轴方向遍历每一个点
            cicle = []
            for h in range(height):
                rgb = im.getpixel((w, h))
                if rgb == (255, 255, 255):
                    down_hs = set()
                    up_hs = set()
                    for tmp_h1 in range(h - radius, h):
                        color = img_obj[w, tmp_h1]
                        if color != (255, 255, 255) and color != (0, 0, 0):
                            down_hs.add((w, h, color))
                    for tmp_h2 in range(h, h + radius):
                        color = img_obj[w, tmp_h2]
                        if color != (255, 255, 255) and color != (0, 0, 0):
                            up_hs.add((w, h, color))
                    # print(down_hs,up_hs)
                    if up_hs.intersection(down_hs):
                        cicle.append(w)
            if len(cicle) >= min_group * 2:
                # print(cicle)
                ws.append(cicle[0])
        return ws

    def parse_space(self, ws, minx_space=20):
        '''
        :param ws:
        :param minx_space: 最小间距
        :return:
        '''
        res_ws = []
        for index, x in enumerate(ws[:-1]):  # 清理小于最小间距的点
            if x + minx_space < ws[index + 1]:
                res_ws.append(x)
        res_ws.append(ws[-1])
        d = (res_ws[-1] - res_ws[0]) // (len(res_ws) - 1)
        d = self._depth_parse(res_ws, d)
        return d

    def _depth_parse(self, ws, d):
        rs = []
        ds=[]
        # print(ws,d)
        for i, w in enumerate(ws):
            if i < len(ws) - 1:
                rs.append(ws[i + 1] - w)
        rs.sort(reverse=True)
        for index,r in enumerate(rs):
            if r>=d:
                ds.append(r)
        return sum(ds)//len(ds)

    def __del__(self):
        try:
            if os.path.exists(self.__ps):
                os.remove(self.__ps)
        except:
            traceback.print_exc()


if __name__ == '__main__':
    img = ImageTrace('test.png',crops=(120,70))
    print(img())
    # print(img.parse_space(img.get_space()))
# Image.open('test.png').convert('L').save('test1.png')
#
# im=Image.open('test1.png')
#
#
# width,height=im.size
# im = im.convert('RGB')
# img_obj=im.load()
# min_tiaoshu=2
# ws=[]
# for w in range(width):
#     cicle=[]
#     for h in range(height):
#         rgb=im.getpixel((w,h))
#         if rgb==(255,255,255):
#             down_hs= set()
#             up_hs=set()
#             for tmp_h1 in range(h-5,h):
#                 color=img_obj[w, tmp_h1]
#                 if color !=(255,255,255) and color !=(0,0,0):
#                     down_hs.add((w,h,color))
#             for tmp_h2 in range(h,h+5):
#                 color = img_obj[w, tmp_h2]
#                 if color !=(255,255,255) and color !=(0,0,0):
#                     up_hs.add((w,h,color))
#             # print(down_hs,up_hs)
#             if up_hs.intersection(down_hs):
#                 cicle.append(w)
#     if len(cicle)>=min_tiaoshu*2:
#         print(cicle)
#         ws.append(cicle[0])
#
# minx_jianju=20
# res_ws=[]
# for index,x in enumerate(ws[:-1]):
#     if x+minx_jianju<ws[index+1]:
#         res_ws.append(x)
# res_ws.append(ws[-1])
# d=(res_ws[-1]-res_ws[0])//(len(res_ws)-1)
#
# print(d)
