import os
from pymxs import runtime as rt
from PySide2.QtWidgets import QPushButton,QRadioButton,QSlider,QLabel,QButtonGroup,QDockWidget
from PySide2.QtCore import QFile
from PySide2 import QtCore,QtGui
from PySide2.QtUiTools import QUiLoader
import qtmax

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
        self.vertexPaint_targetobj = []

        self.create_widget()
        self.create_connect()

        self.resize(500, 550)

    def create_widget(self):
        self.button_addVertexPaint = self.ui.findChild(QPushButton,'pushButton')
        self.button_vertexFromDataTomodifty = self.ui.findChild(QPushButton,'pushButton_6')

        self.buttonGroup =QButtonGroup(self)

        #
        self.buttonGroup = QButtonGroup(self)
        self.radio_R =  self.ui.findChild(QRadioButton,"radioButton")
        self.radio_G = self.ui.findChild(QRadioButton, "radioButton_2")
        self.radio_B = self.ui.findChild(QRadioButton, "radioButton_3")
        self.radio_A = self.ui.findChild(QRadioButton, "radioButton_4")
        self.radio_RGB = self.ui.findChild(QRadioButton, "radioButton_10")

        self.buttonGroup_gray = QButtonGroup(self)
        self.radio0= self.ui.findChild(QRadioButton, "radioButton_5")
        self.radio25 = self.ui.findChild(QRadioButton, "radioButton_6")
        self.radio50 = self.ui.findChild(QRadioButton, "radioButton_7")
        self.radio75 = self.ui.findChild(QRadioButton, "radioButton_8")
        self.radio100 = self.ui.findChild(QRadioButton, "radioButton_9")

        self.buttonGroup.setExclusive(True)
        self.buttonGroup.addButton(self.radio_R,1)
        self.buttonGroup.addButton(self.radio_G,2)
        self.buttonGroup.addButton(self.radio_B,3)
        self.buttonGroup.addButton(self.radio_A,4)
        self.buttonGroup.addButton(self.radio_RGB,5)

        self.buttonGroup_gray.setExclusive(True)
        self.buttonGroup_gray.addButton(self.radio0, 6)
        self.buttonGroup_gray.addButton(self.radio25, 7)
        self.buttonGroup_gray.addButton(self.radio50, 8)
        self.buttonGroup_gray.addButton(self.radio75, 9)
        self.buttonGroup_gray.addButton(self.radio100, 10)

        self.button_close = self.ui.findChild(QPushButton,"pushButton_5")
        self.button_enable_channle_shader = self.ui.findChild(QPushButton,"pushButton_7")
        self.button_applayPaint = self.ui.findChild(QPushButton,"pushButton_2")
        self.button_setPaintMode = self.ui.findChild(QPushButton,"pushButton_3")
        self.button_setPaintMode_easer = self.ui.findChild(QPushButton, "pushButton_4")

    def create_connect(self):
        self.button_vertexFromDataTomodifty.clicked.connect(self.vertexFromDataTomodifty)
        self.button_addVertexPaint.clicked.connect(self.addVertexPaint)
        self.buttonGroup.buttonToggled.connect(self.Set_channel)
        self.buttonGroup_gray.buttonToggled.connect(self.Set_Color_gray)

        self.button_close.clicked.connect(self.closeRGB)
        self.button_enable_channle_shader.clicked.connect(self.enable_channle_shader)
        self.button_applayPaint.clicked.connect(self.applayVertexPaint)

        self.button_setPaintMode.clicked.connect(self.set_PaintMode)
        self.button_setPaintMode_easer.clicked.connect(self.set_PaintMode_easer)

    def addVertexPaint(self):
        self.target_paint = rt.selection[0]
        self.Base = rt.PaintLayerMod()
        self.R = rt.PaintLayerMod()
        self.G = rt.PaintLayerMod()
        self.B = rt.PaintLayerMod()

        paintmodifer = [self.Base,self.R,self.G,self.B]
        paintname = ["Base","R","G","B"]


        for x in range(4):
            rt.addModifier(self.target_paint, paintmodifer[x])
            paintmodifer[x].name = paintname[x]

            if(x!=0):
                paintmodifer[x].layerMode = 'Subtract'

    def applayVertexPaint(self):
        rt.convertTopoly(rt.selection[0])

    def Set_channel(self):
        a = rt.VertexPaintTool()
        graycolor = [0,25,50,75,100]
        if(self.radio_R.isChecked() == True):
            self.m.k_test = 1.0
            a.paintColor  = rt.color(255,0,0)
        if(self.radio_G.isChecked() == True):
            self.m.k_test = 2.0
            a.paintColor = rt.color(0,255,0)
        if(self.radio_B.isChecked() == True):
            self.m.k_test = 3.0
            a.paintColor = rt.color(0,0,255)
        if(self.radio_A.isChecked() == True):
            self.m.k_test = 4.0
        if(self.radio_RGB.isChecked() == True):
            self.m.k_test = 5.0

        rt.redrawViews()

    def vertexFromDataTomodifty(self):
        #获取场景对象
        target_obj = rt.selection[0]
        print(target_obj)
        #得到顶点序号,返回bitarray类型
        numVertex = rt.polyop.getVertSelection(target_obj)
        print(numVertex)

        #存放所有顶点色
        colorarry = []

        for x  in range(numVertex.count):

            # 选择当前点
            target_obj.setSelection(1, rt.BitArray(x+1))

            #0代表枚举类型 rgb
            a = target_obj.GetVertexColor(0)

            #将当前点的顶点色 加入数组
            colorarry.append(a)

        #将所有顶点的颜色 设置为1

        target_obj.setSelection(1,numVertex)
        target_obj.SetVertexColor(rt.color(255,255,255),0)

        # 第一层基础修改器
        paintmod01 = rt.PaintLayerMod()
        paintmod01.name = 'Base'

        # 第二层R
        paintmod02 = rt.PaintLayerMod()
        paintmod02.name = 'R'

        # 第三层G
        paintmod03 = rt.PaintLayerMod()
        paintmod03.name = 'G'

        # 第二层B
        paintmod04 = rt.PaintLayerMod()
        paintmod04.name = 'B'



        #------------------第一层Normal设置---------------
        rt.addModifier(target_obj, paintmod01)

        #------------------R层设置------------------------
        #设置绘制状态为R层
        rt.addModifier(target_obj, paintmod02)
        s = paintmod02.AcquirePaintState(target_obj)
        paintmod02.layerMode= 'Subtract'
        #将原来的 R通道 设置到R层
        for  index  in  range(numVertex.count):
            s.SetVertColor(index+1, rt.Point4( (1.0- (colorarry[index].r) / 255.0 ) , 0, 0, 1) )
        paintmod02.ApplyPaintState(target_obj,s)

        # ------------------G层设置------------------------
        # 设置绘制状态为G层
        rt.addModifier(target_obj, paintmod03)
        s = paintmod03.AcquirePaintState(target_obj)
        paintmod03.layerMode = 'Subtract'
        # 将原来的 R通道 设置到R层
        for index in range(numVertex.count):
            s.SetVertColor(index + 1, rt.Point4(0, (1.0 - (colorarry[index].g) / 255.0), 0, 1))
        paintmod03.ApplyPaintState(target_obj, s)


        # ------------------B层设置------------------------
        # 设置绘制状态为B层
        rt.addModifier(target_obj, paintmod04)
        s = paintmod04.AcquirePaintState(target_obj)
        paintmod04.layerMode = 'Subtract'
        # 将原来的 R通道 设置到R层
        for index in range(numVertex.count):
            s.SetVertColor(index + 1, rt.Point4(0, 0, (1.0 - (colorarry[index].b) / 255.0), 1))
        paintmod04.ApplyPaintState(target_obj, s)

    def enable_channle_shader(self):
        self.vertexPaint_targetobj = rt.selection
        self.m = rt.DXmaterial()
        # 相对路径转换为绝对路径
        self.m.effectfile = "E:\CodeProject\MaxTool_VertexPaint\MaxShader\DAM_Boby_Max_shader.fx"
        for x in self.vertexPaint_targetobj:
            x.material = self.m

    def closeRGB(self):
        self.m.k_test = 0.0
        rt.redrawViews()

    def set_PaintMode(self):
        a = rt.VertexPaintTool()

        a.curPaintMode = 1

        rt.redrawViews()

    def set_PaintMode_easer(self):
        a = rt.VertexPaintTool()

        a.curPaintMode = 2

        rt.redrawViews()

    def Set_Color_gray(self):
        a = rt.VertexPaintTool()
        if(self.radio_R.isChecked() == True):
            if(self.radio0.isChecked() == True):
                a.paintColor = rt.color(0,0,0)

            if (self.radio25.isChecked() == True):
                a.paintColor = rt.color(25, 0, 0)



        print("sdsss")

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


