import json
import hashlib
import requests
import string
from ast import literal_eval

# GET
api_request = requests.get(
    "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=83120580e8345110f3883b44187151cc8abdd46f")
raw_data = api_request.content
arq = raw_data.decode()

# grava json
# gravar JSON da API localmente
with open("answer.json", "w") as myfile:
    new_arq = myfile.write(arq)
    myfile.close()
d = literal_eval(arq)

# JSON
casas = d["numero_casas"]
cifrado = d['cifrado']
hashed = d["resumo_criptografico"]
alfabeto = string.ascii_lowercase
print(alfabeto)

#decifrar mensagem
def decrypt(cif):
    decif = ""
    for c in cif:
        if c in alfabeto:
            c_index = alfabeto.index(c)
            decif += alfabeto[(c_index - casas) % len(alfabeto)]
        else:
            decif += c
    return decif

decif = decrypt(cifrado)

# hash da mensagem decifrada
rcript = decif
hashcript = rcript.encode(encoding='ascii')
hashed = hashlib.sha1(hashcript)
final_obj = hashed.hexdigest()
print(final_obj)

# remover key vazia
d.pop('Decifrado', None)

# adicionar key
d['decifrado'] = decif

# inserir sha1 no JSON
d.pop('resumo_criptografico', None)
d['resumo_criptografico'] = final_obj

with open("answer.json", "w") as final:
    json.dump(d, final)

print(d)
print(final)

files = {'answer': (open('answer.json', 'r'))}

print(files)

url = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=83120580e8345110f3883b44187151cc8abdd46f"
headers = {'Accept': 'application/json'}
response = requests.post(url, files=files, headers=headers)

print(response.status_code)
print(response.text)
