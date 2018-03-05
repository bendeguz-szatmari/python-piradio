import vlc
from time import sleep
import requests
from collections import namedtuple
import os, csv, threading
from subprocess import Popen, PIPE

class StreamManager:
    """

    """
    play = False
    playlists = set(['pls','m3u'])
    Stream = namedtuple('Stream', 'name url')
    radio_csv = os.path.dirname(os.path.abspath(__file__)) + "/radios.csv"

    #urls = [
    #    Stream('Kék Duna','http://stream1.kekduna.hu:8006/;stream'),
    #    Stream('MR2 Petőfi','http://stream001.radio.hu:8080/mr2.m3u')
    #]
    urls = []

    def __init__(self):
        self.read_radios()
        self.__current_id = 0
        self.__current_stream = StreamManager.urls[self.__current_id]
        self.__list = False
        #define VLC instance
        self.__instance = vlc.Instance('--input-repeat=-1', '--fullscreen')

        #Define VLC player
        self.__player=self.__instance.media_player_new()
        #Used if url is a playlist
        self.__list_player=self.__instance.media_list_player_new()
        self.thread = threading.Thread()

    def read_radios(self):
        with open(StreamManager.radio_csv, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                print(', '.join(row))
                StreamManager.urls.append(StreamManager.Stream(row[0], row[1]))
    
    def write_new_radio(self, name="", url=""):
        StreamManager.urls.append(StreamManager.Stream(name, url))
        with open(StreamManager.radio_csv, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow([name, url])

    def select_stream(self, next=True):
        if next == True:
            self.__current_id = self.__current_id + 1
            if self.__current_id >= len(StreamManager.urls):
                self.__current_id = 0
        else:
            self.__current_id = self.__current_id -1
            if self.__current_id < 0:
                self.__current_id = ( len(StreamManager.urls) - 1 )
        self.__current_stream = StreamManager.urls[self.__current_id]
        print(self.__current_stream.name)
        if StreamManager.play == True:
            self.play_stream()

    def play_stream(self):
        #Play the media
        if self.check_stream_online(self.__current_stream.url) == True:
            ext = (self.__current_stream.url.rpartition(".")[2])[:3]
            result = StreamManager.playlists.__contains__(ext)
            if self.thread.is_alive() == True:
                print("thread is running")
                self.stop_stream()
            self.thread = threading.Thread(target=self.start_stream, args=[result])
            self.thread.start()
        else:
            print ("Stream offline:" +self.__current_stream.name)

    def start_stream(self,List=False):
        if List == True:
            self.__list = True
            self.__list_media=self.__instance.media_list_new([self.__current_stream.url])
            self.__list_player.set_media_list(self.__list_media)
            self.__list_player.play()
        else:
            self.__media=self.__instance.media_new(self.__current_stream.url)
            self.__player.set_media(self.__media)
            self.__player.play()
        StreamManager.play = True
        while getattr(self.thread,"do_run", True):
            sleep(1)

    def check_stream_online(self, url=''):
        test_pass = False    
        try:
            if url[:4] == 'file':
                test_pass = True
            else:
                r = requests.get(url, stream=True)
                test_pass = r.ok
        except Exception as e:
            print('failed to get stream: {e}'.format(e=e))
            test_pass = False
        return test_pass
    
    def stop_stream(self):
        StreamManager.play = False
        self.thread.do_run = False
        if self.__list == True:
            print('stopping list media')
            self.__list_player.stop()
            while self.__list_player.is_playing() != 0:
                sleep(1)
        else:
            print('stopping media')
            self.__player.stop()
            while self.__player.is_playing() != 0:
                sleep(1)
        self.__list = False
        if self.thread.is_alive() == True:
            self.thread.join()

    def get_current_radio(self):
        return self.__current_stream.name

    def get_current_url(self):
        return self.__current_stream.url
    
    def get_status(self):
        return StreamManager.play

    def modify_volume(self, value):
        if value < 0:
            amount = str(abs(value))+'%-'
        else:
            amount = str(value)+'%+'
        ##  run 'amixer' as a subprocess, then pipe the output
        card = Popen(['amixer', 'sset', 'Master', amount], stdout=PIPE)

        out = card.communicate()[0]  ##  we only need the first element returned
        vol = str(out).split('[')[1].split(']')[0]
        print(vol)
        return vol

    def get_volume(self):
        card = Popen(['amixer', 'sget', 'Master'], stdout=PIPE)

        out = card.communicate()[0]  ##  we only need the first element returned
        vol = str(out).split('[')[1].split(']')[0]

        return vol


if __name__ == "__main__":
    sm = StreamManager()
    sm.play_stream()
    sleep(5)
    sm.stop_stream()

        


