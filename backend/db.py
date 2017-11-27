from peewee import *

db = SqliteDatabase('facecheck.db')

class BaseModel(Model):
    class Meta:
        database = db

class Vault(BaseModel):
    vault_id = FixedCharField(128)
    content = CharField()

def get_vault(vault_id):
    try:
        result = Vault.get(Vault.vault_id == vault_id)
    except:
        return False

    return result
    

def update_vault(vault_id, content):
    return Vault.create(vault_id=vault_id, content=content)

db.connect()
db.create_tables([Vault])


