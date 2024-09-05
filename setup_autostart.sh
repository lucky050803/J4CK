#!/bin/bash

# Variables
PYTHON_SCRIPT_PATH="/home/pi/mon_script.py"
REQUIREMENTS_FILE="/home/pi/requirements.txt"
SERVICE_FILE="/etc/systemd/system/python-autostart.service"

# Vérifier si le script Python existe
if [ ! -f "$PYTHON_SCRIPT_PATH" ]; then
    echo "Le script Python $PYTHON_SCRIPT_PATH n'existe pas."
    exit 1
fi

# Vérifier si le fichier requirements.txt existe et installer les dépendances
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installation des bibliothèques Python à partir de $REQUIREMENTS_FILE..."
    sudo pip3 install -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        echo "Erreur lors de l'installation des dépendances."
        exit 1
    fi
else
    echo "Aucun fichier requirements.txt trouvé. Ignorer l'installation des dépendances."
fi

# Créer un service systemd pour exécuter le script Python au démarrage
echo "Création du fichier de service systemd..."

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Script Python AutoStart
After=network.target

[Service]
ExecStart=/usr/bin/python3 $PYTHON_SCRIPT_PATH
WorkingDirectory=/home/pi/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
EOL

# Rendre le fichier exécutable
sudo chmod 644 $SERVICE_FILE

# Recharger systemd pour prendre en compte le nouveau service
echo "Rechargement de systemd..."
sudo systemctl daemon-reload

# Activer le service pour qu'il démarre automatiquement au démarrage
echo "Activation du service..."
sudo systemctl enable python-autostart.service

# Démarrer le service immédiatement
echo "Démarrage du service..."
sudo systemctl start python-autostart.service

echo "Le script Python sera désormais exécuté automatiquement au démarrage."
