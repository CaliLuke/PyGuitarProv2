import struct
import logging
from contextlib import contextmanager
from typing import Union, Optional, List, Any, BinaryIO, Tuple, overload, Literal # Literal might be removed if not used by final strategy

import attr

from .. import models as gp
from ..exceptions import GPException



logger = logging.getLogger(__name__)


@attr.s
class GPFileBase:
    data: BinaryIO = attr.ib()
    encoding: str = attr.ib()
    version: Optional[str] = attr.ib(default=None)
    versionTuple: Optional[Tuple[int, ...]] = attr.ib(default=None)

    bendPosition = 60
    bendSemitone = 25

    _supportedVersions: List[str] = []

    _currentTrack: Optional['gp.Track'] = None
    _currentMeasureNumber: Optional[int] = None
    _currentVoiceNumber: Optional[int] = None
    _currentBeatNumber: Optional[int] = None

    def close(self):
        self.data.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        self.close()

    # Reading
    # =======

    def skip(self, count: int):
        return self.data.read(count)

    def read(self, fmt: str, size: int, default: Optional[Any] = None) -> Any:
        try:
            data = self.data.read(size)
            result = struct.unpack(fmt, data)
            return result[0]
        except struct.error:
            if default is not None:
                return default
            else:
                raise

    @overload
    def readByte(self, *, default: Optional[int] = None) -> Optional[int]: ...
    @overload
    def readByte(self, count: int, default: Optional[int] = None) -> Optional[List[int]]: ...
    def readByte(self, count: int = 1, default: Optional[int] = None) -> Union[Optional[int], Optional[List[int]]]:
        """Read 1 byte *count* times."""
        args = ('B', 1)
        if count == 1:
            val = self.read(*args, default=default)
            return val if val is not None else None
        results = [val for _ in range(count) if (val := self.read(*args, default=default)) is not None]
        return results if results else None


    @overload
    def readSignedByte(self, *, default: Optional[int] = None) -> Optional[int]: ...
    @overload
    def readSignedByte(self, count: int, default: Optional[int] = None) -> Optional[List[int]]: ...
    def readSignedByte(self, count: int = 1, default: Optional[int] = None) -> Union[Optional[int], Optional[List[int]]]:
        """Read 1 signed byte *count* times."""
        args = ('b', 1)
        if count == 1:
            val = self.read(*args, default=default)
            return val if val is not None else None
        results = [val for _ in range(count) if (val := self.read(*args, default=default)) is not None]
        return results if results else None

    @overload
    def readBool(self, *, default: Optional[bool] = None) -> Optional[bool]: ...
    @overload
    def readBool(self, count: int, default: Optional[bool] = None) -> Optional[List[bool]]: ...
    def readBool(self, count: int = 1, default: Optional[bool] = None) -> Union[Optional[bool], Optional[List[bool]]]:
        """Read 1 byte *count* times as a boolean."""
        args = ('?', 1)
        if count == 1:
            val = self.read(*args, default=default)
            return val if val is not None else None
        results = [val for _ in range(count) if (val := self.read(*args, default=default)) is not None]
        return results if results else None

    @overload
    def readShort(self, *, default: Optional[int] = None) -> Optional[int]: ...
    @overload
    def readShort(self, count: int, default: Optional[int] = None) -> Optional[List[int]]: ...
    def readShort(self, count: int = 1, default: Optional[int] = None) -> Union[Optional[int], Optional[List[int]]]:
        """Read 2 little-endian bytes *count* times as a short integer."""
        args = ('<h', 2)
        if count == 1:
            val = self.read(*args, default=default)
            return val if val is not None else None
        results = [val for _ in range(count) if (val := self.read(*args, default=default)) is not None]
        return results if results else None

    @overload
    def readInt(self, *, default: Optional[int] = None) -> Optional[int]: ...
    @overload
    def readInt(self, count: int, default: Optional[int] = None) -> Optional[List[int]]: ...
    def readInt(self, count: int = 1, default: Optional[int] = None) -> Union[Optional[int], Optional[List[int]]]:
        """Read 4 little-endian bytes *count* times as an integer."""
        args = ('<i', 4)
        if count == 1:
            val = self.read(*args, default=default)
            return val if val is not None else None
        results = [val for _ in range(count) if (val := self.read(*args, default=default)) is not None]
        return results if results else None

    @overload
    def readFloat(self, *, default: Optional[float] = None) -> Optional[float]: ...
    @overload
    def readFloat(self, count: int, default: Optional[float] = None) -> Optional[List[float]]: ...
    def readFloat(self, count: int = 1, default: Optional[float] = None) -> Union[Optional[float], Optional[List[float]]]:
        """Read 4 little-endian bytes *count* times as a float."""
        args = ('<f', 4)
        if count == 1:
            val = self.read(*args, default=default)
            return val if val is not None else None
        results = [val for _ in range(count) if (val := self.read(*args, default=default)) is not None]
        return results if results else None
        
    @overload
    def readDouble(self, *, default: Optional[float] = None) -> Optional[float]: ...
    @overload
    def readDouble(self, count: int, default: Optional[float] = None) -> Optional[List[float]]: ...
    def readDouble(self, count: int = 1, default: Optional[float] = None) -> Union[Optional[float], Optional[List[float]]]:
        """Read 8 little-endian bytes *count* times as a double."""
        args = ('<d', 8)
        if count == 1:
            val = self.read(*args, default=default)
            return val if val is not None else None
        results = [val for _ in range(count) if (val := self.read(*args, default=default)) is not None]
        return results if results else None

    def readString(self, size: int, length: Optional[int] = None) -> str:
        if length is None:
            length = size
        read_count = size if size > 0 else length
        s = self.data.read(read_count)
        ss = s[:(length if length >= 0 else size)]
        return ss.decode(self.encoding)

    def readByteSizeString(self, size: int) -> str:
        """Read length of the string stored in 1 byte and followed by character
        bytes.
        """
        str_len = self.readByte() 
        if not isinstance(str_len, int):
            raise GPException(f"Expected int for string length, got {type(str_len)}")
        return self.readString(size, str_len)

    def readIntSizeString(self) -> str:
        """Read length of the string stored in 1 integer and followed by
        character bytes.
        """
        str_len = self.readInt() 
        if not isinstance(str_len, int):
            raise GPException(f"Expected int for string length, got {type(str_len)}")
        return self.readString(str_len)

    def readIntByteSizeString(self) -> str:
        """Read length of the string increased by 1 and stored in 1 integer
        followed by length of the string in 1 byte and finally followed by
        character bytes.
        """
        val_d = self.readInt() 
        if not isinstance(val_d, int):
             raise GPException(f"Expected int for string length prefix, got {type(val_d)}")
        d = val_d - 1
        return self.readByteSizeString(d)

    def readVersion(self) -> str:
        if self.version is None:
            self.version = self.readByteSizeString(30)
        return self.version

    @contextmanager
    def annotateErrors(self, action):
        self._currentTrack = None
        self._currentMeasureNumber = None
        self._currentVoiceNumber = None
        self._currentBeatNumber = None
        try:
            yield
        except Exception as err:
            location = self.getCurrentLocation()
            if not location:
                raise
            raise GPException(f"{action} {', '.join(location)}, "
                                 f"got {err.__class__.__name__}: {err}") from err
        finally:
            self._currentTrack = None
            self._currentMeasureNumber = None
            self._currentVoiceNumber = None
            self._currentBeatNumber = None

    def getEnumValue(self, enum):
        if enum.name == 'unknown':
            location = self.getCurrentLocation()
            logger.warning(f"{enum.value!r} is an unknown {enum.__class__.__name__} in {', '.join(location)}")
        return enum.value

    def getCurrentLocation(self):
        location = []
        if self._currentTrack is not None:
            location.append(f"track {self._currentTrack.number}")
        if self._currentMeasureNumber is not None:
            location.append(f"measure {self._currentMeasureNumber}")
        if self._currentVoiceNumber is not None:
            location.append(f"voice {self._currentVoiceNumber}")
        if self._currentBeatNumber is not None:
            location.append(f"beat {self._currentBeatNumber}")
        return location

    # Writing
    # =======

    def placeholder(self, count, byte=b'\x00'):
        self.data.write(byte * count)

    def writeByte(self, data):
        packed = struct.pack('B', int(data))
        self.data.write(packed)

    def writeSignedByte(self, data):
        packed = struct.pack('b', int(data))
        self.data.write(packed)

    def writeBool(self, data):
        packed = struct.pack('?', bool(data))
        self.data.write(packed)

    def writeShort(self, data):
        packed = struct.pack('<h', int(data))
        self.data.write(packed)

    def writeInt(self, data):
        packed = struct.pack('<i', int(data))
        self.data.write(packed)

    def writeFloat(self, data):
        packed = struct.pack('<f', float(data))
        self.data.write(packed)

    def writeDouble(self, data):
        packed = struct.pack('<d', float(data))
        self.data.write(packed)

    def writeString(self, data, size=None):
        if size is None:
            size = len(data)
        self.data.write(data.encode(self.encoding))
        self.placeholder(size - len(data))

    def writeByteSizeString(self, data, size=None):
        if size is None:
            size = len(data)
        self.writeByte(len(data))
        return self.writeString(data, size)

    def writeIntSizeString(self, data):
        self.writeInt(len(data))
        return self.writeString(data)

    def writeIntByteSizeString(self, data):
        self.writeInt(len(data) + 1)
        return self.writeByteSizeString(data)

    def writeVersion(self):
        self.writeByteSizeString(self.version, 30)