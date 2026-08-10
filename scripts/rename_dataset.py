import os

def clean_and_rename(raw_dir, processed_dir):
    if not os.path.exists(raw_dir) or not os.path.exists(processed_dir):
        print("Una de las carpetas no existe. Revisa las rutas.")
        return

    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    
    # Listar y ordenar para mantener la consistencia secuencial
    raw_files = sorted([f for f in os.listdir(raw_dir) if f.lower().endswith(valid_extensions)])
    processed_files = sorted([f for f in os.listdir(processed_dir) if f.lower().endswith(valid_extensions)])
    
    if len(raw_files) != len(processed_files):
        print(f" Advertencia: Hay {len(raw_files)} fotos en raw y {len(processed_files)} en processed. Asegúrate de que el preprocesamiento fue exitoso.")
    
    print("Iniciando el renombrado masivo...")
    
    for index, raw_filename in enumerate(raw_files, start=1):
        ext = os.path.splitext(raw_filename)[1].lower()
        new_name = f"img_{index:03d}"  # Formato secuencial: img_001, img_002...
        
        # Generación de nuevos nombres
        new_raw_name = f"{new_name}{ext}"
        # Se fuerza .jpg asumiendo que el script preprocess.py ya convirtió las imágenes
        new_processed_name = f"{new_name}.jpg" 
        
        old_raw_path = os.path.join(raw_dir, raw_filename)
        new_raw_path = os.path.join(raw_dir, new_raw_name)
        
        # Mapeo y renombrado en la carpeta de procesados
        if index - 1 < len(processed_files):
            old_processed_filename = processed_files[index - 1]
            old_processed_path = os.path.join(processed_dir, old_processed_filename)
            new_processed_path = os.path.join(processed_dir, new_processed_name)
            
            os.rename(old_processed_path, new_processed_path)
        
        # Renombrado en la carpeta original
        os.rename(old_raw_path, new_raw_path)
        
        print(f"🔄 {raw_filename} ➔ {new_raw_name}")

    print("¡Renombrado completado con éxito!")

if __name__ == "__main__":
    # Ruta estandarizada relativa al entorno de usuario (OPSEC)
    BASE_DIR = os.path.expanduser("~/ia-imag")
    RAW_FOLDER = os.path.join(BASE_DIR, "raw_dataset")
    PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed_dataset")
    
    clean_and_rename(RAW_FOLDER, PROCESSED_FOLDER)
