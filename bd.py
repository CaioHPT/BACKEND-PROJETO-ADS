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

#Criar tabela no banco de dados

Base.metadata.create_all(engine)

#Classes
#pacote = Viagens(origem = 'São Paulo', destino = 'Rio de Janeiro', ida = 2024312, volta = 2024315)

#Sessão
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
#Session

session = Session()

#Insert
#session.add(pacote)
#session.commit()

#Adiocionar dados, smp usar o commit apos as inclusoes # session.commit'()'
#session.add_all([
#    Viagens(origem = 'Minas Gerais', destino = 'Rio de Janeiro', ida = 12102024, volta = 15102024),
#   Viagens(origem = 'São Paulo', destino = 'Italia', ida = 12102024, volta = 12102029),
#  Viagens(origem = 'São Paulo', destino = 'Espanha', ida = 12102024, volta = 12102029),
# ])


#session.new

#session.commit()

#Query para consulta
#for instance in session.query(Viagens).order_by(Viagens.id):
#    print(instance.origem, instance.destino, instance.ida, instance.volta)

