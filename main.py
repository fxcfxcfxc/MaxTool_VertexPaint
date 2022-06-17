import os
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QDockWidget
from PySide2.QtWidgets import QPushButton,QRadioButton,QSlider,QLabel
from PySide2.QtCore import QFile
from PySide2 import QtCore
from PySide2.QtUiTools import QUiLoader
import qtmax
from pymxs import runtime as rt

class VertexPaintWindow(QDockWidget):

    #构造函数 初始化
    def __init__(self, parent=None):

        super(VertexPaintWindow,self).__init__(parent)

        loader = QUiLoader()

        ui_file_path = os.path.join( os.path.dirname(os.path.realpath(__file__)), 'ui/VertexPaintTool.ui')

        ui_file = QFile(ui_file_path)

        ui_file.open(QFile.ReadOnly)

        self.ui = loader.load(ui_file, self)
        ui_file.close()

        self.setWindowFlags(QtCore.Qt.Tool)

        self.setWindowTitle("技术中心_顶点绘画工具套件")

        self.create_widget()
        self.create_connect()

        self.resize(500, 550)


    def create_widget(self):
        self.button_addVertexPaint = self.ui.findChild(QPushButton,'pushButton')
        self.button_vertexFromDataTomodifty = self.ui.findChild(QPushButton,'pushButton_6')
        #self.button_vertexFromDataTomodifty.setStyleSheet("background-color: blue")


    def create_connect(self):
        self.button_vertexFromDataTomodifty.clicked.connect(self.vertexFromDataTomodifty)
        self.button_addVertexPaint.clicked.connect(self.addVertexPaint)

    def addVertexPaint(self):
        targetobj = rt.selection[0]

    # def vertexFromDataTomodifty(self):
    #     #获取目标对象
    #     target_obj = rt.selection[0]
    #     print(target_obj)
    #
    #     #得到顶点序号,返回bitarray类型
    #     numVertex = rt.polyop.getVertSelection(target_obj)
    #     print(numVertex)
    #
    #
    #     #存放所有顶点色
    #     colorarry = []
    #
    #     for x  in range(numVertex.count):
    #
    #         # 选择当前点
    #         target_obj.setSelection(1, rt.BitArray(x+1))
    #
    #         #0代表枚举类型 rgb
    #         a = target_obj.GetVertexColor(0)
    #
    #         #将当前点的顶点色 加入数组
    #         colorarry.append(a)
    #
    #     #将所有顶点的颜色 设置为1
    #
    #     target_obj.setSelection(1,numVertex)
    #     target_obj.SetVertexColor(rt.color(255,255,255),0)
    #
    #     # 第一层基础修改器
    #     paintmod01 = rt.PaintLayerMod()
    #     paintmod01.name = 'Base'
    #
    #     # 第二层R
    #     paintmod02 = rt.PaintLayerMod()
    #     paintmod02.name = 'R'
    #
    #     # 第三层G
    #     paintmod03 = rt.PaintLayerMod()
    #     paintmod03.name = 'G'
    #
    #     # 第二层B
    #     paintmod04 = rt.PaintLayerMod()
    #     paintmod04.name = 'B'
    #
    #
    #
    #     #------------------第一层Normal设置---------------
    #     rt.addModifier(target_obj, paintmod01)
    #
    #     #------------------R层设置------------------------
    #     #设置绘制状态为R层
    #     rt.addModifier(target_obj, paintmod02)
    #     s = paintmod02.AcquirePaintState(target_obj)
    #     paintmod02.layerMode= 'Subtract'
    #     #将原来的 R通道 设置到R层
    #     for  index  in  range(numVertex.count):
    #         s.SetVertColor(index+1, rt.Point4( (1.0- (colorarry[index].r) / 255.0 ) , 0, 0, 1) )
    #     paintmod02.ApplyPaintState(target_obj,s)
    #
    #     # ------------------G层设置------------------------
    #     # 设置绘制状态为G层
    #     rt.addModifier(target_obj, paintmod03)
    #     s = paintmod03.AcquirePaintState(target_obj)
    #     paintmod03.layerMode = 'Subtract'
    #     # 将原来的 R通道 设置到R层
    #     for index in range(numVertex.count):
    #         s.SetVertColor(index + 1, rt.Point4(0, (1.0 - (colorarry[index].g) / 255.0), 0, 1))
    #     paintmod03.ApplyPaintState(target_obj, s)
    #
    #
    #     # ------------------B层设置------------------------
    #     # 设置绘制状态为B层
    #     rt.addModifier(target_obj, paintmod04)
    #     s = paintmod04.AcquirePaintState(target_obj)
    #     paintmod04.layerMode = 'Subtract'
    #     # 将原来的 R通道 设置到R层
    #     for index in range(numVertex.count):
    #         s.SetVertColor(index + 1, rt.Point4(0, 0, (1.0 - (colorarry[index].b) / 255.0), 1))
    #     paintmod04.ApplyPaintState(target_obj, s)


    def vertexFromDataTomodifty(self):
        #获取目标对象
        target_obj = rt.selection[0]
        print(target_obj)

        # #得到顶点序号,返回bitarray类型
        # numVertex = rt.polyop.getFacetSelection(target_obj)
        # print(numVertex)

        colorarry = []
        paintmod01 = rt.PaintLayerMod()
        paintmod01.name = 'Base'
        rt.addModifier(target_obj, paintmod01)
        s = paintmod01.AcquirePaintState(target_obj)

        x = s.GetNumRawColors()
        for index in range(x):

            colorpoint = s.GetFaceVertColor(index+1);
            colorarry.append(colorpoint)
        print(colorarry)
        #存放所有顶点色
        # colorarry = []

        # for x  in range(numVertex.count):
        #
        #     # 选择当前点
        #     target_obj.setSelection(1, rt.BitArray(x+1))
        #
        #     #获取当前选择的顶点颜色
        #     a = target_obj.GetVertexColor(0)
        #
        #     #将当前点的顶点色 加入数组
        #     colorarry.append(a)
        #
        # #将所有顶点的颜色 设置为1
        #
        # target_obj.setSelection(1,numVertex)
        # target_obj.SetVertexColor(rt.color(255,255,255),0)
        #
        # # 第一层基础修改器
        # paintmod01 = rt.PaintLayerMod()
        # paintmod01.name = 'Base'
        #
        # # 第二层R
        # paintmod02 = rt.PaintLayerMod()
        # paintmod02.name = 'R'
        #
        # # 第三层G
        # paintmod03 = rt.PaintLayerMod()
        # paintmod03.name = 'G'
        #
        # # 第二层B
        # paintmod04 = rt.PaintLayerMod()
        # paintmod04.name = 'B'
        #
        #
        #
        # #------------------第一层Normal设置---------------
        # rt.addModifier(target_obj, paintmod01)
        #
        # #------------------R层设置------------------------
        # #设置绘制状态为R层
        # rt.addModifier(target_obj, paintmod02)
        # s = paintmod02.AcquirePaintState(target_obj)
        # paintmod02.layerMode= 'Subtract'
        # #将原来的 R通道 设置到R层
        # for  index  in  range(numVertex.count):
        #     s.SetVertColor(index+1, rt.Point4( (1.0- (colorarry[index].r) / 255.0 ) , 0, 0, 1) )
        # paintmod02.ApplyPaintState(target_obj,s)
        #
        # # ------------------G层设置------------------------
        # # 设置绘制状态为G层
        # rt.addModifier(target_obj, paintmod03)
        # s = paintmod03.AcquirePaintState(target_obj)
        # paintmod03.layerMode = 'Subtract'
        # # 将原来的 R通道 设置到R层
        # for index in range(numVertex.count):
        #     s.SetVertColor(index + 1, rt.Point4(0, (1.0 - (colorarry[index].g) / 255.0), 0, 1))
        # paintmod03.ApplyPaintState(target_obj, s)
        #
        #
        # # ------------------B层设置------------------------
        # # 设置绘制状态为B层
        # rt.addModifier(target_obj, paintmod04)
        # s = paintmod04.AcquirePaintState(target_obj)
        # paintmod04.layerMode = 'Subtract'
        # # 将原来的 R通道 设置到R层
        # for index in range(numVertex.count):
        #     s.SetVertColor(index + 1, rt.Point4(0, 0, (1.0 - (colorarry[index].b) / 255.0), 1))
        # paintmod04.ApplyPaintState(target_obj, s)



#代码真正运行的内容 从下面开始
if __name__ == '__main__':
    try:
        vertexPaint_window.close()
        vertexPaint_window.deleteLater()

    except:
        pass

    #获得max当前主窗口对象
    main_window2 = qtmax.GetQMaxMainWindow()


    vertexPaint_window = VertexPaintWindow(parent=main_window2)

    vertexPaint_window.setFloating(True)

    vertexPaint_window.show()


