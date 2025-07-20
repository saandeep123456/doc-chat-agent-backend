from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

DB_PATH = "storage/chat_history.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    role = Column(String)  # 'user' or 'bot'
    text = Column(Text)

Base.metadata.create_all(bind=engine)

def save_message(user_id: str, role: str, text: str):
    session = SessionLocal()
    msg = ChatMessage(user_id=user_id, role=role, text=text)
    session.add(msg)
    session.commit()
    session.close()

def get_history(user_id: str):
    session = SessionLocal()
    messages = session.query(ChatMessage).filter_by(user_id=user_id).all()
    session.close()
    return [{"role": m.role, "text": m.text} for m in messages]
