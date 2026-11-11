"""Length-prefixed binary socket framing protocol for Blender MCP.

Provides zero-copy framing (4-byte big-endian uint32 payload length header)
with transparent fallback to legacy unframed JSON streaming. Eliminates
TCP packet truncation, buffer thrashing, and socket desynchronization.
"""

from __future__ import annotations

import json
import socket
import struct
from typing import Any

FRAME_HEADER_SIZE = 4
MAX_PAYLOAD_SIZE = 64 * 1024 * 1024  # 64 MB maximum payload limit


def encode_frame(data: bytes | str | dict | list) -> bytes:
    """Encode a message dictionary or raw payload with a 4-byte uint32 big-endian header."""
    if isinstance(data, (dict, list)):
        payload = json.dumps(data).encode("utf-8")
    elif isinstance(data, str):
        payload = data.encode("utf-8")
    elif isinstance(data, bytes):
        payload = data
    else:
        raise TypeError(f"Unsupported payload type: {type(data)}")

    if len(payload) > MAX_PAYLOAD_SIZE:
        raise ValueError(
            f"Payload size {len(payload)} bytes exceeds maximum {MAX_PAYLOAD_SIZE} bytes"
        )

    header = struct.pack(">I", len(payload))
    return header + payload


class FrameReceiver:
    """Stream parser that reassembles chunked TCP data into discrete message objects."""

    def __init__(self) -> None:
        self._buffer = bytearray()

    def reset(self) -> None:
        """Clear internal buffer state."""
        self._buffer.clear()

    def feed(self, chunk: bytes) -> list[dict[str, Any]]:
        """Feed a received TCP byte chunk and return any fully assembled messages."""
        if not chunk:
            return []

        self._buffer.extend(chunk)
        messages: list[dict[str, Any]] = []

        while self._buffer:
            # Check for legacy JSON mode:
            # Leading ASCII '{' or '[' (or whitespace) indicates unframed legacy stream.
            stripped_start = 0
            while stripped_start < len(self._buffer) and self._buffer[stripped_start] in (
                32,
                9,
                10,
                13,
            ):
                stripped_start += 1

            if stripped_start < len(self._buffer) and self._buffer[stripped_start] in (
                ord("{"),
                ord("["),
            ):
                # Attempt to parse legacy JSON from buffer
                try:
                    text = self._buffer.decode("utf-8")
                    parsed = json.loads(text)
                    self._buffer.clear()
                    if isinstance(parsed, dict):
                        messages.append(parsed)
                    elif isinstance(parsed, list):
                        messages.extend(parsed)
                    break
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Incomplete legacy buffer, wait for more data
                    break

            # Framed mode: needs at least 4 bytes for header
            if len(self._buffer) < FRAME_HEADER_SIZE:
                break

            (payload_length,) = struct.unpack(">I", self._buffer[:FRAME_HEADER_SIZE])

            if payload_length > MAX_PAYLOAD_SIZE:
                # Corrupted stream or unknown encoding, clear buffer to prevent runaway memory
                self._buffer.clear()
                raise ValueError(
                    f"Corrupted frame header: payload length {payload_length} exceeds limit {MAX_PAYLOAD_SIZE}"
                )

            total_frame_size = FRAME_HEADER_SIZE + payload_length
            if len(self._buffer) < total_frame_size:
                # Incomplete frame, wait for more chunks
                break

            payload_bytes = self._buffer[FRAME_HEADER_SIZE:total_frame_size]
            del self._buffer[:total_frame_size]

            try:
                parsed_msg = json.loads(payload_bytes.decode("utf-8"))
                if isinstance(parsed_msg, dict):
                    messages.append(parsed_msg)
                elif isinstance(parsed_msg, list):
                    messages.extend(parsed_msg)
            except Exception as err:
                raise ValueError(f"Failed to parse framed JSON payload: {err}") from err

        return messages


def send_framed_message(sock: socket.socket, message: dict | list) -> None:
    """Send a framed message over a connected socket."""
    frame = encode_frame(message)
    sock.sendall(frame)


def receive_framed_message(
    sock: socket.socket, timeout: float = 180.0, buffer_size: int = 65536
) -> dict[str, Any]:
    """Receive a framed message from a socket, raising TimeoutError or ConnectionError on failure."""
    sock.settimeout(timeout)
    receiver = FrameReceiver()

    while True:
        try:
            chunk = sock.recv(buffer_size)
            if not chunk:
                raise ConnectionError("Socket closed while waiting for response")
            messages = receiver.feed(chunk)
            if messages:
                return messages[0]
        except socket.timeout as err:
            raise TimeoutError(f"Timed out after {timeout}s waiting for socket response") from err
