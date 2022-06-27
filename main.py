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

        self.resize(550, 650)


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


        self.button_addlayer = self.ui.findChild(QPushButton,"pushButton_8")
        self.button_subtractlayer = self.ui.findChild(QPushButton, "pushButton_9")

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

        self.button_addlayer.clicked.connect(self.addlayer)
        # self.button_subtractlayer.clicked.connect()

    def addVertexPaint(self):
        self.target_paint = rt.selection[0]
        self.Base = rt.PaintLayerMod()
        self.Base.name = "Base_RGB"

        rt.convertToMesh(self.target_paint)
        # 返回顶点数组
        numVer = rt.getNumVerts(self.target_paint)

        rt.convertTopoly(self.target_paint)
        # 添加修改器
        rt.addModifier(self.target_paint, self.Base)
        s = self.Base.AcquirePaintState(self.target_paint)


        #设置基础层每一个点颜色
        for index in range(numVer):
            s.SetVertColor(index+1, rt.point4(1, 0.5, 1, 1))


        self.Base.ApplyPaintState(self.target_paint, s)


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
        rt.convertToMesh(target_obj)

        paintmodtest = rt.PaintLayerMod()
        rt.addModifier(target_obj, paintmodtest)
        rt.convertToMesh(target_obj)
        target_obj = rt.selection[0]

        #得到顶点数量
        # numVertex = rt.polyop.getVertSelection(target_obj)
        numVertex = rt.getNumCPVVerts(target_obj)
        print(numVertex)

        #存放所有顶点色
        colorarry = []

        for x  in range(numVertex):

            # 选择当前点
            # target_obj.setSelection(1, rt.BitArray(x+1))

            #得到定点色 返回 color类型
            a = rt.getVertColor(target_obj,x+1)

            #将当前点的顶点色 加入数组
            colorarry.append(a)

        #将所有顶点的颜色 设置为1

        # target_obj.setSelection(1,numVertex)
        # target_obj.SetVertexColor(rt.color(255,255,255),0)

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
        # 将所有顶点的颜色 设置为1
        rt.addModifier(target_obj, paintmod01)
        s = paintmod01.AcquirePaintState(target_obj)

        for index in range(numVertex):
            s.SetRawColor(index+1,rt.Color(255, 255, 255, 255))
        paintmod01.ApplyPaintState(target_obj, s)

        #------------------R层设置------------------------
        #设置绘制状态为R层
        rt.addModifier(target_obj, paintmod02)
        s = paintmod02.AcquirePaintState(target_obj)
        paintmod02.layerMode ='Subtract'

        for  index  in  range(numVertex):
            s.SetRawColor(index+1, rt.Point4( (1.0 - colorarry[index].r / 255.0 ) , 0, 0, 1) )
        paintmod02.ApplyPaintState(target_obj, s)

        # ------------------G层设置------------------------
        # 设置绘制状态为G层
        rt.addModifier(target_obj, paintmod03)
        s = paintmod03.AcquirePaintState(target_obj)
        paintmod03.layerMode = 'Subtract'
        # 将原来的 R通道 设置到R层
        for index in range(numVertex):
            s.SetRawColor(index + 1, rt.Point4(0, (1.0 - (colorarry[index].g) / 255.0), 0, 1))
        paintmod03.ApplyPaintState(target_obj, s)


        # ------------------B层设置------------------------
        # 设置绘制状态为B层
        rt.addModifier(target_obj, paintmod04)
        s = paintmod04.AcquirePaintState(target_obj)
        paintmod04.layerMode = 'Subtract'
        # 将原来的 R通道 设置到R层
        for index in range(numVertex):
            s.SetRawColor(index + 1, rt.Point4(0, 0, (1.0 - (colorarry[index].b) / 255.0), 1))
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
                a.paintColor = rt.color(63.75, 0, 0)

            if (self.radio50.isChecked() == True):
                a.paintColor = rt.color(127.5, 0, 0)

            if (self.radio75.isChecked() == True):
                a.paintColor = rt.color(191.25, 0, 0)

            if (self.radio100.isChecked() == True):
                a.paintColor = rt.color(255, 0, 0)


        if(self.radio_G.isChecked() == True):
            if(self.radio0.isChecked() == True):
                a.paintColor = rt.color(0,0,0)

            if (self.radio25.isChecked() == True):
                a.paintColor = rt.color(0, 63.75, 0)

            if (self.radio50.isChecked() == True):
                a.paintColor = rt.color(0, 127.5, 0)

            if (self.radio75.isChecked() == True):
                a.paintColor = rt.color(0, 191.25, 0)

            if (self.radio100.isChecked() == True):
                a.paintColor = rt.color(0, 255, 0)


        if(self.radio_B.isChecked() == True):
            if(self.radio0.isChecked() == True):
                a.paintColor = rt.color(0,0,0)

            if (self.radio25.isChecked() == True):
                a.paintColor = rt.color(0, 0, 63.75)

            if (self.radio50.isChecked() == True):
                a.paintColor = rt.color(0, 0, 127.5)

            if (self.radio75.isChecked() == True):
                a.paintColor = rt.color(0, 0, 191.25)

            if (self.radio100.isChecked() == True):
                a.paintColor = rt.color(0, 0, 255)





        print("sdsss")

    def addlayer(self):
        if(self.radio_R.isChecked() == True):
            self.radd = rt.PaintLayerMod()
            self.radd.name = "R_add"
            self.radd.layerMode = 'Add'
            rt.addModifier(self.target_paint, self.radd)


        if (self.radio_G.isChecked() == True):
            self.gadd = rt.PaintLayerMod()
            self.gadd.name = "G_add"
            self.gadd.layerMode = 'Add'
            rt.addModifier(self.target_paint, self.gadd)

        if (self.radio_B.isChecked() == True):
            self.badd = rt.PaintLayerMod()
            self.badd.name = "B_add"
            self.badd.layerMode = 'Add'
            rt.addModifier(self.target_paint, self.badd)




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


