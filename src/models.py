from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Series(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    series=db.Column(db.BigInteger)

class Role(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50),unique=True, nullable=False)
    description=db.Column(db.String(250))
    create_at=db.Column(db.Date)
    user= db.relationship('User')

    def __repr__(self) -> str:
        return super().__repr__()

    def serialize (self):
        return{
            "id":self.id,
            "name": self.name,
            "description": self.description
        }

class Asignacion(db.Model):
    id=db.Column(db.Integer,autoincrement=True, nullable=False, primary_key=True)
    serie=db.Column(db.BigInteger, db.ForeignKey('equipos.serie'), primary_key=True) #serie identificadora del equipo
    fecha_asignacion=db.Column(db.String(50),nullable=True)         # fecha de asignacion del equipo
    tecnico_id=db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True) # el tecnico_id es el mismo de user_id, solo tome el nombre mas a adecuado para la columna
    check=db.Column(db.Boolean)              #chequeo de las series
    estado=db.Column(db.String(20))         #indica si esta pendiente o aprobado
    equipso=db.relationship("Equipos")

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), unique = True, nullable = False)
    name = db.Column(db.String(250), unique=False, nullable=False)
    second_name=db.Column(db.String(100))
    last_name=db.Column(db.String(100),nullable=False)
    second_last_name=db.Column(db.String(100))
    email = db.Column(db.String(250), unique=True, nullable=False)
    rut=db.Column(db.String(10), unique=True, nullable=False)
    password=db.Column(db.String(10), unique=True, nullable=False)
    create_at=db.Column(db.Date)
    role_id=db.Column(db.Integer, db.ForeignKey('role.id'),nullable=False)
    asignacion=db.relationship("Asignacion")

    def __repr__(self) -> str:
        return super().__repr__()

    def serialize (self):
        return{
            "id":self.id, #Lo agrgeue para conocer el id del user y poder hacer los otros metodos
            "name": self.name,
            "second_name": self.second_name,
            "last_name": self.last_name,
            "second_last_name": self.second_last_name,
            "email": self.email,
            "rut": self.rut,
            "create_at": self.create_at,
            "role_id": self.role_id
        }

class Equipos(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    documento_entrada=db.Column(db.BigInteger, nullable=True)   #indica el numero documento sap o pedido de entrada
    folio=db.Column(db.BigInteger)               #indica la utlima guia de despacho sap-Entel de entrada 
    fecha_folio=db.Column(db.Date)   #indica la utlimo fecha del documento sap de entrada 
    material=db.Column(db.Integer)              #codigo sku de entel
    denominacion=db.Column(db.String(100))       #descripcion del equipo
    serie=db.Column(db.BigInteger, db.ForeignKey('entrada.serie'),unique=True, nullable=False)  #serie identificadora del equipo
    b_origen_entrada=db.Column(db.String(20), )   #bodega de origen de entrada
    b_destino_entrada=db.Column(db.String(20),)  #bodega destino de entrada, debe indicar una bodega de la empresa que produce (Ej: Yelou)
    fecha_recepcion=db.Column(db.Date)               #la utlima fecha en que se recibio el equipo fisicamente
    fecha_verificacion=db.Column(db.Date)            #la utlima fecha en que se verifico el euqipo fisicamente
    estado_bodega=db.Column(db.String(20),)      #estado en que se encuentra fisicamente (recibido,bodega,laboratorio,despachado)
    estado_prod=db.Column(db.String(20), )        #estado en que se encuentra el equipo en proceso productivo (sin procesar, procesando, terminado)
    documento_salida=db.Column(db.BigInteger, )    #indica el utlimo numero documento sap o pedido de salida
    guia_despacho=db.Column(db.Integer, )         #indica la utlima guia de despacho de la empresa productora
    b_origen_salida= db.Column(db.String(20), )   #bodega de origen de salida de la empresa productora
    b_destino_salida=db.Column(db.String(20), )   #bodega de destino de salia (centros de distribucion Entel)
    fecha_despacho=db.Column(db.Date, ) #indica la ultima fecha de despacho del equipo
    create_at=db.Column(db.Date)                        #Fecha de creación del registro
    #--------------------------------- Datos de Bodega-------------------------------------------------------------------------
    tipo_caja=db.Column(db.String(2))                           #tipo de caja almacenado, este valor puede ser nulo
    nro_caja=db.Column(db.Integer)                              #numero de caja de almacenado, este valor puede ser nulo
    estante=db.Column(db.Integer)                               #estante donde esta almacenado el equipo
    piso= db.Column(db.Integer)                                 #numero de piso del estante donde se encuentra el equipo
    #---------------------------------- observaciones generales----------------------------------------------------------------
    observaciones=db.Column(db.String(250),nullable=True)
    #--------------------------------- relacion----------------------------------------------------------------------------------
    # asignacion = db.relationship('user', secondary=Asignacion, lazy='subquery',
    #     backref=db.backref('equipos', lazy=True))

    def __repr__(self) -> str:
        return super().__repr__()

    def serialize (self):
        return{
            "serie": self.serie,
            "denominacion": self.denominacion,
            "tipo:caja": self.tipo_caja,
            "numero_caja": self.nro_caja,
            "estante":self.estante,
            "piso":self.piso,
            "observaciones":self.observaciones
        }

class Entrada(db.Model):
    id=db.Column(db.Integer, autoincrement=True , unique=True, nullable=False)
    documento=db.Column(db.BigInteger, primary_key=True, nullable=False)      #indica el numero documento sap o pedido de entrada
    folio=db.Column(db.BigInteger, nullable=True)          #indica la guia de despacho sap-Entel de entrada 
    fecha_folio=db.Column(db.Date)
    material=db.Column(db.Integer, nullable=True)          #codigo sku de entel
    denominacion=db.Column(db.String(100), nullable=True)       #descripcion del equipo
    serie=db.Column(db.BigInteger, nullable=False, primary_key=True ) #serie identificadora del equipo
    rut_empresa=db.Column(db.String(20))    #Rut de la empresa emisora de los equipos
    b_origen=db.Column(db.String(20)) #bodega de origen de envio
    b_destino=db.Column(db.String(20)) #bodega de destino (bodega de empresa productora)
    f_recepcion_fisica=db.Column(db.Date)                #Fecha de recepcion fisica
    f_verificacion=db.Column(db.String(50))                           #fecha de verificacion
    responsable_ver=db.Column(db.Integer)   #quien realiza registro de la verificacion
    tipo_caja=db.Column(db.String(2))                           #tipo de caja almacenado, este valor puede ser nulo
    nro_caja=db.Column(db.Integer)                              #numero de caja de almacenado, este valor puede ser nulo
    estado=db.Column(db.String(20),default="Pendiente")                            #indica lo siguiente: pendiente, verificado
    observaciones=db.Column(db.String(250),nullable=True)
    nombre=db.Column(db.String(20))
    rut=db.Column(db.String(20))
    # --------------------------------------- relationship -----------------------------------------------------
    equipos=db.relationship('Equipos',backref='entrada', lazy=True)
    

    def __repr__(self) -> str:
        return super().__repr__()

    def serialize (self):
        return{
            "serie": self.serie,
        }

class Revision_movil(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    # serie=db.Column(db.BigInteger, unique=False, nullable=False) #serie identificadora del equipo
    # material=db.Column(db.Integer, nullable=False)          #codigo sku de entel
    # denominacion=db.Column(db.String(100), nullable=False)       #descripcion del equipo
    # tecnico_id=db.Column(db.Integer, nullable=False)               #id del tecnico asignado
    # fecha=db.Column(db.Date,nullable=False)         #fecha de asignacion al tecnico
    encendido=db.Column(db.Boolean)    #encendido del equipo
    #--------------------------------- revision cosmetica--------------------------------------------
    frontal=db.Column(db.Boolean)      #vista frontal del equipo
    frontal_r=db.Column(db.Boolean)    #vista frontal con reflejo de luz
    trasera=db.Column(db.Boolean)      #vista trasera
    trasera_r=db.Column(db.Boolean)    #vista trasera con reflejo de luz
    superior=db.Column(db.Boolean)     #vista borde superior
    superior_r=db.Column(db.Boolean)   #vista borde superior con reflejo de luz
    inferior=db.Column(db.Boolean)     #vista borde inferior
    inferior_r=db.Column(db.Boolean)    #vista borde inferior con reflejo de luz
    izquierdo=db.Column(db.Boolean)    #vista borde izquierdo
    izquierdo_r=db.Column(db.Boolean)  #vista borde izquierdo con reflejo de luz
    derecho=db.Column(db.Boolean)      #vista borde derecho
    derecho_r=db.Column(db.Boolean)    #vista borde derecho con reflejo de luz
    puntaje_cos=db.Column(db.Integer)   #puntaje cosmetico: es la suma de toda la evaluacion cosmetica, la cual cada columna tiene valor 1 si es True o 0 si es False
    #--------------------------------- revision técnica--------------------------------------------
    pantalla=db.Column(db.Boolean)     #revsion de pantalla
    tactil=db.Column(db.Boolean)       #revision de táctil
    botones=db.Column(db.Boolean)      #revision de botones laterales
    mic=db.Column(db.Boolean)          #revision de microfonos, y sea superior, inferior o ambos
    audio=db.Column(db.Boolean)        #revisión de parlante inferior, superior y auricular
    bateria=db.Column(db.Boolean)      #revision de bateria
    conector_c=db.Column(db.Boolean)    #revision de conector de carga
    bluetooth=db.Column(db.Boolean)    #revision del bluetooth
    wifi=db.Column(db.Boolean)         #revision de funcionamiento wifi
    zona_w=db.Column(db.Boolean)       #revision de funcionamiento de zona wifi
    nfc=db.Column(db.Boolean)          #revision de sensor nfc
    conector_a=db.Column(db.Boolean)   #revision de conector de audio de 3.5mm (conector para manos libres)
    porta_sim=db.Column(db.Boolean)    #revision del estado del porta sim
    filtracion=db.Column(db.Boolean)   #revision de filtracion del equipo, esta dato indica que no tiene filtraciones
    llamadas_e=db.Column(db.Boolean)   #ejecucion de emision de llamadas
    llamadas_r=db.Column(db.Boolean)   #recepcion de llamadas
    msj_e=db.Column(db.Boolean)        #ejecucion de emision de mensajes de texto
    msj_r=db.Column(db.Boolean)        #recepcion de mensajes de texto
    foto_f=db.Column(db.Boolean)       #toma de foto con camara frontal
    foto_t=db.Column(db.Boolean)       #toma de fotos con camara trasera
    video_f=db.Column(db.Boolean)       #toma de videos con camara frontal
    video_t=db.Column(db.Boolean)      #toma de videos con camara trasera
    sen_proximidad=db.Column(db.Boolean)   #revisoin de sensor de proximidad
    vibrador=db.Column(db.Boolean)     #revision de vibracion del equipo
    puntaje_tec=db.Column(db.Integer)   #puntaje de evaluacion tecnica
    #-----------------------------------revision de software----------------------------------------------------
    bloqueo=db.Column(db.Boolean)  #revision de bloqueo de cuentas google, xiaomi, etc.
    act_sw=db.Column(db.Boolean)   #actualizacion de software
    restauracion=db.Column(db.Boolean) #restauracion de software
    #-------------------------------------fin revision------------------------------------------------------------
    fecha_rev=db.Column(db.String(50))      #fecha de revision del equipo
    clasificacion=db.Column(db.String(20))  #campo calculado que indicara si el equipos bueno, rayado, rayado con problemas de sw, problemas de sw, scrap
    ert=db.Column(db.Boolean)      #indica si el equipo sera utilizado como ert
    observaciones=db.Column(db.String(100)) #se anotan los comentarios adicionales
    #--------------------------------------- relacion ---------------------------------------------
    id_asignacion=db.Column(db.Integer, db.ForeignKey('asignacion.id')) # esta es la relacion con la asignacion
    salida=db.relationship('Salida')

    def __repr__(self) -> str:
        return super().__repr__()

    def serialize (self):
        return{
           "id": self.id,
        "serie": self.serie,
        "material": self.material,
        "denominacion" : self.denominacion,
        "tecnico_id"  : self.tecnico_id,
        "fecha"  : self.fecha,
        "encendido" : self.encendido,
        "frontal"  : self.frontal,
        "frontal_r"  : self.frontal_r,
        "trasera" : self.trasera,
        "trasera_r"  : self.trasera_r,
        "superior"  : self.superior,
        "superior_r" : self.superior_r,
        "inferior"  : self.inferior,
        "inferior_r"  : self.inferior_r,
        "izquierdo" : self.izquierdo,
        "izquierdo_r"  : self.izquierdo_r,
        "derecho"  : self.derecho,
        "derecho_r" : self.derecho_r,
        "puntaje_cos"  : self.puntaje_cos,
        "pantalla"  : self.pantalla,
        "tactil" : self.tactil,
        "mic"  : self.mic,
        "audio"  : self.audio,
        "bateria" : self.bateria,
        "conector_c"  : self.conector_c,
        "bluetooth"  : self.bluetooth,
        "wifi" : self.wifi,
        "zona_w"  : self.zona_w,
        "nfc"  : self.nfc,
        "conector_a"  : self.conector_a,
        "porta_sim"  : self.porta_sim,
        "filtracion"  : self.filtracion,
        "llamadas_e"  : self.llamadas_e,
        "llamadas_r"  : self.llamadas_r,
        "msj_e"  : self.msj_e,
        "msj_r"  : self.msj_r,
        "foto_f"  : self.foto_f,
        "foto_t"  : self.foto_t,
        "video_f"  : self.video_f,
        "video_t"  : self.video_t,
        "sen_proximidad"  : self.sen_proximidad,
        "vibrador"  : self.vibrador,
        "puntaje_tec"  : self.puntaje_tec,
        "bloqueo"  : self.bloqueo,
        "act_sw"  : self.act_sw,
        "restauracion"  : self.restauracion,
        "fecha_rev"  : self.fecha_rev,
        "clasificacion"  : self.clasificacion,
        "ert"  : self.ert,
        "observaciones"  : self.observaciones
        }

class Salida(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    serie=db.Column(db.BigInteger, nullable=False) #serie identificadora del equipo
    material=db.Column(db.Integer)          #codigo sku de entel
    denominacion=db.Column(db.String(100))       #descripcion del equipo
    empacado=db.Column(db.Boolean)      #indica si ya esta empacado el equipo
    fechaEmpacado=db.Column(db.String(50))        #fecha de empacado del equipo
    tipoEmpaque=db.Column(db.String(30))    #tipo de empaque individual del equipo
    responsable=db.Column(db.Integer)
    tipo_caja=db.Column(db.String(2))               #tipo de caja donde esta embalado el equipo, para este caso tendra valor fijo de "DM"
    nro_caja=db.Column(db.Integer)                  #numero de caja emitido por el sistema
    fecha_embalaje=db.Column(db.String(50))                        #fecha de embalado
    documento=db.Column(db.BigInteger)      #indica el numero documento sap o pedido de entrada
    guia_despacho=db.Column(db.Integer)         #indica la utlima guia de despacho de la empresa productora
    b_origen_salida= db.Column(db.String(20))   #bodega de origen de salida de la empresa productora
    b_destino_salida=db.Column(db.String(20))   #bodega de destino de salia (centros de distribucion Entel)
    fecha_documento=db.Column(db.Date)                    #indica la fecha de emsion del documento sap
    f_despacho_fisico=db.Column(db.Date)                        #indica la fecha de despacho fisico
    revision_movil_id=db.Column(db.Integer, db.ForeignKey('revision_movil.id'))

    def __repr__(self) -> str:
        return super().__repr__()

    def serialize (self):
        return{
            "serie": self.serie,
        }
