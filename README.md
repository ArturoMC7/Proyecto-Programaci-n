# Proyecto-Programaci-n
En el siguiente repositorio, encontrará los códigos diseñados para la implementación de un sistema de monitoreo y supervisión de contratos mediante un servidor, donde cada usuario tendrá su rol dentro del programa.
# Sistema de Supervisión de Contratos — Frontend en Python

## Descripción

Este proyecto corresponde al desarrollo del frontend gráfico para un Sistema de Supervisión de Contratos implementado en Python. La aplicación fue desarrollada utilizando Tkinter y trabaja bajo una arquitectura cliente-servidor, donde el frontend se comunica mediante solicitudes HTTP con un backend previamente desarrollado.

El sistema permite gestionar contratos, registrar seguimientos, consultar estadísticas, exportar información y manejar distintos niveles de acceso según el rol del usuario.

---

# Características principales

* Inicio de sesión con autenticación.
* Registro de usuarios.
* Control de acceso basado en roles.
* Gestión de contratos.
* Registro de seguimientos y avances de obra.
* Estadísticas generales del sistema.
* Exportación de contratos en formato CSV.
* Persistencia mediante archivos JSON.
* Arquitectura cliente-servidor.
* Interfaz gráfica desarrollada en Tkinter.
* Validaciones de datos y manejo de permisos.

---

# Roles del sistema

## Administrador (`admin`)

Tiene acceso completo al sistema:

* Mi perfil.
* Gestión de contratos.
* Avances de obra.
* Estadísticas.
* Exportación de CSV.

## Supervisor (`supervisor`)

Tiene acceso a:

* Mi perfil.
* Gestión de contratos.
* Avances de obra.
* Estadísticas.

No puede exportar archivos CSV.

## Viewer / Cliente (`viewer`)

Tiene acceso únicamente a:

* Mi perfil.
* Mis contratos.
* Cancelación de contratos propios.

---

# Arquitectura del proyecto

El sistema se encuentra dividido en diferentes módulos:

```text
Frontend (Tkinter)
        ↓
Cliente HTTP (supervision_client.py)
        ↓
Servidor Backend
        ↓
Archivos JSON
```

---

# Estructura del proyecto

```text
project/
│
├── iNter.py
├── supervision.py
├── supervision_client.py
├── auth.py
├── db.json
├── users.json
├── exports/
├── img/
└── README.md
```

---

# Explicación de archivos

## `iNter.py`

Contiene toda la interfaz gráfica desarrollada con Tkinter.

Funciones principales:

* Login.
* Registro.
* Dashboard.
* Gestión visual de contratos.
* Estadísticas.
* Seguimientos.

---

## `supervision_client.py`

Funciona como cliente HTTP.

Se encarga de:

* Enviar solicitudes al servidor.
* Recibir respuestas.
* Comunicar frontend y backend.

---

## `supervision.py`

Contiene la lógica principal del sistema.

Funciones principales:

* Registrar contratos.
* Buscar contratos.
* Actualizar estados.
* Cancelar contratos.
* Generar estadísticas.
* Exportar CSV.

---

## `auth.py`

Administra:

* Usuarios.
* Roles.
* Sesiones.
* Permisos.

---

## `db.json`

Archivo utilizado para almacenar contratos y seguimientos.

Ejemplo:

```json
{
  "number": "001",
  "contractor": "Velasquez",
  "status": "ACTIVO"
}
```

---

## `users.json`

Archivo utilizado para almacenar usuarios registrados.

Ejemplo:

```json
{
  "user": "admin1",
  "role": "admin"
}
```

---

# Tecnologías utilizadas

* Python 3
* Tkinter
* JSON
* HTTP Requests
* CSV

---

# Instalación

## 1. Clonar repositorio

```bash
git clone https://github.com/usuario/repositorio.git
```

---

## 2. Entrar al proyecto

```bash
cd repositorio
```

---

## 3. Instalar dependencias

```bash
pip install requests
```

---

# Ejecución del proyecto

## IMPORTANTE

El servidor debe ejecutarse antes de iniciar la interfaz gráfica.

Si el servidor no está activo, el frontend únicamente mostrará la pantalla inicial y no podrá acceder al resto de funcionalidades del sistema.

---

## 1. Ejecutar servidor

```bash
python server.py
```

---

## 2. Ejecutar interfaz gráfica

```bash
python iNter.py
```

---

# Funcionalidades del sistema

## Gestión de contratos

Permite:

* Registrar contratos.
* Buscar contratos.
* Actualizar estados.
* Cancelar contratos.

---

## Avances de obra

Permite:

* Registrar seguimientos.
* Asociar avances a contratos.
* Visualizar historial.

---

## Estadísticas

Muestra:

* Contratos de mayor valor.
* Dinero total invertido.
* Contratos próximos a vencer.

---

## Exportación CSV

Genera automáticamente un archivo CSV con toda la información contractual registrada.

Disponible únicamente para administradores.

---

# Validaciones implementadas

El sistema incluye validaciones para:

* Usuarios duplicados.
* Contratos duplicados.
* Fechas inválidas.
* Valores numéricos incorrectos.
* Roles y permisos.
* Credenciales inválidas.

---

# Persistencia de datos

Toda la información se almacena utilizando archivos JSON.

Esto permite:

* Mantener datos después de cerrar el programa.
* Simplicidad de implementación.
* Fácil lectura y modificación.

---

# Resultados obtenidos

Durante las pruebas realizadas se comprobó:

* Correcto funcionamiento del login.
* Persistencia de usuarios registrados.
* Comunicación cliente-servidor funcional.
* Restricción dinámica según roles.
* Gestión correcta de contratos.
* Generación adecuada de estadísticas.
* Exportación correcta de archivos CSV.

---

# Mejoras futuras

* Implementación de base de datos SQL.
* Cifrado de contraseñas.
* API REST más robusta.
* Sistema multiusuario concurrente.
* Dashboard con gráficas dinámicas.
* Despliegue en red local o internet.

---

# Autores

* Carlos Arturo Cardona Muñoz
* Lina Marcela Escobar González
* Juan Sebastian Rojas

Programa de Ingeniería Electrónica
Universidad del Quindío
