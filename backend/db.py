from peewee import *
import datetime

db = SqliteDatabase('facecheck.db')

class BaseModel(Model):
    class Meta:
        database = db

class Vault(BaseModel):
    vault_id = FixedCharField(128)
    content = CharField()
    uploaded = DateTimeField(default=datetime.datetime.utcnow)

def get_vault(vault_id):
    try:
        result = (Vault.select().where(Vault.vault_id == vault_id).order_by(Vault.uploaded.desc()).get())
    except:
        return False

    return result
    

def update_vault(vault_id, content):
    return Vault.create(vault_id=vault_id, content=content)

db.connect()
try:
    db.create_tables([Vault])
except:
    pass

