import os

def purgar_captions(directorio_textos, trigger_word="ohwx man"):
    contador = 0
    if not os.path.exists(directorio_textos):
        print("La ruta no existe. Ejecuta primero la generación de captions.")
        return

    for archivo in os.listdir(directorio_textos):
        if archivo.endswith('.txt'):
            ruta_completa = os.path.join(directorio_textos, archivo)
            # Sobrescribimos el archivo dejando únicamente el trigger word
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                f.write(trigger_word)
            contador += 1
    
    print(f"¡Saneamiento completado! Se han limpiado {contador} archivos .txt.")

if __name__ == '__main__':
    BASE_DIR = os.path.expanduser("~/ia-imag")
    # Ajusta esta ruta a donde realmente tengas los .txt antes de entrenar
    TEXT_FOLDER = os.path.join(BASE_DIR, "kohya_dataset", "img", "40_ohwx")
    
    purgar_captions(TEXT_FOLDER)
