import bcrypt

def encrypt(plain_text):
  return bcrypt.hashpw(bytes(plain_text, 'utf-8'), bcrypt.gensalt())

def validate_encrypted(plain_text, decrypted_text):
  try:
    return bcrypt.checkpw(bytes(plain_text, 'utf-8'), decrypted_text)
  except:
    return False

