from flask import Flask,request,render_template,redirect
import yt_dlp as ytd
import os
import pymysql as mc
import pymysql.cursors

app=Flask(__name__)

connection=mc.connect(
    host="localhost",
    port=1105,
    user="root",
    password="root",
    database="srihas"
)
data = connection.cursor(cursor=pymysql.cursors.DictCursor) 

@app.route('/',methods=["POST","GET"])
def first():
    if request.method=="POST":
        url=request.form['url_take']
        options={
            'format':'bestaudio/best',
            'postprocessors':[{
                'key':'FFmpegExtractAudio',
                'preferredcodec':'mp3',
                'preferredquality':'192',
        }],
        'outtmpl':'C:/Users/SRIHAS/Desktop/prgramming/python/yt-dlp/static/audio/%(title)s.%(ext)s',
        }

        with ytd.YoutubeDL(options) as ydl:
            ydl.download(url)
    folder=os.path.join(app.static_folder,'audio')
    music=[f for f in os.listdir(folder) if f.endswith(".mp3")]
    music_db=music
    data.execute("truncate music;")
    for music_loop in music_db:
        values=(music_loop,)
        query="insert into music(song) values (%s)"
        data.execute(query,values)
        connection.commit()
    return render_template('/link.html',music=music)
        

@app.route('/delete/<string:audio_file>')
def delete(audio_file):
    folder=os.path.join(app.static_folder,'audio')
    path=os.path.join(folder,audio_file)
    dir=os.listdir(folder)
    if audio_file in dir:
        os.remove(path)
    return redirect('/')


@app.route('/database',methods=["POST","GET"])
def database():
    data.execute("select * from music")
    data2=data.fetchall()
    return render_template('database.html',data2=data2)
       

if __name__=="__main__":
    app.run(debug=True)