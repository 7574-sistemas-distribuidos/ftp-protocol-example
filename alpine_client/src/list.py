#!/usr/bin/env python3
import socket
import sys
import os
import time
import re

HOST = os.environ["FTP_HOST"]
PORT = int(os.environ["FTP_PORT"])
NAME = os.environ["NAME"]
PASS = os.environ["PASS"]

def send_text(s, text):
  print('[CLIENT] Sending: {}'.format(text))
  s.sendall('{}\r\n'.format(text).encode())

def receive_data(s):
  buff = bytearray()
  data = s.recv(1024)
  while data and len(data) > 0:
    buff.extend(data)
    data = s.recv(1024)
  print('[DATA] Received: {}'.format(buff))
  return buff

def receive_text(s):
  buff = bytearray()
  text = None
  while text is None:
    data = s.recv(1024)
    if data and len(data) > 0:
      buff.extend(data)
      if buff.decode(errors='ignore').find('\r\n') >= 0:
        text = buff.decode()
  print('[CLIENT] Received: {}'.format(text))
  return text

def check_ok(text, code):
  if not text.startswith(str(code)):
    raise Exception('Response code not OK. Expected: {}. Text Received: {}'.format(code, text))

def parse_port(response):
  m = re.search('^.*\(\d+,\d+,\d+,\d+,(\d+),(\d+)\).*$', response)
  if m is None or len(m.groups()) != 2:
    raise Exception('Response to PASV does not include connection port. Text Received: {}. {}'.format(response, m))
  return int(m.group(1))*256 + int(m.group(2))

def do_list_sequence(s, ip, list_cmd):
    send_text(s, 'PASV')
    response = receive_text(s)
    check_ok(response, 227)
    passive_port = parse_port(response)
    print('Passive port: {}'.format(passive_port))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s_data:
      send_text(s, list_cmd)
      s_data.connect((ip, passive_port))
      print('[DATA] Socket connected')
      response = receive_text(s)
      response_data = receive_data(s_data)
      check_ok(response, 150)
      response = receive_text(s)
      check_ok(response, 226)

def main():
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      print('[CLIENT] Socket created')
      ip = socket.gethostbyname(HOST)
      s.connect((ip, PORT))
      print('[CLIENT] Socket connected')
      response = receive_text(s)
      check_ok(response, 220)
      send_text(s, 'USER {}'.format(NAME))
      response = receive_text(s)
      check_ok(response, 331)
      send_text(s, 'PASS {}'.format(PASS))
      response = receive_text(s)
      check_ok(response, 230)

      do_list_sequence(s, ip, 'LIST')
      do_list_sequence(s, ip, 'LIST /home')
      do_list_sequence(s, ip, 'LIST /home/user1')
  except Exception as e:
    print('[CLIENT] Error detected. Error: {}'.format(e))

if __name__ == '__main__':
  main()	
