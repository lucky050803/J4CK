from flask import Flask, render_template, request, redirect, url_for, session
import time

app = Flask(__name__)

# Mot de passe défini
PASSWORD = "oui"
# Dictionnaire pour stocker le nombre de tentatives échouées par IP
failed_attempts = {}
# Dictionnaire pour bloquer les IP temporairement
blocked_ips = {}
auth_ips = {}
# Durée du blocage en secondes (5 minutes)
BLOCK_TIME = 300

@app.route('/', methods=['GET', 'POST'])
def login():
    ip_address = request.remote_addr

    # Vérifier si l'IP est bloquée
    if ip_address in blocked_ips:
        if time.time() - blocked_ips[ip_address] < BLOCK_TIME:
            return f"Accès bloqué pour {BLOCK_TIME / 60} minutes."
        else:
            # Débloquer après le temps écoulé
            del blocked_ips[ip_address]
    
    if request.method == 'POST':
        password = request.form['password']
        
        # Vérifier si le mot de passe est correct
        if password == PASSWORD:
            # Réinitialiser les tentatives échouées
            failed_attempts[ip_address] = 0
            return redirect(url_for('home'))
        else:
            # Incrémenter les tentatives échouées
            if ip_address not in failed_attempts:
                failed_attempts[ip_address] = 0
            failed_attempts[ip_address] += 1

            # Vérifier si 3 tentatives échouées ont été atteintes
            if failed_attempts[ip_address] >= 3:
                blocked_ips[ip_address] = time.time()
                return f"Accès bloqué pour {BLOCK_TIME / 60} minutes."

            return f"Mot de passe incorrect. Tentative {failed_attempts[ip_address]}/3"
    
    return render_template('index.html')


@app.route('/home', methods=['GET', 'POST'])
def home(): 
    response = ''
    if request.method == 'POST' and 'phrase' in request.form:
        phrase = request.form['phrase']
        # Logique de réponse
        if phrase == "OK":
            response = "elle a la degaine"
        else:
            response = phrase
    return render_template('home.html', response=response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
