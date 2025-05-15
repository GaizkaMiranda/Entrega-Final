import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configuración general
num_pacientes = 10
num_registros = 500
inicio = datetime.now()
tiempos = [inicio + timedelta(minutes=i) for i in range(num_registros)]

############################## Datos personales ficticios #####################################################
nombres = ['Carlos Ruiz', 'Ana Torres', 'Luis Gómez', 'María López', 'Pedro Sánchez',
           'Lucía Fernández', 'Diego Herrera', 'Laura Castro', 'Miguel Ortega', 'Sofía Moreno']
hospitales = [
    ('Hospital General Madrid', 'Madrid'),
    ('Clínica del Norte', 'Bilbao'),
    ('Hospital Central Sevilla', 'Sevilla'),
    ('Hospital Vall d\'Hebron', 'Barcelona'),
    ('Hospital Universitario de Álava - Txagorritxu', 'Vitoria-Gasteiz'),
]

############################### Generar datos de pacientes ##########################################################
pacientes = []
for i in range(num_pacientes):
    nombre = nombres[i]
    dni = f'{random.randint(10000000, 99999999)}{random.choice("TRWAGMYFPDXBNJZSQVHLCKE")}'
    edad = random.randint(25, 85)
    hosp, ciudad = random.choice(hospitales)
    
    pacientes.append({
        'paciente_id': i + 1,
        'nombre': nombre,
        'dni': dni,
        'edad': edad,
        'hospital': hosp,
        'ubicacion': ciudad
    })

df_pacientes = pd.DataFrame(pacientes)
df_pacientes.to_csv('pacientes.csv', index=False)


################################ Generar datos de sensores ##########################################################3

def generar_ritmo_cardiaco():
    return np.random.choice([np.random.normal(75, 10), np.random.normal(130, 5)], p=[0.95, 0.05])

def generar_spo2():
    return np.random.choice([np.random.normal(98, 1), np.random.normal(89, 1)], p=[0.97, 0.03])

def generar_frecuencia_respiratoria():
    return np.random.choice([np.random.normal(16, 2), np.random.normal(6, 1)], p=[0.96, 0.04])

def generar_presion_sistolica():
    return np.random.choice([np.random.normal(115, 10), np.random.normal(150, 5)], p=[0.95, 0.05])

def generar_presion_diastolica():
    return np.random.choice([np.random.normal(75, 8), np.random.normal(95, 3)], p=[0.95, 0.05])

actividad_niveles = ['reposo', 'ligero', 'moderado', 'intenso']
estados_animo = ['neutro', 'estresado', 'feliz', 'cansado']

################################ Registros médicos ##########################################################
datos_medicos = []
for paciente in pacientes:
    for t in tiempos:
        datos_medicos.append({
            'paciente_id': paciente['paciente_id'],
            'timestamp': t,
            'ritmo_cardiaco': int(generar_ritmo_cardiaco()),
            'spo2': round(generar_spo2(), 1),
            'temperatura': round(np.random.normal(36.6, 0.3), 1),
            'frecuencia_respiratoria': int(generar_frecuencia_respiratoria()),
            'presion_sistolica': int(generar_presion_sistolica()),
            'presion_diastolica': int(generar_presion_diastolica()),
            'actividad': random.choices(actividad_niveles, weights=[0.4, 0.3, 0.2, 0.1])[0],
            'pasos': int(np.random.choice([0, np.random.randint(10, 200)], p=[0.6, 0.4])),
            'estado_animo': random.choice(estados_animo)
        })

df_medico = pd.DataFrame(datos_medicos)
df_medico.to_csv('datos_salud_varios_pacientes.csv', index=False)
