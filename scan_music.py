# python scan_music.py  运行代码  
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # 启用跨域支持

@app.route('/music/')
def scan_music():
    music_dir = os.path.join(os.path.dirname(__file__), 'music')
    try:
        # 获取所有mp3文件并按修改时间排序
        mp3_files = [f for f in os.listdir(music_dir) if f.lower().endswith('.mp3')]
        mp3_files.sort(key=lambda x: os.path.getmtime(os.path.join(music_dir, x)))
        return jsonify(mp3_files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/picture/')
def scan_pictures():
    picture_dir = os.path.join(os.path.dirname(__file__), 'picture')
    try:
        # 获取所有图片文件
        picture_files = [f for f in os.listdir(picture_dir) 
                        if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif'))]
        return jsonify(picture_files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/music/<path:filename>')
def serve_music(filename):
    music_dir = os.path.join(os.path.dirname(__file__), 'music')
    response = send_from_directory(music_dir, filename)
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

@app.route('/picture/<path:filename>')
def serve_picture(filename):
    picture_dir = os.path.join(os.path.dirname(__file__), 'picture')
    response = send_from_directory(picture_dir, filename)
    response.headers['Cache-Control'] = 'public, max-age=31536000'
    return response

if __name__ == '__main__':
    app.run(port=5000, debug=False)