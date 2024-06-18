-- Primero asegúrate de que las tablas están vacías
DELETE FROM carga_familiar;
DELETE FROM contacto_emergencia;
DELETE FROM datos_laborales;
DELETE FROM empleados;

-- Insertar datos en la tabla empleados
INSERT INTO empleados (ID_EMPLEADOS, RUT, NOMBRE, GENERO_EMPLEADO, DIRECCION, TELEFONO) VALUES
(1, '11.111.111-1', 'Juan Perez', 'M', 'Calle Falsa 123', '912345678'),
(2, '22.222.222-2', 'Maria Gonzalez', 'F', 'Avenida Siempre Viva 456', '923456789'),
(3, '33.333.333-3', 'Pedro Martinez', 'M', 'Boulevard de los Sueños Rotos 789', '934567890'),
(4, '44.444.444-4', 'Lucia Fernandez', 'F', 'Calle de la Amargura 321', '945678901'),
(5, '55.555.555-5', 'Carlos Sanchez', 'M', 'Pasaje de la Esperanza 654', '956789012');

-- Insertar datos en la tabla datos_laborales
INSERT INTO datos_laborales (CARGO, FECHA_INGRESO, AREA, DEPARTAMENTO, ID_EMPLEADOS) VALUES
('Desarrollador', '2020-01-15', 'Tecnología', 'Desarrollo', 1),
('Analista', '2019-03-20', 'Finanzas', 'Contabilidad', 2),
('Gerente', '2018-07-10', 'Administración', 'Dirección', 3),
('Diseñadora', '2021-05-25', 'Marketing', 'Publicidad', 4),
('Soporte', '2017-11-30', 'Tecnología', 'Soporte Técnico', 5);

-- Insertar datos en la tabla contacto_emergencia
INSERT INTO contacto_emergencia (NOMBRE_CONTACTO, RELACION, TELEFONO_CONTACTO, ID_EMPLEADOS) VALUES
('Ana Perez', 'Esposa', '987654321', 1),
('Jose Gonzalez', 'Hermano', '976543210', 2),
('Laura Martinez', 'Madre', '965432109', 3),
('Pedro Fernandez', 'Padre', '954321098', 4),
('Elena Sanchez', 'Esposa', '943210987', 5);

-- Insertar datos en la tabla carga_familiar
INSERT INTO carga_familiar (NOMBRE_CARGA, PARENTESCO, GENERO_CARGA, RUT_CARGA, ID_EMPLEADOS) VALUES
('Luis Perez', 'Hijo', 'M', '11.111.111-2', 1),
('Marta Gonzalez', 'Hija', 'F', '22.222.222-3', 2),
('Carlos Martinez', 'Hijo', 'M', '33.333.333-4', 3),
('Julia Fernandez', 'Hija', 'F', '44.444.444-5', 4),
('Pablo Sanchez', 'Hijo', 'M', '55.555.555-6', 5);

-- Insertar datos en la tabla USUARIOS
INSERT INTO USUARIOS (RUT, NOMBRE_USUARIO, CONTRASENA) VALUES
('21220806-k','gat', 'password123'),
('21508106-0', 'rukawa', 'securepass123'),
('20453875-4', 'wesesu', 'mypassword123');

