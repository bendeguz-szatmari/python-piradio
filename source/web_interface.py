from stream_manager import StreamManager

sm = StreamManager()

from flask import Flask, request, render_template, jsonify
import json
app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def radio_control():
    if request.method == 'POST':
        data = request.get_json()
        if data['submit'] == 'Play':
            print('play')
            sm.play_stream()
            print(sm.get_current_radio())
            print(sm.get_current_url())
            print(sm.check_stream_online(sm.get_current_url()))
        elif data['submit'] == 'Stop':
            print('stop')
            sm.stop_stream()
        if data['submit'] == 'Previous':
            print('previous')
            sm.stop_stream()
            sm.select_stream(False)
            sm.play_stream()
        elif data['submit'] == 'Next':
            print('next')
            sm.stop_stream()
            sm.select_stream()
            sm.play_stream()
        elif data['submit'] == 'Increase':
            print('increase volume')
            sm.modify_volume(10)
        elif data['submit'] == 'Decrease':
            print('decrease volume')
            sm.modify_volume(-10)
        else:
            print("unknown button pressed")
            pass # unknown
    elif request.method == 'GET':
        print('get')
        dict = {}
        dict['status'] = str(sm.get_status)
        data = json.dumps(dict)
    return jsonify(data)

@app.route('/add', methods=['GET', 'POST'])
def radio_add():
    if request.method == 'POST':
        data = request.get_json()
        sm.write_new_radio(data['name'], data['url'])
    return jsonify(data)

if __name__ == '__main__':
   app.run()
