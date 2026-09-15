"""Real adapter tests: skipped when the actual SDK extra is absent.

No mocked test is reported as a real Scrapling roundtrip. This test uses only
an explicitly permitted loopback HTTP fixture, not a third-party website.
"""
import threading
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
import pytest
from keensight_scrapling.transport import ScraplingTransport
from keensight_scrapling.urls import NetworkPolicy

@pytest.mark.live
def test_real_scrapling_local_roundtrip():
    pytest.importorskip('scrapling.fetchers')
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200);self.send_header('Content-Type','text/html');self.end_headers()
            self.wfile.write(b'<html><p>Actual SDK roundtrip</p></html>')
        def log_message(self,*a):pass
    server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f'http://127.0.0.1:{server.server_port}'
    try:
        result=ScraplingTransport(NetworkPolicy((base,),allow_loopback_test=True)).get(base+'/')
        assert result.status_code==200 and b'Actual SDK roundtrip' in result.body
    finally:server.shutdown();server.server_close();thread.join()
