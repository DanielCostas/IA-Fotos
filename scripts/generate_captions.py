import os

def generate_captions(processed_dir, trigger_word="ohwx man"):
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    count = 0

    for filename in os.listdir(processed_dir):
        if filename.lower().endswith(valid_extensions):
            base_name = os.path.splitext(filename)[0]
            txt_path = os.path.join(processed_dir, f"{base_name}.txt")
            
            # Etiqueta base para condicionamiento de la red neuronal
            caption = f"{trigger_word}, 1boy, solo, looking at viewer"
            
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(caption)
            
            count += 1

    print(f"Se han generado {count} archivos .txt con la etiqueta de anclaje base.")

if __name__ == "__main__":
    # Ruta estandarizada relativa al entorno de usuario (OPSEC)
    BASE_DIR = os.path.expanduser("~/ia-imag")
    PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed_dataset")
    
    generate_captions(PROCESSED_FOLDER)
