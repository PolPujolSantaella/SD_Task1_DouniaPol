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




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nchat.proto\"6\n\x11\x43onnectionRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x0f\n\x07\x63hat_id\x18\x02 \x01(\t\"I\n\x12\x43onnectionResponse\x12\x11\n\tconnected\x18\x01 \x01(\x08\x12\x12\n\nip_address\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\x32\x41\n\x0b\x43hatService\x12\x32\n\x07\x43onnect\x12\x12.ConnectionRequest\x1a\x13.ConnectionResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'chat_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_CONNECTIONREQUEST']._serialized_start=14
  _globals['_CONNECTIONREQUEST']._serialized_end=68
  _globals['_CONNECTIONRESPONSE']._serialized_start=70
  _globals['_CONNECTIONRESPONSE']._serialized_end=143
  _globals['_CHATSERVICE']._serialized_start=145
  _globals['_CHATSERVICE']._serialized_end=210
# @@protoc_insertion_point(module_scope)