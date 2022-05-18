from Crypto import Random
from Crypto.Cipher import AES
import random
import math
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_c
from Crypto.Signature import PKCS1_v1_5 as PKCS1_signature
from Crypto.Cipher import DES3
from Crypto.Util import Padding
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA224
from Crypto.Hash import SHA256
import sys
import base64


#funkcija za zapisivanje u datoteku (s potrebnim tagovima)
def write_to_file(filename, alg, key, descrip = "Secret key"):
	key = adjust(key.hex())
	with open(filename, 'w') as f:
		f.write(
'''---BEGIN OS2 CRYPTO DATA---
Description:
    {descrip}
Method:
    {alg}
Secret key:
{key}
---END OS2 CRYPTO DATA--- 
	'''.format(descrip = descrip, alg = alg, key = key))

#pretvaranje int vrijednost u hex vrijednost
def int_to_hex_pad(number):	#padded
    repr = hex(number)[2:]
    near_e_2 = 1
    while (near_e_2 < len(repr)):
        near_e_2 *= 2
    if (near_e_2 != len(repr)):
        repr = '0' * (near_e_2-len(repr)) + repr
    return repr 		#representation

#funkcija za zapisivanje ključa u datoteku (uz potrebne tagove)
def rsa_write_key_to_file(public, filename, pub_key, key_size, descr):
	if(public):
		output_file = 'public'+'_'+filename
		repr_prefix = 'Public '
	if(public is False):
		output_file = 'private'+'_'+filename
		repr_prefix = 'Private '
	len_of_key = int_to_hex_pad(key_size)

	mod_rep = adjust(hex(pub_key.n))[2:]
	exp_rep = ""
	if(public):
		exp_rep = adjust(hex(pub_key.e)[2:])
	if(public is False):
		exp_rep = adjust(hex(pub_key.d)[2:])

	with open(filename, 'w') as f:
		f.write('''---BEGIN OS2 CRYPTO DATA---
Description:
    {description}
Method:
    RSA
Key length:
    {key_length}
Modulus:
  {mod_rep}
{repr_prefix}exponent:
{exp_repr}
---END OS2 CRYPTO DATA---
'''.format(description=descr, key_length=len_of_key, mod_rep=mod_rep,
           repr_prefix=repr_prefix, exp_repr=exp_rep))

#razdvajanje na blokove
def piece(list, n):
	res = []
	l = len(list)
	for i in range(0, math.floor(l/n + 1)):
		if(i*n == l):
			break
		if((i + 1)*n <= l):
			res.append(list[i * n : (i + 1)*n])
		else:
			res.append(list[i*n:])
	return res

#prikaz stringa
def adjust(str):
	return '\n'.join(['    ' + i for i in piece(str, 60)]) #60 = najveca moguca duljina linije

#funkcija za upisivanje u datoteku iz omotnice (uz potrebne tagove)
def from_envelope_to_file(in_filename, out_filename, sym_alg, asym_alg, sym_key_len, asym_key_len, data,
                     sym_key):
    data = adjust(base64.b64encode(data).decode('utf-8'))
    sym_key = adjust(sym_key.hex())
    with open(out_filename, 'w') as f:
        f.write('''---BEGIN OS2 CRYPTO DATA---
Description:
    Envelope
File name:
    {in_filename}
Method:
    {sym_alg}
    {asym_alg}
Key length:
    {sym_key_len}
    {asym_key_len}
Envelope data:
{data}
Envelope crypt key:
{sym_key}
---END OS2 CRYPTO DATA---
'''.format(in_filename=in_filename, sym_alg=sym_alg, asym_alg=asym_alg,
                   sym_key_len=int_to_hex_pad(sym_key_len), asym_key_len=int_to_hex_pad(asym_key_len),
                   data=data, sym_key=sym_key))

#funkcija za upisivanje u datoteku iz potpisa (uz potrebne tagove)
def from_signature_to_file(in_filename, out_filename, hash, asym_alg, hash_len, asym_key_len,signature):
    signature = adjust(signature.hex())
    with open(out_filename, 'w') as f:
        f.write('''---BEGIN OS2 CRYPTO DATA---
Description:
    Signature
File name:
    {in_filename}
Method:
    {hash}
    {asym_alg}
Key length:
    {hash_len}
    {asym_key_len}
Signature:
{signature}
---END OS2 CRYPTO DATA---
'''.format(in_filename=in_filename, hash=hash,asym_alg=asym_alg,
           hash_len=int_to_hex_pad(hash_len), asym_key_len=int_to_hex_pad(asym_key_len), signature=signature))

#razred AEScrypto - kriptiranje algoritmom AES
class AEScrypto:
	def __init__(self):
		self.name = 'AES'
		self.modes = {
		'CBC' : AES.MODE_CBC,
		'OFB' : AES.MODE_OFB
		}
		self.key_sizes = {'128' : 16, '192' : 24, '256': 32}

	def init_aes(self, mode, key_size, crypto_file = 'aes.txt'):
		self.mode = self.modes[mode]
		self.key_size = self.key_sizes[key_size]
		self.key = Random.new().read(self.key_size)
		self.block_size = AES.block_size
		self.iv = Random.new().read(self.block_size)
		self.cypher = AES.new(self.key, self.mode, self.iv)

		write_to_file(crypto_file, self.name, self.key)

	def encrypt(self, input):
		input = Padding.pad(input, self.block_size)
		output = b''
		l = len(input)
			
		for i in range(math.floor(l / self.block_size)):
			output += self.cypher.encrypt(input[i * self.block_size:(i + 1) * self.block_size])
		return output

	def decrypt(self, text):
		decription_output = b''
		l = len(text)
		for i in range(math.floor(l / self.block_size)):
			decription_output += self.cypher.decrypt(text[i * self.block_size:(i + 1) * self.block_size])
		return Padding.unpad(decription_output, self.block_size)

	def copy(self):
		obj = AEScrypto()
		obj.mode = self.mode
		obj.key_size = self.key_size
		obj.key = self.key
		obj.block_size = AES.block_size
		obj.iv = self.iv
		obj.cypher = AES.new(obj.key, obj.mode, obj.iv)
		return obj

#Razred DES3crypto - kriptiranje algoritmom DES3
class DES3crypto:
	def __init__(self):
		self.name = 'DES3'
		self.modes = {
		'CBC' : DES3.MODE_CBC,
		'OFB' : DES3.MODE_OFB
		}
		self.key_sizes = {'16': 16, '24': 24}

	def init_des3(self, mode, key_size, crypto_file = 'des3.txt'):
		self.mode = self.modes[mode]
		self.key_size = self.key_size[key_size]

		self.key = Random.new().read(self.key_size)
		self.block_size = DES3.block_size
		self.iv = Random.new.read(self.block_size)
		self.cypher = DES3.new(self.key, self.mode, self.iv)

		write_to_file(crypto_file, self.name, self.key)

	def encrypt(self, input):
		input = Padding.pad(input, self.block_size)
		output = b''
		l = len(input)
		for i in range(math.floor(l / self.block_size)):
			output += self.cypher.encryption(input[i * self.block_size:(i + 1) * self.block_size])
		return output

	def decrypt(self, text):
		decription_output = b''
		l = len(text)
		for i in range(math.floor(l / self.block_size)):
			decription_output += self.cypher.decryption(text[i * self.block_size:(i + 1) * self.block_size])
		return Padding.unpad(decription_output, self.block_size)

	def copy(self):
		obj = DES3crypto()
		obj.mode = self.mode
		obj.key_size = self.key_size
		obj.key = self.key
		obj,block_size = DES3.block_size
		obj.iv = self.iv
		obj.cypher = DES3.new(obj.key, obj.mode, obj.iv)
		return obj

#Razred RSAcrypto - kriptiranje algoritmom RSA
class RSAcrypto:
	def __init__(self):
		self.name = 'RSA'
		self.key_sizes = {'1024' : 1024, '2048' : 2048, '4096' : 4096}

	def init_rsa(self, key_size, crypto_file = 'rsa.txt'):
		self.key_size = self.key_sizes[key_size]
		self.private_key = RSA.generate(self.key_size)
		self.public_key = self.private_key.publickey()

		rsa_write_key_to_file(True, 'pub_'+crypto_file, self.public_key, self.key_size, descr = 'Public key')
		rsa_write_key_to_file(False, 'priv_'+crypto_file, self.private_key, self.key_size, descr = 'Private key')

		self.sign_key = PKCS1_signature.new(self.private_key)
		self.verify_key = PKCS1_signature.new(self.public_key)
		self.private_key = PKCS1_c.new(self.private_key)
		self.public_key = PKCS1_c.new(self.public_key)

	def encrypt(self, input):
		return self.public_key.encrypt(input)

	def decrypt(self, text):
		sentin = Random.new().read(20 + len(text))
		return self.private_key.decrypt(text, sentin)

	def sign(self, digest):
		return self.sign_key.sign(digest)

	def verify(self, digest, signature):
		return self.verify_key.verify(digest, signature)

#Razred SHAcrypto - kriptiranje algoritmom SHA
class SHAcrypto:
	def __init__(self):
		self.types = {
		'SHA224': (SHA224, 224),
		'SHA256': (SHA256, 256)
		}

	def initSHA(self, type):
		self.name = type
		self.type, self.digest_len = self.types[type]
		self.obj = self.type.new()
		self.digest_size = self.obj.digest_size

	def update(self, input):
		self.obj.update(input)

	def digest(self, input):
		self.update(input)

	def copy(self):
		h = SHAcrypto()
		h.initSHA(self.name)
		return h

#funkcija koja pokreće cijeli program
#program je moguće pokrenuti na dva načina:
# 1. tako da se kao argument prilikom poziva programa preda 1 => potrebno ručno odabrati parametre
# 2. tako da se kao argument prilikom poziva programa preda 2 => program se pokreće s podacima:
# kriptira se simetričnim kriptosustavom AES, veličine ključa 128 bita, u CBC modu.
# Veličina ključa pošiljatelja je 1024 bita kriptirana algoritmom RSA, dok je veličina ključa
# primatelja također 1024 bita (algoritam RSA)
# Kao hash algoritam odabran je SHA224.
def run_app():
	if(sys.argv[1] == str(1)):
		input_file = "input_dat.txt"
		print("Odaberite algoritam za simetrično kriptiranje\n1 AES\n2 DES3")
		a = input("-> ")
		cypher = None
		if(a == '1'):
			cypher = AEScrypto()
			print("Odaberite veličinu ključa:\n1 128\n2 192\n3 256")
			c = input("-> ")
			if(c == '1'):
				key_size = '128'
			if(c == '2'):
				key_size = '192'
			if(c == '3'):
				key_size = '256'
		if(a == '2'):
			cypher = DES3crypto()
			print("Odaberite veličinu ključa:\n1 16\n2 24")
			c = input("-> ")
			if(c == '1'):
				key_size = '16'
			if(c == '2'):
				key_size = '24'
		print("Odaberite način rada algoritma:\n1 CBC\n2 OFB")	
		b = input("-> ")
		mode = None
		if(b == '1' and a == '1'):
			mode = 'CBC'
		if(b == '1' and a == '2'):
			mode = 'OFB'
		if(b == '2' and a == '1'):
			mode = 'CBC'
		if(b == '2' and a == '2'):
			mode = 'OFB'

		if(a == '1'):
			cypher.init_aes(mode = mode, key_size = key_size)
			session_key = cypher
		if(a == '2'):
			cypher.init_des3(mode = mode, key_size = key_size)
			session_key = cypher

		print("Odaberite veličinu ključa pošiljatelja:\n1 1024\n2 2048\n3 4096")
		d = input("-> ")
		if(d == '1'):
			key_size = '1024'
		if(d == '2'):
			key_size = '2048'
		if(d == '3'):
			key_size = '4096'
		sk = RSAcrypto()
		sk.init_rsa(key_size = key_size, crypto_file = "sender.txt")
		sender_key = sk


		print("Odaberite veličinu ključa primatelja:\n1 1024\n2 2048\n3 4096")
		e = input("-> ")
		if(d == '1'):
			key_size = '1024'
		if(d == '2'):
			key_size = '2048'
		if(d == '3'):
			key_size = '4096'
		rk = RSAcrypto()
		rk.init_rsa(key_size = key_size, crypto_file = 'reciever.txt')
		reciever_key = rk


		print("Odaberite hash algoritam\n1 SHA224\n2 SHA256")
		f = input("->" )
		if(f == '1'):
			h = SHAcrypto()
			h.initSHA(type = 'SHA224')
		if(f == '2'):
			h = SHAcrypto()
			h.initSHA(types = 'SHA256')

	if(sys.argv[1] == str(2)):
		input_file = "input_dat.txt"

		cypher = AEScrypto()
		key_size = '128'
		mode = 'CBC'
		cypher.init_aes(mode = mode, key_size = key_size)
		session_key = cypher

		#veličina ključa pošiljatelja
		key_size = '1024'
		sk = RSAcrypto()
		sk.init_rsa(key_size = key_size, crypto_file = "sender.txt")
		sender_key = sk

		#veličina ključa primatelja
		key_size = '1024'
		rk = RSAcrypto()
		rk.init_rsa(key_size = key_size, crypto_file = 'reciever.txt')
		reciever_key = rk

		#hash algoritam
		h = SHAcrypto()
		h.initSHA(type = 'SHA224')

	input_dat = "input_dat.txt"
	i = open(input_dat, "r").read()
	i = bytes(i, 'utf-8')

	print(">Kreiram digitalnu omotnicu")
	env_data = session_key.encrypt(i)
	evn_cryp_key = reciever_key.encrypt(session_key.key)
	from_envelope_to_file(input_file, "envelope.txt",session_key.name, reciever_key.name,
	session_key.key_size,reciever_key.key_size,env_data,evn_cryp_key)

	print(">Kreiram digitalni potpis")
	hash_env = h.digest(env_data)
	signat = sender_key.sign(h.obj)
	from_signature_to_file(input_file, "signature.txt", h.name, sender_key.name, h.digest_len,
	sender_key.key_size, signat)

	print(">Dekriptiranje")
	decr_file = "decrypted-" + input_file
	decr_hash = h.copy()
	decr_hash.update(env_data)
	print("Da li dekriptirani hash odgovara hashu podataka?", sender_key.verify(decr_hash.obj, signat))
	decrypted_session_key = sender_key.decrypt(evn_cryp_key)
	decrypting_session_key = session_key.copy()
	decrypt_data = decrypting_session_key.decrypt(env_data)
	
	print("Odgovara li dekodirani sadržaj početnom?",i.decode('utf-8') == decrypt_data.decode('utf-8'))
	with open(decr_file,'w') as out_file:
		out_file.write(decrypt_data.decode('utf-8'))
	print("Upisan je dekriptirani sadržaj u datoteku", decr_file)

if __name__ == "__main__":
	run_app()