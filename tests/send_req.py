import socket
from prompt_processing.batchhandling import SocketBatchHandler


handler = SocketBatchHandler()
handler.submit('submit echo hee hee')

