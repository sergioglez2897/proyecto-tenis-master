#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 14:12:59 2025

@author: sergio
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- 1. CONFIGURACIÓN DE LA ESCUELA ---

SEDES_OBJETIVO = {
    'Liceo de Taoro': 300,
    'San Marcos': 150,
    'La Vera': 130
}

# Licencias federativas (Competitiva vs No Competitiva)
LICENCIAS_OBJETIVO = {
    'Liceo de Taoro': 100,
    'La Vera': 60,
    'San Marcos': 40
}

# Configuración de Grupos (Capacidad por grupo)
CAPACIDAD_GRUPOS = {
    'Pre-tenis': 20,
    'Mini Tenis': 14,
    'Iniciación': 14,
    'Perfeccionamiento': 10,
    'Competición': 8,
    'Adultos': 8
}

# Precios orientativos
PRECIOS = {
    'Pre-tenis': 30, 'Mini Tenis': 35, 'Iniciación': 45,
    'Perfeccionamiento': 55, 'Competición': 70, 'Adultos': 60
}

# Grupos de Competición EXACTOS que pediste
# (El resto de categorías se llenarán automáticamente)
GRUPOS_COMPETICION_FIJOS = {
    'Liceo de Taoro': 3, # 3 grupos de 8
    'La Vera': 1,        # 1 grupo de 8
    'San Marcos': 1      # 1 grupo de 8
}

# --- 2. FUNCIONES ---

def generar_fecha_sin_agosto(inicio, fin):
    # Genera una fecha aleatoria pero evita el mes de AGOSTO (8)
    while True:
        delta = fin - inicio
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        fecha = inicio + timedelta(seconds=random_second)
        if fecha.month != 8: # Si no es agosto, nos vale
            return fecha

def calcular_letra_grupo(indice):
    # Convierte 0 -> A, 1 -> B, 2 -> C...
    return chr(65 + indice)

# --- 3. GENERACIÓN DE ALUMNOS BASE ---
print("Generando alumnos con lógica avanzada...")

lista_alumnos = []
contador = 1
hoy = datetime.now()
inicio_curso = hoy - timedelta(days=300) # Un curso académico aprox

# --- PASO A: Crear los huecos de COMPETICIÓN PURA primero (los VIP) ---
# Para asegurar que existen los grupos exactos que pediste
ids_competicion = []

for sede, num_grupos in GRUPOS_COMPETICION_FIJOS.items():
    total_compe_sede = num_grupos * CAPACIDAD_GRUPOS['Competición']
    for _ in range(total_compe_sede):
        lista_alumnos.append({
            "ID": f"Usuario_{str(contador).zfill(3)}",
            "Sede": sede,
            "Categoría": "Competición", # Categoría forzada
            "Edad": random.randint(10, 18),
            "Es_Competicion_Grupo": True # Marca interna
        })
        ids_competicion.append(lista_alumnos[-1]["ID"])
        contador += 1

# --- PASO B: Rellenar el resto hasta llegar a los 580 ---
for sede, objetivo in SEDES_OBJETIVO.items():
    # Contamos cuántos llevamos ya en esa sede (por los de competición que creamos antes)
    actuales = len([a for a in lista_alumnos if a["Sede"] == sede])
    faltan = objetivo - actuales
    
    for _ in range(faltan):
        id_usuario = f"Usuario_{str(contador).zfill(3)}"
        
        # Asignar Categoría por Probabilidad (Ajustada a tu realidad)
        # 40% Adultos, resto repartido en niños
        rand_cat = random.random()
        if rand_cat < 0.40:
            cat = 'Adultos'
            edad = random.randint(19, 65)
        elif rand_cat < 0.50:
            cat = 'Perfeccionamiento'
            edad = random.randint(12, 17)
        elif rand_cat < 0.70:
            cat = 'Iniciación'
            edad = random.randint(9, 11)
        elif rand_cat < 0.90:
            cat = 'Mini Tenis'
            edad = random.randint(6, 8)
        else:
            cat = 'Pre-tenis'
            edad = random.randint(3, 5)
            
        lista_alumnos.append({
            "ID": id_usuario,
            "Sede": sede,
            "Categoría": cat,
            "Edad": edad,
            "Es_Competicion_Grupo": False
        })
        contador += 1

# Convertimos a DataFrame para facilitar los siguientes pasos
df = pd.DataFrame(lista_alumnos)

# --- PASO 4: ASIGNAR LICENCIAS ---
# Tenemos que llegar a los objetivos de licencias (100 Liceo, 60 Vera, 40 SM)
# Prioridad: Los de grupo "Competición" TIENEN que tener licencia.
# El resto se reparte entre Perfeccionamiento y Adultos.

print("Asignando licencias federativas...")
df["Licencia"] = "No Competitiva" # Por defecto

for sede, objetivo_licencias in LICENCIAS_OBJETIVO.items():
    # 1. Filtrar alumnos de esa sede
    mask_sede = df["Sede"] == sede
    
    # 2. Los de Grupo Competición SIEMPRE tienen licencia
    mask_compe = mask_sede & (df["Categoría"] == "Competición")
    df.loc[mask_compe, "Licencia"] = "Competitiva"
    
    licencias_asignadas = mask_compe.sum()
    licencias_faltantes = objetivo_licencias - licencias_asignadas
    
    if licencias_faltantes > 0:
        # 3. Buscamos candidatos (Perf y Adultos) que aun no tengan licencia
        candidatos = df[
            mask_sede & 
            (df["Categoría"].isin(['Perfeccionamiento', 'Adultos'])) & 
            (df["Licencia"] == "No Competitiva")
        ].index.tolist()
        
        # Seleccionamos al azar
        if len(candidatos) >= licencias_faltantes:
            elegidos = random.sample(candidatos, licencias_faltantes)
            df.loc[elegidos, "Licencia"] = "Competitiva"

# --- PASO 5: ASIGNAR GRUPOS (LOGÍSTICA) ---
# Aquí creamos "Wiki Adultos A", "Wiki Adultos B"...
print("Creando grupos y asignando alumnos...")

df["Grupo"] = "Sin Asignar"
df = df.sort_values(by=["Sede", "Categoría"]) # Ordenar para agrupar bien

# Iteramos por cada Sede y Categoría para armar los grupos
for sede in df["Sede"].unique():
    for cat in df["Categoría"].unique():
        # Filtramos los alumnos de este subgrupo
        mask = (df["Sede"] == sede) & (df["Categoría"] == cat)
        alumnos_subgrupo = df[mask]
        
        if len(alumnos_subgrupo) == 0: continue
        
        capacidad = CAPACIDAD_GRUPOS.get(cat, 10)
        
        # Dividimos en trozos según la capacidad
        alumnos_indices = alumnos_subgrupo.index.tolist()
        chunks = [alumnos_indices[i:i + capacidad] for i in range(0, len(alumnos_indices), capacidad)]
        
        for i, chunk in enumerate(chunks):
            letra = calcular_letra_grupo(i)
            # Nombre chulo del grupo
            if cat == "Competición":
                nombre_grupo = f"Wiki Comp. {letra}"
            elif cat == "Adultos":
                nombre_grupo = f"Wiki Adultos {letra}"
            else:
                nombre_grupo = f"Wiki {cat} {letra}"
            
            df.loc[chunk, "Grupo"] = nombre_grupo

# --- PASO 6: DETALLES FINALES (Fechas, Precios, Estado) ---
df["Cuota"] = df["Categoría"].map(PRECIOS)
df["Fecha Nacimiento"] = df.apply(lambda row: hoy - timedelta(days=row["Edad"]*365), axis=1)

# Generar Fechas Alta/Baja (Sin Agosto)
print("Calculando fechas (evitando Agosto)...")
fechas_alta = []
fechas_baja = []
estados = []

for _ in range(len(df)):
    # Alta
    f_alta = generar_fecha_sin_agosto(inicio_curso, hoy)
    
    # Baja (10% de probabilidad)
    es_baja = random.random() < 0.10
    estado = "Activo"
    f_baja = None
    
    if es_baja:
        # La baja debe ser posterior al alta
        if f_alta < hoy - timedelta(days=30): # Solo si lleva tiempo
             # Intentamos generar fecha baja
             posible_baja = generar_fecha_sin_agosto(f_alta, hoy)
             if posible_baja > f_alta:
                 f_baja = posible_baja
                 estado = "Baja"
    
    fechas_alta.append(f_alta.date())
    fechas_baja.append(f_baja.date() if f_baja else None)
    estados.append(estado)

df["Fecha Alta"] = fechas_alta
df["Fecha Baja"] = fechas_baja
df["Estado"] = estados

# Limpieza final (quitamos columnas auxiliares)
df = df.drop(columns=["Es_Competicion_Grupo", "Edad"])

# --- GUARDAR ---
df.to_csv("datos_escuela.csv", index=False)

print("="*50)
print("¡DATOS ACTUALIZADOS CON ÉXITO!")
print(f"Total Alumnos: {len(df)}")
print("="*50)
print("RECUENTO DE GRUPOS DE COMPETICIÓN (Debe ser 3, 1, 1 de 8 pax):")
print(df[df["Categoría"]=="Competición"].groupby("Sede")["Grupo"].value_counts())
print("="*50)
print("RECUENTO DE LICENCIAS (Objetivo: 100, 60, 40):")
print(df[df["Licencia"]=="Competitiva"]["Sede"].value_counts())
print("="*50)