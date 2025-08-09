import yt_dlp
import os
from urllib.parse import urlparse

def download_video(url, output_path='./downloads', quality='best'):
    """
    Downloads videos from multiple platforms (YouTube, Facebook, TikTok, Instagram, etc.)
    
    Args:
        url (str): URL of the video to download
        output_path (str): Directory to save downloaded videos
        quality (str): Preferred quality ('best', 'worst', '720p', '480p', etc.)
    
    Returns:
        str: Path to the downloaded video file or None if failed
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        # Set download options
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': get_format_selector(quality),
            'merge_output_format': 'mp4',
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,
            'force_generic_extractor': True,
        }
        
        # Platform-specific adjustments
        if 'instagram.com' in url:
            ydl_opts.update({'cookiefile': 'cookies.txt'})  # Instagram may require login
            
        if 'facebook.com' in url:
            ydl_opts.update({'format': 'best[height<=720]'})  # Facebook often limits quality
            
        # Download the video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"\nDownload complete: {os.path.basename(filename)}")
            return filename
            
    except Exception as e:
        print(f"\nError downloading video: {e}")
        return None

def get_format_selector(quality):
    """Returns format selector based on quality preference"""
    if quality == 'best':
        return 'bestvideo+bestaudio/best'
    elif quality == 'worst':
        return 'worstvideo+worstaudio/worst'
    elif quality.isdigit():
        return f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]'
    else:
        return 'bestvideo+bestaudio/best'

def clean_filename(filename):
    """Remove invalid characters from filenames"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_domain(url):
    """Extract domain name from URL"""
    parsed = urlparse(url)
    return parsed.netloc.replace('www.', '')

if __name__ == "__main__":
    print("Universal Video Downloader")
    print("Supports: YouTube, Facebook, Instagram, TikTok, Twitter, and many more\n")
    
    while True:
        url = input("Enter video URL (or 'q' to quit): ").strip()
        if url.lower() == 'q':
            break
            
        if not url.startswith(('http://', 'https://')):
            print("Please enter a valid URL starting with http:// or https://")
            continue
            
        domain = get_domain(url)
        print(f"\nDownloading from {domain}...")
        
        quality = input("Enter preferred quality (best, worst, or resolution like 720p): ").strip().lower()
        output_dir = input(f"Enter download directory (leave blank for './downloads'): ").strip()
        
        if not output_dir:
            output_dir = './downloads'
            
        download_video(url, output_dir, quality)
        
        print("\n" + "="*50 + "\n")