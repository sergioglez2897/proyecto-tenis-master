#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 18 09:34:20 2025

@author: sergio
"""

import pandas as pd
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN EXACTA ---
SEDES_OBJETIVO = {
    'Liceo de Taoro': 300,
    'San Marcos': 150,
    'La Vera': 130
}

PROYECTOS_OBJETIVO = {
    'Pichón Trail': 20,
    'Asmipuerto': 15,
    'Quiero ser como tu': 15
}

# Precios
PRECIOS = {
    'Mini Tenis': 35,
    'Iniciación': 45,
    'Competición': 65, # Un poco más caro
    'Adultos': 60
}

# --- 2. FUNCIONES ---
def fecha_aleatoria(inicio, fin):
    delta = fin - inicio
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return inicio + timedelta(seconds=random_second)

# --- 3. GENERANDO ALUMNOS ---
print("Generando alumnos...")
lista_alumnos = []
contador = 1
hoy = datetime.now()
hace_dos_anos = hoy - timedelta(days=730)

# Listas temporales para luego asignar competición y proyectos
ids_para_competicion = [] # Candidatos (niños de Liceo y La Vera)
ids_activos = [] # Para proyectos

for sede, cantidad in SEDES_OBJETIVO.items():
    for _ in range(cantidad):
        id_usuario = f"Usuario_{str(contador).zfill(3)}"
        
        # Lógica 40% Adultos vs 60% Niños
        es_adulto = random.random() < 0.40 
        
        if es_adulto:
            categoria = 'Adultos'
            edad = random.randint(19, 70)
        else:
            # Si es niño, asignamos temporalmente por edad
            edad = random.randint(4, 17)
            if 4 <= edad <= 8: categoria = 'Mini Tenis'
            else: categoria = 'Iniciación'
        
        cuota = PRECIOS[categoria]
        fecha_nac = hoy - timedelta(days=edad*365)
        
        # Fechas Alta/Baja
        fecha_alta = fecha_aleatoria(hace_dos_anos, hoy)
        es_baja = random.random() < 0.12 # 12% de bajas históricas
        fecha_baja = None
        estado = "Activo"
        
        if es_baja:
            dias_activo = random.randint(30, 400)
            posible_baja = fecha_alta + timedelta(days=dias_activo)
            if posible_baja < hoy:
                fecha_baja = posible_baja
                estado = "Baja"
        
        # Guardamos al alumno
        alumno = {
            "ID": id_usuario,
            "Sede": sede,
            "Estado": estado,
            "Categoría": categoria, # Esto puede cambiar a Competición luego
            "Edad": edad,
            "Fecha Nacimiento": fecha_nac.date(),
            "Fecha Alta": fecha_alta.date(),
            "Fecha Baja": fecha_baja.date() if fecha_baja else None,
            "Cuota": cuota
        }
        lista_alumnos.append(alumno)
        
        # Guardamos candidatos para lógica posterior
        if estado == 'Activo':
            ids_activos.append(id_usuario)
            # Para competición: Solo niños, activos, y NO de San Marcos
            if not es_adulto and sede in ['Liceo de Taoro', 'La Vera']:
                ids_para_competicion.append(id_usuario)
                
        contador += 1

# --- 4. ASIGNAR COMPETICIÓN (40 ALUMNOS) ---
# Seleccionamos 40 aleatorios de los candidatos (Liceo/Vera)
seleccionados_compe = random.sample(ids_para_competicion, 40)

for alumno in lista_alumnos:
    if alumno['ID'] in seleccionados_compe:
        alumno['Categoría'] = 'Competición'
        alumno['Cuota'] = PRECIOS['Competición']

# --- 5. ASIGNAR PROYECTOS ---
print("Asignando proyectos...")
lista_participaciones = []

# Copiamos la lista de activos para ir sacando gente y no repetir (si quieres)
candidatos_proyectos = ids_activos.copy()
random.shuffle(candidatos_proyectos)

for proyecto, num_plazas in PROYECTOS_OBJETIVO.items():
    # Tomamos los primeros X de la lista mezclada
    participantes = candidatos_proyectos[:num_plazas]
    # Los quitamos de la lista para que no repitan (opcional)
    candidatos_proyectos = candidatos_proyectos[num_plazas:]
    
    for id_alum in participantes:
        lista_participaciones.append({
            "Proyecto": proyecto,
            "ID_Alumno": id_alum
        })

# --- 6. CREAR LOS DATA FRAMES Y GUARDAR ---
df_alumnos = pd.DataFrame(lista_alumnos)
df_proyectos = pd.DataFrame(lista_participaciones)

# Guardamos 2 archivos CSV
df_alumnos.to_csv("datos_escuela.csv", index=False)
df_proyectos.to_csv("datos_proyectos.csv", index=False)

print("="*30)
print("¡PROCESO COMPLETADO EN SPYDER!")
print("="*30)
print(f"Total Alumnos: {len(df_alumnos)}")
print(f"Adultos: {len(df_alumnos[df_alumnos['Categoría']=='Adultos'])} (aprox 40%)")
print(f"Competición: {len(df_alumnos[df_alumnos['Categoría']=='Competición'])} (Objetivo: 40)")
print("Desglose Competición por Sede:")
print(df_alumnos[df_alumnos['Categoría']=='Competición']['Sede'].value_counts())
print("-" * 20)
print(f"Participaciones en Proyectos guardadas en 'datos_proyectos.csv': {len(df_proyectos)}")