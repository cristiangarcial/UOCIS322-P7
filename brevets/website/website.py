from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def home():
    return render_template('index.html')


@app.route('/list')
def list():
    csv_or_json = request.args.get('csv_or_json', type=str)
    topk = str(request.args.get('topk', type=int))
    retlist = request.args.get('retOption', type=str)
    r = requests.get(f'http://restapi:5000/{retlist}/{csv_or_json}?topk={topk}')
    return r.text


 #  @app.route('/listAll')
 #   def listAll():
 #       csv_or_json = request.args.get('csv_or_json', type=str)
 #       topk= str(request.args.get('topk', type=int))
 #       r = requests.get(f'http://restapi:5000/listAll/') # {csv_or_json}?topk={topk}')
 #       return r.text

 #   @app.route('/listOpenOnly')
 #   def listOpenOnly():
 #       csv_or_json = request.args.get('csv_or_json', type=str)
 #       topk= str(request.args.get('topk', type=int))
 #       r = requests.get(f'http://restapi:5000/listOpenOnly/{csv_or_json}?topk={topk}')
 #       return r.text

 #  @app.route('/listCloseOnly')
 #   def listCloseOnly():
 #       csv_or_json = request.args.get('csv_or_json', type=str)
 #       topk= str(request.args.get('topk', type=int))
 #       r = requests.get(f'http://restapi:5000/listCloseOnly/{csv_or_json}?topk={topk}')
 #       return r.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
