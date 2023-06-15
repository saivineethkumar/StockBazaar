from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

BUY: TRADE_TYPE
DESCRIPTOR: _descriptor.FileDescriptor
SELL: TRADE_TYPE

class HelloRequest(_message.Message):
    __slots__ = ["msg"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class HelloResponse(_message.Message):
    __slots__ = ["msg"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    msg: str
    def __init__(self, msg: _Optional[str] = ...) -> None: ...

class StockInfo(_message.Message):
    __slots__ = ["price", "volume"]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    VOLUME_FIELD_NUMBER: _ClassVar[int]
    price: float
    volume: int
    def __init__(self, price: _Optional[float] = ..., volume: _Optional[int] = ...) -> None: ...

class StockName(_message.Message):
    __slots__ = ["name"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class TradeInput(_message.Message):
    __slots__ = ["name", "quantity", "type"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    name: str
    quantity: int
    type: TRADE_TYPE
    def __init__(self, name: _Optional[str] = ..., quantity: _Optional[int] = ..., type: _Optional[_Union[TRADE_TYPE, str]] = ...) -> None: ...

class TradeStatus(_message.Message):
    __slots__ = ["trade_status"]
    TRADE_STATUS_FIELD_NUMBER: _ClassVar[int]
    trade_status: int
    def __init__(self, trade_status: _Optional[int] = ...) -> None: ...

class UpdateInput(_message.Message):
    __slots__ = ["name", "price"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    name: str
    price: float
    def __init__(self, name: _Optional[str] = ..., price: _Optional[float] = ...) -> None: ...

class UpdateStatus(_message.Message):
    __slots__ = ["update_status"]
    UPDATE_STATUS_FIELD_NUMBER: _ClassVar[int]
    update_status: int
    def __init__(self, update_status: _Optional[int] = ...) -> None: ...

class TRADE_TYPE(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
