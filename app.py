from flask import Flask, request, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from werkzeug.datastructures import ImmutableMultiDict

#from flask.ext.api.parsers import MultiPartParser

app = Flask(__name__)

app.config.update(
    # SECRET_KEY='postgres',
    # SQLALCHEMY_DATABASE_URI='<database>://<user_id>:<password>@<server>/<database_name>',
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:postgres@localhost/facconsole',
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)

db = SQLAlchemy(app)

@app.route('/index')
@app.route('/')
def hello_world():
    return 'index route'


@app.route('/new/')
def query_strings():
    query_val = request.args.get('greeting')
    return '<h1> the greeting is : {0} </h1>'.format(query_val)

@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        head = dict(request.headers)
        data = dict(request.form)
        print(head)
        print(data)

        print('Content-Type:', head['Content-Type'])
        print('Authorization: ', head['Authorization'])
        print('User-Agent: ', head['User-Agent'])
        print('Host: ', head['Host'])
        print('Content-Length: ', head['Content-Length'])
        print('subject:', trim_all(data['subject']))
        print('comments:', trim_all(data['comments']))
        print('numberOfFiles:', trim_all(data['numberOfFiles']))
        print('file1:', trim_all(data['file1']))
        print('file2:', trim_all(data['file2']))
        return Response('Uploaded file successfully', status=200)

        #res = '200'
        #return res
        #f = request.files['the_file']
        #f.save('C:/Users/Frank/files/uploaded_file.txt')


# display (localhost:5000/check_server)
@app.route('/check_server')
def check_server_status(name='Flask'):
    #query_val = request.args.get('greeting')
    return '<h1> The {} server is up on localhost!</h1>'.format(name)


# display (localhost:5000/user/Frank)
@app.route('/user')
@app.route('/user/<name>')
def no_query_strings(name='frank'):
    query_val = request.args.get('greeting')
    return '<h1> hello there ! {} </h1>'.format(name)

# STRINGS (localhost:5000/test/hello there)
@app.route('/test/<string:name>')
def working_with_strings(name):
    return '<h1> here is a string: ' + name + '</h1>'

# NUMBERS (localhost:5000/numbers/58)
@app.route('/numbers/<int:num>')
def working_with_numbers(num):
    return '<h1> the number you picked is: ' + str(num) + '</h1>'

# ADDING NUMBERS (localhost:5000/add/58/59)
@app.route('/add/<int:num1>/<int:num2>')
def adding_integers(num1, num2):
    return '<h1> the sum is : {}'.format(num1 + num2) + '</h1>'

# FLOATS (localhost:5000/product/58.1/2.3)
@app.route('/product/<float:num1>/<float:num2>')
def product_two_numbers(num1, num2):
    return '<h1> the product is : {}'.format(num1 * num2) + '</h1>'


# USING TEMPLATES (localhost:5000/temp)
@app.route('/temp')
def using_templates():
    return render_template('hello.html')

# USING JINJA2 TEMPLATES - SAMPLE CODE (localhost:5000/temp)
@app.route('/watch')
def movies_2017():
    movie_list = ['Autopsy of Jane Doe',
                  'Neon Angel',
                  'Ghost in a Shell',
                  'John Wick 2',
                  'Spiderman - Homecoming'
    ]

    return render_template('movies.html',
                           movies = movie_list,
                           name='Frank')


class Publication(db.Model):
    __tablename__ = 'publication'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return 'The id is {}, Name is {}'.format(self.id, self.name)


class Trequest(db.Model):
    __tablename__ = 'trequest'

    id = db.Column(db.Integer, primary_key=True)
    postingapp = db.Column(db.Integer, nullable=False)
    postingapp_name = db.Column(db.String(128), nullable=False)
    auth_type = db.Column(db.String(64), nullable=False)
    remote_addr = db.Column(db.String(15), nullable=False)
    remote_host = db.Column(db.String(128), nullable=False)
    remote_user = db.Column(db.String(64), nullable=False)
    content_type = db.Column(db.String(128), nullable=False)
    sender_ident = db.Column(db.String(64), nullable=False)
    content_length = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(1), nullable=False)
    error_msg = db.Column(db.String(1024), nullable=False)
    change_ts = db.Column(db.DateTime, default=datetime.utcnow())
    uw_case_id = db.Column(db.String(20), nullable=True)

    def __init__(self, id, postingapp, postingapp_name, auth_type, remote_addr, remote_host,
                 remote_user, content_type, sender_ident, content_length, status, error_msg,
                 change_ts, uw_case_id):
        self.id = id
        self.postingapp = postingapp
        self.postingapp_name = postingapp_name
        self.auth_type = auth_type
        self.remote_addr = remote_addr
        self.remote_host = remote_host
        self.remote_user = remote_user
        self.content_type = content_type
        self.sender_ident = sender_ident
        self.content_length = content_length
        self.status = status
        self.error_msg = error_msg
        self.change_ts = change_ts
        self.uw_case_id = uw_case_id

    def __repr__(self):
        return 'The id is {}, posting appl is {}'.format(self.id, self.postingapp)

def trim_all(raw_data):
    return str(raw_data).replace('[','').replace(']','')

if __name__ == '__main__':
    #db.create_all()
    app.run(debug=True)
