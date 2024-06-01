from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LoginRequest(_message.Message):
    __slots__ = ("username",)
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    username: str
    def __init__(self, username: _Optional[str] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ("success", "message", "ip", "port")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    IP_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    ip: str
    port: int
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., ip: _Optional[str] = ..., port: _Optional[int] = ...) -> None: ...

class ConnectionRequest(_message.Message):
    __slots__ = ("username", "chat_id")
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    username: str
    chat_id: str
    def __init__(self, username: _Optional[str] = ..., chat_id: _Optional[str] = ...) -> None: ...

class MessageRequest(_message.Message):
    __slots__ = ("sender", "message")
    SENDER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    sender: str
    message: str
    def __init__(self, sender: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class Subscribe(_message.Message):
    __slots__ = ("chat_id",)
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    def __init__(self, chat_id: _Optional[str] = ...) -> None: ...
