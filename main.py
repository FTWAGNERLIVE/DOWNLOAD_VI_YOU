import customtkinter as ctk
import yt_dlp
import threading
import os
import shutil

ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader (HD/4K)")
        self.geometry("650x450")
        self.resizable(False, False)

        # UI Elements
        self.title_label = ctk.CTkLabel(self, text="YouTube Video Downloader", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(20, 10))

        self.url_entry = ctk.CTkEntry(self, width=500, placeholder_text="Cole o link do vídeo do YouTube aqui...")
        self.url_entry.pack(pady=10)

        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(pady=10, padx=20, fill="x")

        self.resolution_var = ctk.StringVar(value="Melhor Qualidade (Até 4K)")
        self.resolution_label = ctk.CTkLabel(self.options_frame, text="Qualidade:")
        self.resolution_label.pack(side="left", padx=(10, 5), pady=10)

        self.resolution_menu = ctk.CTkOptionMenu(self.options_frame, variable=self.resolution_var, values=["Melhor Qualidade (Até 4K)", "1080p", "720p", "Somente Áudio"])
        self.resolution_menu.pack(side="left", padx=5, pady=10)
        
        # Check if FFmpeg is installed
        self.ffmpeg_installed = shutil.which('ffmpeg') is not None
        if not self.ffmpeg_installed:
            self.warning_label = ctk.CTkLabel(
                self.options_frame, 
                text="Aviso: FFmpeg não detectado!\nQualidades acima de 720p podem não ter som.",
                text_color="orange", justify="left")
            self.warning_label.pack(side="right", padx=10)

        self.download_button = ctk.CTkButton(self, text="Baixar Vídeo", command=self.start_download, width=200, height=45, font=ctk.CTkFont(size=15, weight="bold"))
        self.download_button.pack(pady=20)

        self.progress_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.progress_label.pack(pady=(0, 5))

        self.progressbar = ctk.CTkProgressBar(self, width=500)
        self.progressbar.set(0)
        self.progressbar.pack(pady=5)

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            self.progress_label.configure(text="Por favor, insira um link válido.", text_color="red")
            return
            
        self.progress_label.configure(text="Iniciando download...", text_color="white")
        self.progressbar.set(0)
        self.download_button.configure(state="disabled")
        
        # Start download in a separate thread so GUI doesn't freeze
        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.start()

    def download_video(self, url):
        quality = self.resolution_var.get()
        
        # Default options
        format_str = 'bestvideo+bestaudio/best'
        if quality == "1080p":
            format_str = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
        elif quality == "720p":
            # 720p usually comes combined already on YT, so 'best' fallback works well
            format_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
        elif quality == "Somente Áudio":
            format_str = 'bestaudio/best'

        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

        ydl_opts = {
            'format': format_str,
            'outtmpl': os.path.join(downloads_folder, '%(title)s.%(ext)s'),
            'progress_hooks': [self.my_hook],
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': True
        }
        
        if quality == "Somente Áudio":
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.progress_label.configure(text=f"Concluído! Salvo em: {downloads_folder}", text_color="green")
        except Exception as e:
            error_msg = str(e)
            if "requested format not available" in error_msg.lower():
                error_msg = "Formato indisponível para este vídeo."
            self.progress_label.configure(text=f"Erro: {error_msg[:60]}...", text_color="red")
        finally:
            self.download_button.configure(state="normal")
            self.progressbar.set(1)

    def my_hook(self, d):
        if d['status'] == 'downloading':
            try:
                # Calculate progress and update progress bar
                percent_str = d.get('_percent_str', '0%').strip()
                # Remove ANSI escape codes
                percent_str = re.sub(r'\x1b\[[0-9;]*m', '', percent_str)
                percent = float(percent_str.replace('%', '')) / 100.0
                
                speed = re.sub(r'\x1b\[[0-9;]*m', '', d.get('_speed_str', 'N/A'))
                eta = re.sub(r'\x1b\[[0-9;]*m', '', d.get('_eta_str', 'N/A'))
                
                def update_ui():
                    self.progressbar.set(percent)
                    self.progress_label.configure(
                        text=f"Progresso: {percent_str} | Vel: {speed} | Tempo est.: {eta}", 
                        text_color="white"
                    )
                self.after(0, update_ui)
            except Exception:
                pass
        elif d['status'] == 'finished':
            def finish_ui():
                self.progress_label.configure(text="Download inicial concluído. Processando (pode demorar)...", text_color="#00ff00")
                self.progressbar.set(0.99)
            self.after(0, finish_ui)

import re

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
