from stream_manager import StreamManager

sm = StreamManager()

from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
header = '''
<!doctype html>
'''
control_buttons = '''    
    <form action="/" method="post">
        <input type="submit" name="submit" value="Play">
        <input type="submit" name="submit" value="Previous">
        <input type="submit" name="submit" value="Next">
        <input type="submit" name="submit" value="Stop">
    </form>
    '''
add_url = '''
    <form action="/add" method="post">
        <input type="text" name="name" value="Radio">
        <input type="text" name="url" value="URL">
        <input type="submit" name="submit" value="Add URL">
    </form>
    '''
current_radio = ''
#return_string = header + control_buttons + add_url

def return_string(act_radio=''):
    current_radio = act_radio
    playing = '''
    Current radio: ''' + current_radio + '''
    '''
    #return header + playing + control_buttons + add_url
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/control', methods=['POST'])
def radio_control():
    if request.method == 'POST':
        print('Post')
        print(request)
        print(request.get_json())
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
        else:
            print("unknown button pressed")
            pass # unknown
    elif request.method == 'GET':
        print('get')
    return jsonify(data)

@app.route('/add', methods=['GET', 'POST'])
def radio_add():
    if request.method == 'POST':
        print('Post')
        print(request.form['name'])
        print(request.form['url'])
        sm.write_new_radio(request.form['name'], request.form['url'])
    return return_string(sm.get_current_radio())

if __name__ == '__main__':
   app.run()
