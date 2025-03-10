import uuid
from datetime import datetime
from typing import List, Literal
from uuid import UUID

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "core_user"

    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        insert_default=uuid.uuid4()
    )
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    first_name: Mapped[str] = mapped_column(default=' ')
    last_name: Mapped[str] = mapped_column(default=' ')
    is_superuser: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    nodes: Mapped[List["Node"]] = relationship(
        back_populates="user",
        primaryjoin="User.id == Node.user_id"
    )
    home_folder_id: Mapped[UUID] = mapped_column(
        ForeignKey("core_folder.basetreenode_ptr_id", deferrable=True)
    )
    home_folder: Mapped['Folder'] = relationship(
        primaryjoin="User.home_folder_id == Folder.id",
        back_populates="user",
        viewonly=True
    )
    inbox_folder_id: Mapped[UUID] = mapped_column(
        ForeignKey("core_folder.basetreenode_ptr_id", deferrable=True)
    )
    inbox_folder: Mapped['Folder'] = relationship(
        primaryjoin="User.home_folder_id == Folder.id",
        back_populates="user",
        viewonly=True
    )
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now()
    )
    date_joined: Mapped[datetime] = mapped_column(
        insert_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now()
    )


CType = Literal["document", "folder"]


class Node(Base):
    __tablename__ = "core_basetreenode"

    id: Mapped[UUID] = mapped_column(
        primary_key=True, insert_default=uuid.uuid4()
    )
    title: Mapped[str] = mapped_column(String(200))
    ctype: Mapped[CType]
    lang: Mapped[str] = mapped_column(String(8))
    tags: List[str] = []
    user: Mapped["User"] = relationship(
        back_populates="nodes",
        primaryjoin="User.id == Node.user_id"
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("core_user.id"))
    parent_id: Mapped[UUID] = mapped_column(ForeignKey("core_basetreenode.id"))
    created_at: Mapped[datetime] = mapped_column(
        insert_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now()
    )

    __mapper_args__ = {
        "polymorphic_identity": "node",
        "polymorphic_on": "ctype",
    }

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title!r})"


class Folder(Node):
    __tablename__ = "core_folder"

    id: Mapped[UUID] = mapped_column(
        'basetreenode_ptr_id',
        ForeignKey("core_basetreenode.id"),
        primary_key=True,
        insert_default=uuid.uuid4()
    )

    __mapper_args__ = {
        "polymorphic_identity": "folder",
    }


class Document(Node):
    __tablename__ = "core_document"

    id: Mapped[UUID] = mapped_column(
        'basetreenode_ptr_id',
        ForeignKey("core_basetreenode.id"), primary_key=True
    )

    ocr: Mapped[bool]
    ocr_status: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "document",
    }


class DocumentVersion(Base):
    __tablename__ = "core_documentversion"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    number: Mapped[int]
    file_name: Mapped[str]
    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("core_document.basetreenode_ptr_id")
    )
    lang: Mapped[str]
    short_description: Mapped[str]


class Page(Base):
    __tablename__ = "core_page"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    number: Mapped[int]
    lang: Mapped[str]
    text: Mapped[str]
    document_version_id: Mapped[UUID] = mapped_column(
        ForeignKey("core_documentversion.id")
    )


class Tag(Base):
    __tablename__ = "core_tag"
    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str]
    bg_color: Mapped[str]
    fg_color: Mapped[str]
    description: Mapped[str]
    pinned: Mapped[bool]


class ColoredTag(Base):
    __tablename__ = "core_coloredtag"
    id: Mapped[int] = mapped_column(primary_key=True)
    object_id: Mapped[UUID]
    tag_id: Mapped[UUID] = mapped_column(
        ForeignKey("core_tag.id")
    )
    tag: Mapped["Tag"] = relationship(
        primaryjoin="Tag.id == ColoredTag.tag_id"
    )
