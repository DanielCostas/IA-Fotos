import os
from PIL import Image

def process_images(input_dir, output_dir, target_size=(1024, 1024)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(valid_extensions):
            file_path = os.path.join(input_dir, filename)
            
            try:
                with Image.open(file_path) as img:
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    
                    width, height = img.size
                    new_size = min(width, height)
                    
                    left = (width - new_size) / 2
                    top = (height - new_size) / 2
                    right = (width + new_size) / 2
                    bottom = (height + new_size) / 2
                    
                    img_cropped = img.crop((left, top, right, bottom))
                    img_resized = img_cropped.resize(target_size, Image.Resampling.LANCZOS)
                    
                    output_path = os.path.join(output_dir, f"processed_{filename}")
                    img_resized.save(output_path, 'JPEG', quality=95)
                    
                    print(f"Procesada exitosamente: {filename}")
                    
            except Exception as e:
                print(f" Error procesando {filename}: {e}")

if __name__ == "__main__":
    # Rutas absolutas para evitar problemas al ejecutar
    BASE_DIR = os.path.expanduser("~/ia-imag")
    INPUT_FOLDER = os.path.join(BASE_DIR, "raw_dataset")
    OUTPUT_FOLDER = os.path.join(BASE_DIR, "processed_dataset")
    
    print("Iniciando el procesamiento de imágenes...")
    process_images(INPUT_FOLDER, OUTPUT_FOLDER)
    print("Proceso finalizado.")
