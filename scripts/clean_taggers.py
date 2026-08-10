import os

# Ruta exacta donde Kohya lee los archivos de entrenamiento
directorio_textos = '/home/daniel/Escritorio/ia-imag/kohya_dataset/img/40_ohwx'

def purgar_captions():
    contador = 0
    for archivo in os.listdir(directorio_textos):
        if archivo.endswith('.txt'):
            ruta_completa = os.path.join(directorio_textos, archivo)
            # Sobrescribimos el archivo dejando únicamente el trigger word
            with open(ruta_completa, 'w', encoding='utf-8') as f:
                f.write('ohwx man')
            contador += 1
    
    print(f"¡Saneamiento completado! Se han limpiado {contador} archivos .txt.")

if __name__ == '__main__':
    purgar_captions()