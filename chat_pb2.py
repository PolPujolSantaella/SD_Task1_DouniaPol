# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chat.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\" \n\x0cLoginRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"F\n\x08Response\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\n\n\x02ip\x18\x03 \x01(\t\x12\x0c\n\x04port\x18\x04 \x01(\x05\"0\n\x0b\x43hatRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0f\n\x07\x63hat_id\x18\x02 \x01(\t\"*\n\x07Message\x12\x0e\n\x06sender\x18\x01 \x01(\t\x12\x0f\n\x07message\x18\x02 \x01(\t\"\"\n\x0fMessageResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x32X\n\x0b\x43hatService\x12#\n\x05Login\x12\r.LoginRequest\x1a\t.Response\"\x00\x12$\n\x07\x43onnect\x12\x0c.ChatRequest\x1a\t.Response\"\x00\x32<\n\nChatClient\x12.\n\x0eReceiveMessage\x12\x08.Message\x1a\x10.MessageResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_LOGINREQUEST']._serialized_start=14
  _globals['_LOGINREQUEST']._serialized_end=46
  _globals['_RESPONSE']._serialized_start=48
  _globals['_RESPONSE']._serialized_end=118
  _globals['_CHATREQUEST']._serialized_start=120
  _globals['_CHATREQUEST']._serialized_end=168
  _globals['_MESSAGE']._serialized_start=170
  _globals['_MESSAGE']._serialized_end=212
  _globals['_MESSAGERESPONSE']._serialized_start=214
  _globals['_MESSAGERESPONSE']._serialized_end=248
  _globals['_CHATSERVICE']._serialized_start=250
  _globals['_CHATSERVICE']._serialized_end=338
  _globals['_CHATCLIENT']._serialized_start=340
  _globals['_CHATCLIENT']._serialized_end=400
# @@protoc_insertion_point(module_scope)
