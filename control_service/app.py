from flask import Flask
from webServices.register import register


app = Flask(__name__)
app.register_blueprint(register)


if __name__ == '__main__':
    app.run(debug=True)