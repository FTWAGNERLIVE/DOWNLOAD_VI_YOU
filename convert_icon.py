from PIL import Image
import os

png_path = r"C:\Users\creat\.gemini\antigravity\brain\b5c5786a-ac24-42d1-9e9b-470ab7f3b658\ydl_icon_1775741305780.png"
if os.path.exists(png_path):
    # Carregar imagem original gerada (RGBA)
    img = Image.open(png_path).convert("RGBA")
    
    # 1. Gerar o ICone oficial (.ico)
    img.save("icon.ico")
    
    # 2. Gerar o Banner Lateral Grande pro Instalador (BMP - padrao 164x314)
    # Criamos um fundo estilo "Dark Mode" para ficar chique
    wizard_large = Image.new('RGB', (164, 314), (15, 23, 42)) 
    img_large = img.resize((140, 140))
    # Cola a logo centralizada no banner com transparencia suportada
    wizard_large.paste(img_large, (12, 87), img_large)
    wizard_large.save("wizard_large.bmp")
    
    # 3. Gerar a Logo Pequena do Canto Direito Superior (BMP - padrao 55x55)
    wizard_small = Image.new('RGB', (55, 55), (15, 23, 42))
    img_small = img.resize((55, 55))
    wizard_small.paste(img_small, (0, 0), img_small)
    wizard_small.save("wizard_small.bmp")

    print("Icone e Imagens Oficiais do Instalador geradas com sucesso!")
else:
    print("Imagem PNG nao encontrada. O aplicativo sera compilado sem arte customizada.")
