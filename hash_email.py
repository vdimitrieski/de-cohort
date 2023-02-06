from hashlib import sha1

def compute_hash(email):
  return sha1(email.lower().encode('utf-8')).hexdigest()


print(compute_hash("vldimitrieski@gmail.com"))

# e4bb908d76fa8ecc730b32e0e6ba8b8d4ef66e31