from flask import Flask, redirect, url_for, request, render_template
from pytube import extract

app = Flask(__name__)
 
@app.route('/', methods=['GET'])
def home():
    return render_template('form.html')
 
@app.route('/success/<name>/<lan>')
def success(name, lan):
    return render_template('index.html', name=name, lan=lan)
 
 
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print(request.form)
        url = request.form['url']
        lan = request.form['lan']
        id=extract.video_id(url)
        return redirect(url_for('success', name=id, lan=lan))
    else:
        url = request.args.get('url')
        lan = request.args.get['lan']
        id=extract.video_id(url)
        return redirect(url_for('success', name=url, lan=lan))
 
 
if __name__ == '__main__':
    app.run(debug=True)