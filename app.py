from flask import Flask, render_template
app = Flask(__name__)

posts = [
    {
        'author' : 'Joe Vitko',
        'title' : 'Post 1',
        'content' : 'First post content',
        'date_posted' : 'April 20 2018'
    },
    {
        'author' : 'Joe Vitko',
        'title' : 'Post 2',
        'content' : 'Second post content',
        'date_posted' : 'April 21 2018'
    }

]

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html', posts=posts)

@app.route('/about')
def cakes():
    return render_template('about.html', title='About')

@app.route('/hello/<name>')
def hello(name):
    return render_template('page.html', name=name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

