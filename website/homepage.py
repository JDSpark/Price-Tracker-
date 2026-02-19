from flask import Flask, render_template
app = Flask(__name__)

posts = [
    {
        'author' : 'JDSpark',
        'title' : 'Post 1',
        'content' : 'Test 1 ',
        'date_posted' : 'test 1 date '
    },
    {
        'author' : 'JDSparky',
        'title' : 'Post 2',
        'content' : 'test 2',
        'date_posted' : 'test 2 date'
    },
]

@app.route("/")
def home_page():
    return render_template('home.html', posts=posts)

@app.route("/about")
def about():
    return render_template('about.html', title='About')