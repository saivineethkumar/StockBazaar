from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

BUY: TradeType
DESCRIPTOR: _descriptor.FileDescriptor
SELL: TradeType

class AliveResponse(_message.Message):
    __slots__ = ["is_alive"]
    IS_ALIVE_FIELD_NUMBER: _ClassVar[int]
    is_alive: bool
    def __init__(self, is_alive: bool = ...) -> None: ...

class CacheInvalidateRequest(_message.Message):
    __slots__ = ["stockname"]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    stockname: str
    def __init__(self, stockname: _Optional[str] = ...) -> None: ...

class Empty(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetLeaderResponse(_message.Message):
    __slots__ = ["leader_id"]
    LEADER_ID_FIELD_NUMBER: _ClassVar[int]
    leader_id: int
    def __init__(self, leader_id: _Optional[int] = ...) -> None: ...

class LookupRequest(_message.Message):
    __slots__ = ["stockname"]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    stockname: str
    def __init__(self, stockname: _Optional[str] = ...) -> None: ...

class LookupResponse(_message.Message):
    __slots__ = ["price", "stockname", "volume"]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    price: float
    stockname: str
    volume: int
    def __init__(self, stockname: _Optional[str] = ..., price: _Optional[float] = ..., volume: _Optional[int] = ...) -> None: ...

class OrderDBItem(_message.Message):
    __slots__ = ["quantity", "stockname", "trade_type", "transaction_number"]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    TRADE_TYPE_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    quantity: int
    stockname: str
    trade_type: TradeType
    transaction_number: int
    def __init__(self, stockname: _Optional[str] = ..., trade_type: _Optional[_Union[TradeType, str]] = ..., quantity: _Optional[int] = ..., transaction_number: _Optional[int] = ...) -> None: ...

class OrderLookupRequest(_message.Message):
    __slots__ = ["order_id"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    def __init__(self, order_id: _Optional[int] = ...) -> None: ...

class OrderLookupResponse(_message.Message):
    __slots__ = ["order_id", "quantity", "status", "stockname", "trade_type"]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    TRADE_TYPE_FIELD_NUMBER: _ClassVar[int]
    order_id: int
    quantity: int
    status: int
    stockname: str
    trade_type: TradeType
    def __init__(self, order_id: _Optional[int] = ..., status: _Optional[int] = ..., stockname: _Optional[str] = ..., trade_type: _Optional[_Union[TradeType, str]] = ..., quantity: _Optional[int] = ...) -> None: ...

class SetLeaderRequest(_message.Message):
    __slots__ = ["leader_id"]
    LEADER_ID_FIELD_NUMBER: _ClassVar[int]
    leader_id: int
    def __init__(self, leader_id: _Optional[int] = ...) -> None: ...

class SyncRequest(_message.Message):
    __slots__ = ["max_transaction_number"]
    MAX_TRANSACTION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    max_transaction_number: int
    def __init__(self, max_transaction_number: _Optional[int] = ...) -> None: ...

class TradeRequest(_message.Message):
    __slots__ = ["quantity", "stockname", "trade_type"]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    TRADE_TYPE_FIELD_NUMBER: _ClassVar[int]
    quantity: int
    stockname: str
    trade_type: TradeType
    def __init__(self, stockname: _Optional[str] = ..., trade_type: _Optional[_Union[TradeType, str]] = ..., quantity: _Optional[int] = ...) -> None: ...

class TradeResponse(_message.Message):
    __slots__ = ["status", "stockname", "transaction_number"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    status: int
    stockname: str
    transaction_number: int
    def __init__(self, stockname: _Optional[str] = ..., status: _Optional[int] = ..., transaction_number: _Optional[int] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ["quantity", "stockname", "trade_type"]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    TRADE_TYPE_FIELD_NUMBER: _ClassVar[int]
    quantity: int
    stockname: str
    trade_type: TradeType
    def __init__(self, stockname: _Optional[str] = ..., trade_type: _Optional[_Union[TradeType, str]] = ..., quantity: _Optional[int] = ...) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ["status", "stockname"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STOCKNAME_FIELD_NUMBER: _ClassVar[int]
    status: int
    stockname: str
    def __init__(self, stockname: _Optional[str] = ..., status: _Optional[int] = ...) -> None: ...

class TradeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
