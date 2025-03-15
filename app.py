from flask import Flask, render_template

app = Flask(__name__)

projects = [{
    'title': 'project 1',
    'date': '24/03/2005 - 10:55',
    'description': 'aaaa '*200,
    'creator': 'You'
}] * 10

@app.route('/')
def home():
    return render_template('index.html', projects=projects)

if __name__ == '__main__':
    app.run(debug=True)
