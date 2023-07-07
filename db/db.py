from pymongo.mongo_client import MongoClient

uri =  'mongodb+srv://cortegana:hV7fXizMZLzN7PR5@cluster0.jvpg63q.mongodb.net/Nobel'
client = MongoClient(uri)

mongo = client["Nobel"]

dbAdmins = mongo["Administrador"]
dbAlumnos = mongo["Alumnos"]
dbApoderados = mongo["Apoderados"]
dbDescuento = mongo["Descuento"]
dbInformacion = mongo["Informacion"]
dbPagos = mongo["Pagos"]

areas = {
    'Derecho': 'Derecho y C.P.',
    'Educación Inicial': 'Letras',
    'Trabajo Social': 'Letras',
    'Contabilidad y Finanzas': 'Economicas',
    'Educación Secundaria: Mención en Idiomas': 'Letras',
    'Arquitectura y Urbanismo': 'Ingenierias',
    'Administración': 'Economicas',
    'Educación Primaria': 'Letras',
    'Economía': 'Economicas',
    'Ciencias de la Comunicación': 'Letras',
    'Turismo': 'Letras',
    'Agronomía': 'Ingenierias',
    'Ingeniería Civil': 'Ingenierias',
    'Ingeniería Industrial': 'Ingenierias',
    'Ingeniería Agroindustrial': 'Ingenierias',
    'Ingeniería de Minas': 'Ingenierias',
    'Ingeniería de Sistemas': 'Ingenierias',
    'Informática': 'Ingenierias',
    'Ingeniería Ambiental': 'Ingenierias',
    'Ingeniería Mecánica': 'Ingenierias',
    'Ingeniería Mecatrónica': 'Ingenierias',
    'Ingeniería Química': 'Ingenierias',
    'Ingeniería Agrícola': 'Ingenierias',
    'Ciencias Políticas y Gobernabilidad': 'Derecho y C.P.',
    'Educación Secundaria: Mención en Lengua y Literatura': 'Letras',
    'Medicina': 'Medicina y C.S.',
    'Estomatología': 'Medicina y C.S.',
    'Enfermería': 'Medicina y C.S.',
    'Farmacia y Bioquímica': 'Medicina y C.S.'
}
