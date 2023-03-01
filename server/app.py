from flask import Flask

app = Flask(__name__)


@app.route('/')
def home():
    return


@app.route('/drivers')
def driver():
    return

@app.route('/customers')
def customer():
    return

@app.route('/buses')
def bus():
    return

@app.route('/routes')
def route():
    return



if __name__ == "__main__":
    app.run(debug=True)