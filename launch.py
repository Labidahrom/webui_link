import http.server
import socketserver
import json
from module import get_image_link


class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/image.png':
            with open('image.png', 'rb') as f:
                img_data = f.read()

            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Content-Length', str(len(img_data)))
            self.end_headers()

            self.wfile.write(img_data)
            return

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        post_json = json.loads(post_data)
        prompt = post_json.get('description', None)

        # Process the post_json data and generate a response JSON
        if prompt:
            response_json = {'image_url': get_image_link(prompt)}
        else:
            response_json = {'image_url': 'wrong description'}
        response_data = json.dumps(response_json)

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(response_data)))
        self.end_headers()

        # Send the response JSON back to the client
        self.wfile.write(response_data.encode('utf-8'))

# Set up the server to listen on localhost and port 8000
server_address = ('0.0.0.0', 8000)
httpd = socketserver.TCPServer(server_address, MyHandler)

# Start the server
print('Server started on {}:{}'.format(*server_address))
httpd.serve_forever()
