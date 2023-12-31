# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: stocktrade.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10stocktrade.proto\"\"\n\rLookupRequest\x12\x11\n\tstockname\x18\x01 \x01(\t\"B\n\x0eLookupResponse\x12\x11\n\tstockname\x18\x01 \x01(\t\x12\r\n\x05price\x18\x02 \x01(\x01\x12\x0e\n\x06volume\x18\x03 \x01(\x03\"T\n\rUpdateRequest\x12\x11\n\tstockname\x18\x01 \x01(\t\x12\x1e\n\ntrade_type\x18\x02 \x01(\x0e\x32\n.TradeType\x12\x10\n\x08quantity\x18\x03 \x01(\x03\"3\n\x0eUpdateResponse\x12\x11\n\tstockname\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\x11\"S\n\x0cTradeRequest\x12\x11\n\tstockname\x18\x01 \x01(\t\x12\x1e\n\ntrade_type\x18\x02 \x01(\x0e\x32\n.TradeType\x12\x10\n\x08quantity\x18\x03 \x01(\x03\"N\n\rTradeResponse\x12\x11\n\tstockname\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\x11\x12\x1a\n\x12transaction_number\x18\x03 \x01(\x03\"\x07\n\x05\x45mpty*\x1e\n\tTradeType\x12\x07\n\x03\x42UY\x10\x00\x12\x08\n\x04SELL\x10\x01\x32j\n\x0e\x43\x61talogService\x12+\n\x06Lookup\x12\x0e.LookupRequest\x1a\x0f.LookupResponse\"\x00\x12+\n\x06Update\x12\x0e.UpdateRequest\x1a\x0f.UpdateResponse\"\x00\x32R\n\x0cOrderService\x12(\n\x05Trade\x12\r.TradeRequest\x1a\x0e.TradeResponse\"\x00\x12\x18\n\x04Save\x12\x06.Empty\x1a\x06.Empty\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'stocktrade_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _TRADETYPE._serialized_start=437
  _TRADETYPE._serialized_end=467
  _LOOKUPREQUEST._serialized_start=20
  _LOOKUPREQUEST._serialized_end=54
  _LOOKUPRESPONSE._serialized_start=56
  _LOOKUPRESPONSE._serialized_end=122
  _UPDATEREQUEST._serialized_start=124
  _UPDATEREQUEST._serialized_end=208
  _UPDATERESPONSE._serialized_start=210
  _UPDATERESPONSE._serialized_end=261
  _TRADEREQUEST._serialized_start=263
  _TRADEREQUEST._serialized_end=346
  _TRADERESPONSE._serialized_start=348
  _TRADERESPONSE._serialized_end=426
  _EMPTY._serialized_start=428
  _EMPTY._serialized_end=435
  _CATALOGSERVICE._serialized_start=469
  _CATALOGSERVICE._serialized_end=575
  _ORDERSERVICE._serialized_start=577
  _ORDERSERVICE._serialized_end=659
# @@protoc_insertion_point(module_scope)
