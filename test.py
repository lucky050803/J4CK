import re

def extract_ips(text):
    # Expression régulière pour reconnaître les adresses IP (IPv4)
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    
    # Rechercher toutes les correspondances d'adresses IP dans le texte
    ips = re.findall(ip_pattern, text)
    
    # Filtrer les adresses IP valides (0-255)
    valid_ips = [ip for ip in ips if all(0 <= int(octet) <= 255 for octet in ip.split('.'))]
    
    return valid_ips

# Exemple d'utilisation
user_input = input("Entrez du texte avec des adresses IP : ")
found_ips = extract_ips(user_input)

if found_ips:
    print("Adresses IP trouvées :", found_ips)
else:
    print("Aucune adresse IP valide trouvée.")
