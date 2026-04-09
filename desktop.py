import sys
import os
import threading
import webview
import shutil
from web.app import app, JOBS

class WebviewApi:
    def save_video(self, job_id):
        job = JOBS.get(job_id)
        if not job or job['status'] != 'completed':
            return ""
            
        filepath = job.get('filename')
        title = job.get('title') + os.path.splitext(filepath)[1]
        sanitized_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ' or c=='.']).rstrip()
        
        try:
            result = webview.windows[0].create_file_dialog(
                webview.SAVE_DIALOG, 
                directory='', 
                save_filename=sanitized_title
            )
            if result:
                dest = result[0] if isinstance(result, tuple) else result
                shutil.copy(os.path.abspath(filepath), dest)
                
                # Executa alerta 100% nativo do Windows (sem nenhum vinculo com navegador)
                import ctypes
                # 36 significa MB_YESNO (botões Sim/Não) + MB_ICONQUESTION (ícone de pergunta)
                # 6 é o código de retorno quando o usuário clica em "Sim"
                open_dir = ctypes.windll.user32.MessageBoxW(
                    0, 
                    'Vídeo salvo com sucesso!\n\nDeseja abrir a pasta onde o arquivo foi salvo?', 
                    'YouDL', 
                    36
                ) == 6
                
                if open_dir:
                    import subprocess
                    subprocess.run(['explorer', '/select,', os.path.normpath(dest)])
                    
                return True
            return False
        except Exception as e:
            print("Error saving:", e)
            return ""

    def open_folder(self, filepath):
        import subprocess
        try:
            norm_path = os.path.normpath(filepath)
            subprocess.run(['explorer', '/select,', norm_path])
        except Exception as e:
            print("Error opening folder:", e)

def start_server():
    # Desativa os logs de output do Flask para não poluir
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    # Roda o Flask
    app.run(port=5000)

if __name__ == '__main__':
    # Inicia o backend em paralelo
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    # Cria uma API para comunicar o JS com o Python
    api = WebviewApi()

    # Cria uma janela nativa de desktop que aponta para o servidor interno
    webview.create_window(
        title='YouDL - Baixe vídeos',
        url='http://127.0.0.1:5000',
        width=700,
        height=800,
        resizable=False,
        js_api=api
    )
    
    # Inicia o app de desktop
    webview.start()

