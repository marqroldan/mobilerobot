#! /usr/bin/python
import os
import os.path
import signal
import subprocess
import socket
import urlparse
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import movement_func as move_py
import time


#Tornado Folder Paths
settings = dict(
	template_path = os.path.join(os.path.dirname(__file__), "templates"),
	static_path = os.path.join(os.path.dirname(__file__), "static"),
	autoreload=False,
	debug=True
	)

#Tonado server port
PORT = 3500
pro = ''
last_message = "Connected"

class MainHandler(tornado.web.RequestHandler):
  def get(self):
     print ("[HTTP](MainHandler) User Connected.")
     hostname = urlparse.urlparse("%s://%s"
     % (self.request.protocol, self.request.host)).hostname
     ip_address = socket.gethostbyname(hostname)
     self.render("index.html", currIP='test', hostname=hostname, ip_address=ip_address)

	
class WSHandler(tornado.websocket.WebSocketHandler):
  connections = set()
  global last_message
  global pro

  def check_origin(self, origin):
    return True
	
  def open(self):
    self.connections.add(self)
    print '[WS] Connection was opened.'
    self.write_message("Connection opened.")
    self.write_message(last_message)
	
  def stopAuto(self):
    autoFile = open('/home/pi/masterOff.txt','w')
    autoFile.write('0')
	time.sleep(2)
    autoFile.close()
 
  def on_message(self, message):
    mg = message.split(",xyx,");
    message = mg[0];
    global last_message
    global pro
    print '[WS] Incoming message:', message
    if message == "go_forward":
      self.stopAuto()
      move_py.movement_func(1)
      last_message="I'm forwarding"
      #self.write_message("I'm forwarding")
    if message == "go_stop":
      self.stopAuto()
      move_py.movement_func(5)
      last_message="Stopping"
      #self.write_message("Stopping.")
    if message == "go_reverse":
      self.stopAuto()
      move_py.movement_func(4)
      last_message="Reversing"
      #self.write_message("Reversing")
    if message == "go_right":
      self.stopAuto()
      move_py.movement_func(3)
      last_message="Turning right"
      #self.write_message("Turning right")
    if message == "go_left":
      self.stopAuto()
      move_py.movement_func(2)
      last_message="Turning left"
      #self.write_message("Turning left")
    if message == "stop_auto":
      last_message = 'Trying to stop automatic operation.'
      self.stopAuto()
      autoFile = open('/home/pi/masterOff.txt','r')
      if(autoFile.read(1)=='0'):
        autoFile.close()
        last_message = 'Automatic operation stopped.'
      
      autoFile.close()
    if message == "pause_auto":
      autoFile = open('/home/pi/masterOff.txt','w')
      autoFile.write('2')
      autoFile.close()
      autoFile = open('/home/pi/masterOff.txt','r')
      if(autoFile.read(1)=='2'):
        autoFile.close()
        last_message = 'Automatic operation paused.'
      
      autoFile.close()
    if message == "play_auto":
      autoFile = open('/home/pi/masterOff.txt','w')
      autoFile.write('1')
      autoFile.close()
      autoFile = open('/home/pi/masterOff.txt','r')
      if(autoFile.read(1)=='1'):
        autoFile.close()
        last_message = 'Automatic operation started.'
      
      autoFile.close()
    if message == "go_auto":
      last_message = 'Attempting to start automatic process.'
      self.stopAuto()
      time.sleep(1)
      autoFile = open('/home/pi/masterOff.txt','r')
      if(autoFile.read(1)=='0'):
        autoFile.close()
      #move_py.movement_func(2)
      #print(r"sudo bython /home/pi/t21.py '{\"1\":{\"1\":\"ako\"}}' 1 2>&1")
        cmd = r"lxterminal -e sudo python3 /home/pi/t21.py "+mg[1]+r" 2>&1"
        print(cmd)
      #os.system(r"sudo bython /home/pi/ws/t21.py '{\"1\":{\"1\":\"ako\"}}' 1 2>&1")
      #p = subprocess.Popen(r"sudo bython /home/pi/t21.py '{\"1\":{\"1\":\"ako\"}}' 1 2>&1", stdout=subprocess.PIPE, shell=True)
        pro = subprocess.Popen(cmd, stdout=subprocess.PIPE, 
                            shell=True, preexec_fn=os.setsid) 
        last_message="Doing Auto"
	  
    #self.write_message(last_message)
    [con.write_message(last_message) for con in self.connections]

  def on_close(self):
    self.connections.remove(self)
    if(len(self.connections)==0):
      move_py.movement_func(5)
    print '[WS] Connection was closed.'


application = tornado.web.Application([
  (r'/', MainHandler),
  (r'/ws', WSHandler),
  ], **settings)


if __name__ == "__main__":
    try:
        http_server = tornado.httpserver.HTTPServer(application)
        http_server.listen(PORT)
        main_loop = tornado.ioloop.IOLoop.instance()

        print "Tornado Server started"
        main_loop.start()

    except Exception, e:
        print "Exception triggered - Tornado Server stopped." + str(e)
        GPIO.cleanup()

#End of Program
