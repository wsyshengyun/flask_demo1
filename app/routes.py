from flask import render_template
from app import app 


@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Migue'}
    posts = [ 
            {
                'author':{'username':'John'}, 
                'body':'Beautiful day in Portland!'
            },
            {
                'author':{'username':'Susan'}, 
                'body':'The Avengers movie was so cool!'
            }
    ]
    title = "Home"
    return render_template('index.html', user=user
    , title=title
    , posts = posts
    )

