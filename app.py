from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '𝐇𝐞𝐥𝐥𝐨 𝐟𝐫𝐨𝐦 𝐀𝐉 𝐓𝐄𝐂𝐇 𝐖𝐎𝐑𝐋𝐃'


if __name__ == "__main__":
    app.run()
