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
    ret = {}
    if request.method == 'POST':
        data = request.get_json()
        if data['submit'] == 'Play':
            print('play')
            sm.play_stream()
            print(sm.get_current_radio())
            ret['response'] = sm.get_current_radio()
        elif data['submit'] == 'Stop':
            print('stop')
            sm.stop_stream()
            ret['response'] = sm.get_current_radio()
        if data['submit'] == 'Previous':
            print('previous')
            sm.select_stream(False)
            ret['response'] = sm.get_current_radio()
        elif data['submit'] == 'Next':
            print('next')
            sm.select_stream()
            ret['response'] = sm.get_current_radio()
        elif data['submit'] == 'Increase':
            print('increase volume')
            ret['response'] = sm.modify_volume(10)
        elif data['submit'] == 'Decrease':
            print('decrease volume')
            ret['response'] = sm.modify_volume(-10)
        elif data['submit'] == 'Status':
            print('get status')
            ret['response'] = str(sm.get_status())
            ret['response2'] = str(sm.get_current_radio())
        elif data['submit'] == 'Volume':
            print('get volume')
            ret['response'] = str(sm.get_volume())
        elif data['submit'] == 'Add':
            print('add new radio')
            ret['response'] = sm.write_new_radio(data['name'], data['url'])
            ret['response'] = sm.get_current_radio()
        else:
            print("unknown button pressed")
            pass # unknown
    elif request.method == 'GET':
        print('get')
        ret['response'] = str(sm.get_status())
    data = json.dumps(ret)
    return jsonify(data)

@app.route('/add', methods=['GET', 'POST'])
def radio_add():
    if request.method == 'POST':
        data = request.get_json()
        sm.write_new_radio(data['name'], data['url'])
    return jsonify(data)

if __name__ == '__main__':
   app.run()
