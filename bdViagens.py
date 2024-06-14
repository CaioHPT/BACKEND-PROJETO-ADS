# Instar o sqlalchemy no terminal
#pip install sqlalchemy

import sqlalchemy

#Conectando ao banco de dados

engine = sqlalchemy.create_engine('sqlite:///viagens.db', echo=True)

#Declarando o Mapeamento

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Numeric

Base = declarative_base()

class Viagens (Base):
  __tablename__ = 'turismo'
  id = Column(Integer, primary_key = True)
  origem = Column(String)
  destino = Column(String)
  valor = Column(Numeric(11, 2))
  urlfoto = Column(String)

  def to_json(self):
     return {
        "id": self.id,
        "origem": self.origem,
        "destino": self.destino,
        "valor": self.valor,
        "urlFoto": self.urlfoto
     }
  
Base.metadata.create_all(engine)
#Sessão
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
#Session

session = Session()
