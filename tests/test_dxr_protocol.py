import json
import struct
import io
import pytest
from blender_mcp.protocol import (
    encode_frame,
    FrameReceiver,
    FRAME_HEADER_SIZE,
    MAX_PAYLOAD_SIZE,
)

def test_encode_frame_dict():
    msg = {"type": "ping", "id": 123}
    encoded = encode_frame(msg)
    assert len(encoded) >= FRAME_HEADER_SIZE
    length = struct.unpack(">I", encoded[:4])[0]
    payload = encoded[4:]
    assert len(payload) == length
    decoded = json.loads(payload.decode("utf-8"))
    assert decoded == msg

def test_frame_receiver_single_complete():
    receiver = FrameReceiver()
    msg = {"status": "ok", "data": [1, 2, 3]}
    frame = encode_frame(msg)
    messages = receiver.feed(frame)
    assert len(messages) == 1
    assert messages[0] == msg

def test_frame_receiver_fragmented_chunks():
    receiver = FrameReceiver()
    msg = {"type": "execute_code", "params": {"code": "print('hello' * 1000)"}}
    frame = encode_frame(msg)
    
    # Split frame into tiny chunks of 7 bytes
    messages = []
    chunk_size = 7
    for i in range(0, len(frame), chunk_size):
        chunk = frame[i:i+chunk_size]
        res = receiver.feed(chunk)
        messages.extend(res)
        
    assert len(messages) == 1
    assert messages[0] == msg

def test_frame_receiver_multiple_messages_in_single_chunk():
    receiver = FrameReceiver()
    msg1 = {"type": "msg1", "value": 42}
    msg2 = {"type": "msg2", "value": 99}
    combined = encode_frame(msg1) + encode_frame(msg2)
    
    messages = receiver.feed(combined)
    assert len(messages) == 2
    assert messages[0] == msg1
    assert messages[1] == msg2

def test_frame_receiver_legacy_unframed_fallback():
    receiver = FrameReceiver()
    legacy_json = json.dumps({"type": "legacy", "message": "unframed"}).encode("utf-8")
    messages = receiver.feed(legacy_json)
    assert len(messages) == 1
    assert messages[0]["type"] == "legacy"

def test_frame_receiver_large_payload():
    receiver = FrameReceiver()
    # 500KB payload
    large_data = "x" * (500 * 1024)
    msg = {"type": "large", "data": large_data}
    frame = encode_frame(msg)
    
    messages = receiver.feed(frame)
    assert len(messages) == 1
    assert messages[0]["data"] == large_data
