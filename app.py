from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

# RSA Logic
p = 61
q = 53
n = p * q
phi = (p - 1) * (q - 1)
e = 17

def mod_inverse(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d

d = mod_inverse(e, phi)

# DB Setup
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS messages (original TEXT, encrypted TEXT)")
    conn.commit()
    conn.close()

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    encrypted = ""
    decrypted = ""

    if request.method == "POST":
        msg = int(request.form["message"])

        cipher = (msg ** e) % n
        decrypted = (cipher ** d) % n
        encrypted = cipher

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO messages VALUES (?, ?)", (msg, cipher))
        conn.commit()
        conn.close()

    return render_template("index.html", encrypted=encrypted, decrypted=decrypted)

if __name__ == "__main__":
    app.run(debug=True)