import os
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

def auto_caption_images(processed_dir, trigger_word="ohwx man"):
    # Detección automática de aceleración por hardware (CUDA)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Inicializando modelo BLIP en: {device.upper()}")

    try:
        # Carga del procesador y modelo Vision-Language en caché/VRAM
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)
    except Exception as e:
        print(f" Error al cargar el modelo: {e}")
        return

    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    count = 0

    print("🔍 Analizando imágenes y generando vectores semánticos...")

    for filename in sorted(os.listdir(processed_dir)):
        if filename.lower().endswith(valid_extensions):
            img_path = os.path.join(processed_dir, filename)
            base_name = os.path.splitext(filename)[0]
            txt_path = os.path.join(processed_dir, f"{base_name}.txt")

            try:
                raw_image = Image.open(img_path).convert('RGB')
                
                # Inferencia del modelo
                inputs = processor(raw_image, return_tensors="pt").to(device)
                out = model.generate(**inputs, max_new_tokens=50)
                
                # Decodificación de tensores a lenguaje natural
                blip_caption = processor.decode(out[0], skip_special_tokens=True)
                
                # Inyección del Trigger Word de identidad
                final_caption = f"{trigger_word}, {blip_caption}, 1boy, solo, looking at viewer"
                
                with open(txt_path, 'w', encoding='utf-8') as f:
                    f.write(final_caption)
                
                print(f" {filename} ➔ {final_caption}")
                count += 1
                
            except Exception as e:
                print(f"❌ Error procesando {filename}: {e}")

    print(f"Proceso completado. Se han etiquetado {count} imágenes.")

if __name__ == "__main__":
    # Rutas relativas seguras (OPSEC)
    BASE_DIR = os.path.expanduser("~/ia-imag")
    PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed_dataset")
    
    # Etiqueta biométrica principal
    TRIGGER_WORD = "ohwx man" 
    
    auto_caption_images(PROCESSED_FOLDER, TRIGGER_WORD)
