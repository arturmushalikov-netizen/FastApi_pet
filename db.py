from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

engine = create_engine(url='sqlite:///chat_log.db')

session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class ChatRequest(Base):
    __tablename__ = 'chat_requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    ip_address: Mapped[str] = mapped_column(index=True)
    prompt: Mapped[str]
    response: Mapped[str]

def get_user_request(user_ip: str) -> list[ChatRequest] : 
    with session() as sess:
        query = select(ChatRequest).filter_by(ip_address=user_ip)
        result = sess.execute(query)
        return result.scalars().all()    

def add_request_data(user_ip: str, prompt: str, response: str) -> None : 
    with session() as sess:
        new_request = ChatRequest(
            ip_address=user_ip,
            prompt=prompt,
            response=response
        )
        sess.add(new_request)
        sess.commit()

