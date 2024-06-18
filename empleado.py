class Empleado:
    def __init__(self, rut, nombre, sexo, direccion, telefono, cargo, fecha_ingreso, area, departamento, nombre_contacto, relacion, telefono_contacto, nombre_carga, parentesco, genero_carga, rut_carga):
        self._rut = rut
        self._nombre = nombre
        self._sexo = sexo
        self._direccion = direccion
        self._telefono = telefono
        self._cargo = cargo
        self._fecha_ingreso = fecha_ingreso
        self._area = area
        self._departamento = departamento
        self._nombre_contacto = nombre_contacto
        self._relacion = relacion
        self._telefono_contacto = telefono_contacto
        self._nombre_carga = nombre_carga
        self._parentesco = parentesco
        self._genero_carga = genero_carga
        self._rut_carga = rut_carga
        self._contactos_emergencia = []  # Lista de contactos de emergencia
        self._cargas_familiares = []  # Lista de cargas familiares

    @property
    def rut(self):
        return self._rut

    @rut.setter
    def rut(self, value):
        self._rut = value

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, value):
        self._nombre = value

    @property
    def sexo(self):
        return self._sexo

    @sexo.setter
    def sexo(self, value):
        self._sexo = value

    @property
    def direccion(self):
        return self._direccion

    @direccion.setter
    def direccion(self, value):
        self._direccion = value

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, value):
        self._telefono = value

    @property
    def cargo(self):
        return self._cargo

    @cargo.setter
    def cargo(self, value):
        self._cargo = value

    @property
    def fecha_ingreso(self):
        return self._fecha_ingreso

    @fecha_ingreso.setter
    def fecha_ingreso(self, value):
        self._fecha_ingreso = value

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, value):
        self._area = value
    
    @property
    def departamento(self):
        return self._departamento

    @departamento.setter
    def departamento(self, value):
        self._departamento = value

    @property
    def nombre_contacto(self):
        return self._nombre_contacto

    @nombre_contacto.setter
    def nombre_contacto(self, value):
        self._nombre_contacto = value

    @property
    def relacion(self):
        return self._relacion

    @relacion.setter
    def relacion(self, value):
        self._relacion = value

    @property
    def telefono_contacto(self):
        return self._telefono_contacto

    @telefono_contacto.setter
    def telefono_contacto(self, value):
        self._telefono_contacto = value

    @property
    def nombre_carga(self):
        return self._nombre_carga

    @nombre_carga.setter
    def nombre_carga(self, value):
        self._nombre_carga = value

    @property
    def parentesco(self):
        return self._parentesco

    @parentesco.setter
    def parentesco(self, value):
        self._parentesco = value

    @property
    def genero_carga(self):
        return self._genero_carga

    @genero_carga.setter
    def genero_carga(self, value):
        self._genero_carga = value

    @property
    def rut_carga(self):
        return self._rut_carga

    @rut_carga.setter
    def rut_carga(self, value):
        self._rut_carga = value

    @property
    def contactos_emergencia(self):
        return self._contactos_emergencia

    @property
    def cargas_familiares(self):
        return self._cargas_familiares
