from flask import Flask,request,render_template,redirect
import yt_dlp as ytd
import os
app=Flask(__name__)


@app.route('/',methods=["POST","GET"])
def homepage():
    if request.method=="POST":
        url=request.form['url_take']
        options={
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key':'FFmpegExtractAudio',
                'preferredcodec' :'mp3',
                'preferredquality':'192',
            }],
            'outtmpl':'C:/Users/SRIHAS/Desktop/prgramming/python/yt-dlp/static/audio/%(title)s.%(ext)s'
        }
        with ytd.YoutubeDL(options) as yld:
            yld.download([url])
    audio_folder = os.path.join(app.static_folder, 'audio')
    audio_files = [f for f in os.listdir(audio_folder) if f.endswith('.mp3')]

    return render_template('link.html',audio_files=audio_files)

@app.route('/delete/<string:audio_file>')
def delete(audio_file):
    audio_folder = os.path.join(app.static_folder, 'audio')
    dir_ad=os.listdir(audio_folder)
    file_path = os.path.join(audio_folder, audio_file)
    if audio_file in dir_ad:
        os.remove(file_path)
    return redirect('/')
    
if __name__=="__main__":
    app.run(debug=True)