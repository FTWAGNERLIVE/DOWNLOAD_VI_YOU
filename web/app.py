from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp
import uuid
import threading
import os
import re
import imageio_ffmpeg

app = Flask(__name__)

# Basic dictionary to hold status
JOBS = {}
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

class MyLogger(object):
    def __init__(self, job_id):
        self.job_id = job_id
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        JOBS[self.job_id]['error'] = msg

def progress_hook(d, job_id):
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', 'N/A').strip()
        eta = d.get('_eta_str', 'N/A').strip()
        JOBS[job_id]['progress'] = percent_str
        JOBS[job_id]['speed'] = speed
        JOBS[job_id]['eta'] = eta
    elif d['status'] == 'finished':
        JOBS[job_id]['status'] = 'processing'

def download_task(job_id, url, quality):
    # Força MP4 com áudio M4A antes de cair para outros formatos, o que resolve problemas de players nativos do Windows ficarem mudos.
    format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
    if quality == "1080p":
        format_str = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=1080]+bestaudio/best'
    elif quality == "720p":
        format_str = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<=720]+bestaudio/best'
    elif quality == "audio":
        format_str = 'bestaudio/best'

    ydl_opts = {
        'format': format_str,
        'outtmpl': os.path.join(DOWNLOAD_DIR, f'{job_id}_%(title)s.%(ext)s'),
        'progress_hooks': [lambda d: progress_hook(d, job_id)],
        'merge_output_format': 'mp4',
        'quiet': True,
        'logger': MyLogger(job_id),
        'ffmpeg_location': imageio_ffmpeg.get_ffmpeg_exe()
    }

    if quality == "audio":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # We use extract_info with download=True to fetch metadata easily while downloading
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Adjust final extension based on format
            if quality == "audio":
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            elif 'merge_output_format' in ydl_opts:
                filename = filename.rsplit('.', 1)[0] + '.' + ydl_opts['merge_output_format']
            
            JOBS[job_id]['status'] = 'completed'
            JOBS[job_id]['filename'] = filename
            JOBS[job_id]['title'] = info.get('title', 'video')
    except Exception as e:
        JOBS[job_id]['status'] = 'error'
        JOBS[job_id]['error'] = str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    url = data.get('url')
    quality = data.get('quality')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
        
    job_id = str(uuid.uuid4())
    JOBS[job_id] = {'status': 'downloading', 'progress': '0%', 'speed': '', 'eta': ''}
    
    t = threading.Thread(target=download_task, args=(job_id, url, quality))
    t.start()
    
    return jsonify({'job_id': job_id})

@app.route('/status/<job_id>')
def status(job_id):
    job = JOBS.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job)

@app.route('/download/<job_id>')
def download_file(job_id):
    job = JOBS.get(job_id)
    if not job or job['status'] != 'completed':
        return "File not ready", 400
    
    filepath = job.get('filename')
    title = job.get('title') + os.path.splitext(filepath)[1]
    # Sanitizing filename for attachment
    sanitized_title = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ' or c=='.']).rstrip()
    
    if os.path.exists(filepath):
        return send_file(os.path.abspath(filepath), as_attachment=True, download_name=sanitized_title)
    else:
        return "Arquivo não encontrado no servidor", 404

if __name__ == '__main__':
    print("Iniciando servidor NexDownloader...")
    print("Acesse: http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)
