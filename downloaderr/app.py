from flask import Flask, request, jsonify, send_from_directory, render_template
import yt_dlp
import os
import re
from urllib.parse import urlparse

app = Flask(__name__)

# Configuration
DOWNLOAD_FOLDER = 'downloads'
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
ALLOWED_DOMAINS = ['youtube.com', 'youtu.be', 'facebook.com', 'instagram.com', 'tiktok.com', 'twitter.com']

def sanitize_filename(filename):
    """Remove invalid characters from filenames"""
    return re.sub(r'[\\/*?:"<>|]', "_", filename)

def get_best_format(quality):
    """Determine the best format based on quality preference"""
    if quality == 'best':
        return 'bv*+ba/b'
    elif quality == 'worst':
        return 'wv*+wa/w'
    elif quality.isdigit():
        return f'bv*[height<={quality}]+ba/b[height<={quality}]'
    else:
        return 'bv*+ba/b'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    quality = data.get('quality', 'best')
    
    if not url:
        return jsonify({'success': False, 'message': 'URL is required'}), 400
    
    try:
        # Validate domain
        domain = urlparse(url).netloc.lower()
        if not any(allowed in domain for allowed in ALLOWED_DOMAINS):
            return jsonify({'success': False, 'message': 'Unsupported website'}), 400

        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': get_best_format(quality),
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_warnings': False,
            'extract_flat': False,
            'format_sort': ['res:1080', 'res:720', 'res:480', 'res:360'],
            'noplaylist': True,
        }
        
        # Platform-specific adjustments
        if 'instagram.com' in url:
            ydl_opts.update({
                'cookiefile': 'cookies.txt',
                'format': 'bestvideo+bestaudio/best'
            })
            
        if 'facebook.com' in url:
            ydl_opts.update({
                'format': 'best[height<=720]',
                'referer': 'https://facebook.com/'
            })
            
        if 'tiktok.com' in url:
            ydl_opts.update({
                'format': 'bv*+ba/b',
                'referer': 'https://www.tiktok.com/',
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            sanitized_filename = sanitize_filename(os.path.basename(filename))
            os.rename(os.path.join(DOWNLOAD_FOLDER, os.path.basename(filename)), 
                     os.path.join(DOWNLOAD_FOLDER, sanitized_filename))
            
            return jsonify({
                'success': True,
                'filename': sanitized_filename,
                'filepath': os.path.join(DOWNLOAD_FOLDER, sanitized_filename),
                'message': 'Download complete'
            })
            
    except yt_dlp.utils.DownloadError as e:
        # Try fallback format if first attempt fails
        try:
            ydl_opts['format'] = 'bv*+ba/b/wv*+wa/w'
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                sanitized_filename = sanitize_filename(os.path.basename(filename))
                os.rename(os.path.join(DOWNLOAD_FOLDER, os.path.basename(filename)), 
                         os.path.join(DOWNLOAD_FOLDER, sanitized_filename))
                
                return jsonify({
                    'success': True,
                    'filename': sanitized_filename,
                    'filepath': os.path.join(DOWNLOAD_FOLDER, sanitized_filename),
                    'message': 'Download complete (used fallback format)'
                })
        except Exception as e:
            return jsonify({'success': False, 'message': f'Download failed: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)