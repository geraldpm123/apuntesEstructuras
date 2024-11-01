import openseespy.opensees as ops   # Biblioteca de OpenSeesPy
import vfo.vfo as vfo               # Biblioteca para visualizar los modelos

# Generar el modelo
ops.wipe() # Borra todo lo que se encuentra en el dominio
# Inicial el modelo ->basico con 2 ndm(number dimensions) y con 2 ndf(grados de libertad)
ops.model('basic', '-ndm', 2, '-ndf', 2) 

# Generar los nodos node(name, coordX, coordY) 
ops.node(1, 0.0, 0.0) 
ops.node(2, 3.0, 0.0)
ops.node(3, 6.0, 0.0)
ops.node(4, 9.0, 0.0)
ops.node(5, 12.0, 0.0)
ops.node(6, 15.0, 0.0)
ops.node(7, 18.0, 0.0)
ops.node(8, 3.0, 3.0) 
ops.node(9, 6.0, 3.0)
ops.node(10, 9.0, 3.0)
ops.node(11, 12.0, 3.0)
ops.node(12, 15.0, 3.0)

# Se definen las Restricciones (apoyos de la estructura).
# 1-Grado de libertad restringido
# 0-Grado de libertad no restringido
ops.fix(1, 1, 1)  #fix(name, restX, restY)
ops.fix(7, 0, 1) 

# Se define el material de los elementos de la armadura.
tagMaterial = 1
ops.uniaxialMaterial('Elastic', tagMaterial, 200e9) # Elastic es un material simple.


# Se definen los elementos de la armadura. Área del elemento = 0.0005 m2 = 5 cm2 
ops.element('truss',1, 2, 1, 0.0005, TagMaterial)
ops.element('truss',2, 2, 3, 0.0005, TagMaterial)
ops.element('truss',3, 3, 4, 0.0005, TagMaterial)
ops.element('truss',4, 4, 5, 0.0005, TagMaterial)
ops.element('truss',5, 5, 6, 0.0005, TagMaterial)
ops.element('truss',6, 6, 7, 0.0005, TagMaterial)
ops.element('truss',11, 1, 8, 0.0005, TagMaterial)
ops.element('truss',12, 2, 8, 0.0005, TagMaterial)
ops.element('truss',13, 2, 9, 0.0005, TagMaterial)
ops.element('truss',14, 3, 9, 0.0005, TagMaterial)
ops.element('truss',15, 3, 10, 0.0005, TagMaterial)
ops.element('truss',16, 4, 10, 0.0005, TagMaterial)
ops.element('truss',17, 5, 10, 0.0005, TagMaterial)
ops.element('truss',18, 5, 11, 0.0005, TagMaterial)
ops.element('truss',19, 6, 11, 0.0005, TagMaterial)
ops.element('truss',20, 6, 12, 0.0005, TagMaterial)
ops.element('truss',21, 7, 12, 0.0005, TagMaterial)
# # Barras del tirante superior. Área del elemento = 0.001 m2 = 10 cm2
ops.element('truss',7, 8, 9, 0.001, TagMaterial)
ops.element('truss',8, 9, 10, 0.001, TagMaterial)
ops.element('truss',9, 10, 11, 0.001, TagMaterial)
ops.element('truss',10, 11, 12, 0.001, TagMaterial)

# Se definen las cargas actuantes sobre la armadura.
timeLinear=1
ops.timeSeries('Linear',timeLinear)
ops.pattern('Plain',1,timeLinear)

# Cargas aplicadas en la armadura, ops.load(ID nodo, Fx, Fy)
ops.load(2, 0.0, -10000)
ops.load(3, 0.0, -15000)
ops.load(4, 0.0, -20000)
ops.load(5, 0.0, -15000)
ops.load(6, 0.0, -10000)

ops.load(7, 5000, 0.0)

# Creación de la base de datos
# Es importante actualizar la versión de vfo con "pip install --upgrade vfo"
vfo.createODB(model="Armadura",loadcase="Estatico")
vfo.plot_model(model="Armadura", show_nodes='yes',show_nodetags='yes',show_eletags='yes')

# Se definen registros de salida
ops.recorder('Element','-xml','Fuerzas.txt','-time','-ele',1,2,3,9,10,'basicForces')
ops.recorder('Node','-file','DeflexionSup.txt','-node',8,9,10,11,12,'-dof',2,'disp')
ops.recorder('Node','-file','DeflexionInf.txt','-node',1,2,3,4,5,6,7,'-dof',2,'disp')

# Se definen los parámetros del análisis estático.
ops.system('BandGeneral')
ops.numberer('RCM')
ops.constraints('Plain')
ops.test('NormDispIncr', 1.0e-6, 10)
ops.integrator('LoadControl', 0.1)
ops.algorithm('Newton')
ops.analysis('Static')
ops.analyze(10)

# Se elimina el modelo de OpenSees 
ops.wipe()

# Visualización de la forma deformada del modelo
vfo.plot_deformedshape(model="Armadura", loadcase="Estatico", scale=20)