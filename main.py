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

        self.button_vertexFromDataTomodifty = self.ui.findChild(QPushButton,'pushButton_6')


    def create_connect(self):
        self.button_vertexFromDataTomodifty.clicked.connect(self.vertexFromDataTomodifty)


    def vertexFromDataTomodifty(self):
        #获取目标对象
        target_obj = rt.selection[0]
        print(target_obj)

        #得到顶点序号,返回bitarray类型
        numVertex = rt.polyop.getVertSelection(target_obj)
        # numVertex = rt.polyop.getNumVerts(target_obj)
        print(numVertex.count)

        #存放所有顶点色
        colorarry = []

        for x  in range(numVertex.count):

            # 选择当前点
            target_obj.setSelection(1, rt.BitArray(x+1))

            #0代表枚举类型 rgb
            a = target_obj.GetVertexColor(0)

            #将当前点的顶点色 加入数组
            colorarry.append(a)


        #第一层基础修改器
        paintmod01 = rt.PaintLayerMod()

        #第二层R
        paintmod02 = rt.PaintLayerMod()

        rt.addModifier(target_obj, paintmod01)
        rt.addModifier(target_obj,paintmod02)
        s = paintmod01.AcquirePaintState(target_obj)

        for  index  in  range(numVertex.count):
            s.SetVertColor(index+1, rt.Point4(  (colorarry[index].b) / 255.0, 0, 0, 1) )
        paintmod01.ApplyPaintState(target_obj,s)





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


