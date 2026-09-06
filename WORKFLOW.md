# Documentación Técnica y Guía de Despliegue: Arquitectura Nodal en ComfyUI

**Autor:** Daniel Costas San Miguel  
**Hardware de Despliegue:** NVIDIA GeForce RTX 3060 (12GB VRAM)  
**Propósito:** Guía de arquitectura, enrutamiento de nodos y resolución de dependencias para el pipeline de inferencia y micro-restauración facial mediante FaceDetailer.

---

## 1. Introducción y Arquitectura del Grafo

Este documento detalla el diseño técnico del flujo nodal implementado en ComfyUI para la generación fotorrealista de retratos utilizando un modelo LoRA entrenado sobre SDXL. A diferencia de las interfaces lineales tradicionales, la arquitectura basada en grafos permite interceptar el flujo de tensores latentes y aplicar técnicas de *inpainting* en cascada para preservar la identidad biométrica y maximizar el realismo de las micro-texturas (poros, vello facial y reflejos oculares).

---

## 2. Estructura y Conexiones del Pipeline Nodal

El grafo de ejecución se divide en bloques funcionales interconectados que gestionan desde la carga de pesos base hasta el post-procesamiento de la imagen final:

*   **Bloque de Carga y Modelos:**
    *   `Load Checkpoint`: Carga el modelo base (`RealVisXL V5.0`) extrayendo las salidas de `MODEL`, `CLIP` y `VAE`.
    *   `Load LoRA`: Se interpone en las señales de `MODEL` y `CLIP` aplicando el ajuste fino de identidad (`daniel_lora_v2`) con una `fuerza_modelo` de `0.85` y una `fuerza_clip` de `1.00`.
*   **Bloque de Condicionamiento Semántico:**
    *   `CLIP Text Encode (Positive)`: Aloja el *prompt* principal de escena, plano medio (*medium shot*), restricciones de vestuario (`long-sleeve t-shirt`) y directrices de textura orgánica.
    *   `CLIP Text Encode (Negative)`: Filtra artefactos digitales, iluminación de estudio y estilos ilustrativos.
*   **Bloque de Generación Base (KSampler):**
    *   Recibe el latente vacío (`1024x1024`), el modelo con LoRA integrado y los condicionamientos de texto.
    *   Configurado con 30 pasos, muestreador `euler_ancestral` y escala CFG de `5.5`. Su salida de imagen decodificada por el VAE pasa al sistema de detalle.
*   **Bloque de Detección y Restauración (FaceDetailer):**
    *   `UltralyticsDetectorProvider` (o proveedor ONNX con dimensiones dinámicas): Carga el modelo de detección de rostros (`face_yolov8m.pt`) y conecta su salida `BBOX_DETECTOR` al nodo `FaceDetailer`.
    *   El `FaceDetailer` intercepta la imagen generada por el KSampler principal, recorta una región de guía (*guide size*) de `512` píxeles centrada en el rostro, y aplica un segundo sub-muestreo con un `denoise` estricto de `0.40`.

---

## 3. Resolución de Conflictos Técnicos y Dependencias

Durante el despliegue del entorno sobre Ubuntu Linux con Python 3.12 y GPU RTX 3060, se resolvieron incidencias críticas documentadas para futuras réplicas del entorno:

*   **Incompatibilidad de Nodos Ultralytics Nativos:** Ante la falta de resolución de dependencias en el arranque del servidor para ciertos bloques de detección directa, se integró el paquete `ComfyUI Impact Subpack` para habilitar el proveedor de modelos compatible con la arquitectura de YOLOv8.
*   **Errores de Dimensiones en ONNX (`INVALID_ARGUMENT`):** Al exportar el modelo de detección a formato ONNX mediante terminal (`yolo export model=... format=onnx`), las matrices de entrada rígidas de `640x640` colisionaban con las resoluciones de `1024x1024` del flujo. Se solucionó habilitando el parámetro de exportación dinámica o utilizando el proveedor nativo del Subpack para procesar tensores variables sin desajustes de canales (`BCHW`).

---

## 4. Guía de Hiperparámetros Críticos

Para replicar con exactitud el equilibrio entre la precisión de la identidad biométrica y el realismo de los detalles, se deben mantener los siguientes valores en los nodos clave:

| Componente / Nodo | Parámetro | Valor Configurado | Justificación Técnica |
| :--- | :--- | :--- | :--- |
| **Cargar LoRA** | Fuerza del Modelo | `0.85` | Ancla la estructura ósea y los rasgos faciales exactos del dataset sin generar distorsiones plásticas. |
| **KSampler Principal** | Pasos / CFG / Sampler | `30` / `5.5` / `euler_ancestral` | Optimiza la coherencia volumétrica y la iluminación general de la escena base. |
| **FaceDetailer** | Denoise | `0.40` | Margen preciso que permite inyectar poros, vello facial (*stubble*) y reflejos oculares sin alterar la identidad del LoRA. |
| **FaceDetailer** | Guide Size / Feather | `512` / `10` | Define el área de recorte para el *inpainting* local y suaviza los bordes de la máscara para una fusión transparente. |
