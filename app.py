from flask import Flask, request, jsonify
import yt_dlp
import os


app = Flask(__name__)

@app.route('/fetch', methods=['GET'])
def fetch():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'No URL provided'}), 400

    ydl_opts = {
        'forcejson': True,
        'skip_download': True,
        'quiet': True,
        'no_warnings': True,
        'simulate': True,
        'cookiefile': 'cookies.txt',
        
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        videos = []
        if 'entries' in info:
            entries = info['entries']
        else:
            entries = [info]

        for e in entries:
            video = {
                'title': e.get('title'),
                'thumbnail': e.get('thumbnail'),
                'formats': []
            }
            for f in e.get('formats', []):
                if f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                    video['formats'].append({
                        'format_id': f.get('format_id'),
                        'ext': f.get('ext'),
                        'resolution': f.get('format_note'),
                        'filesize': f.get('filesize'),
                        'url': f.get('url')
                    })
            videos.append(video)

        return jsonify({'videos': videos})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

  
