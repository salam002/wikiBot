from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def home():
  return "Hello. I am alive!"


def run():
  app.run('0.0.0.0', port=8080)


def keep_alive():
  t = Thread(target=run)
  t.start()


# server runs on separate thread from our bot so they can run at the same time