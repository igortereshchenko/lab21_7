from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey

Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    password_hash = Column(String, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Documents(Base):
    __tablename__ = "documents"
    document_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=False)
    document_name = Column(String, nullable=False)
    document_file_path = Column(String, nullable=False)
    document_upload_date = Column(Date, nullable=False)


class Templates(Base):
    __tablename__ = 'templates'
    template_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=False)
    template_name = Column(String, nullable=False)
    template_file_path = Column(String, nullable=False)
    template_upload_date = Column(Date, nullable=False)


class Fields(Base):
    __tablename__ = 'fields'

    field_id = Column(Integer, primary_key=True)
    template_id = Column(Integer, ForeignKey('templates.template_id'), primary_key=False)
    field_name = Column(String, nullable=False)
    field_content = Column(String, nullable=False)

class Mail(Base):
    __tablename__ = 'mail'

    mail_id = Column(Integer, primary_key=True)
    mail_domain = Column(String, nullable=False)
    mail_receiver = Column(String, nullable=False)
    mail_sender = Column(String, nullable=False)
    mail_datetime = Column(Date, nullable=False)

class DocumentsMail(Base):
    __tablename__ = 'documentsoftware'

    document_id_fk = Column(Integer, ForeignKey('documents.document_id'), primary_key=True)
    mail_id_fk = Column(Integer, ForeignKey('mail.mail_id'), primary_key=True)