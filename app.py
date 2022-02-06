from flask import Flask,render_template,url_for,request,redirect,flash


app = Flask(__name__)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/', subdomain ='api')
def courses():
    return "Courses listed " \
           "under practice subdomain."

if __name__ == '__main__':
    # website_url = 'vibhu.gfg:5000'
    # app.config['SERVER_NAME'] = website_url
    app.run(debug=True)