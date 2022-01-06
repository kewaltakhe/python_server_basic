import socket
import threading
import os.path

webpages_path = './webpages/'
webpages_abs_path = os.path.abspath(webpages_path)

def main():
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	server_socket.bind(('',80))
	server_socket.listen(2)
	while True:
		client_conn, addr = server_socket.accept()
		client_handler(client_conn)
		#handler_thread = threading.Thread(target = client_handler,args=(client_conn,))
		#handler_thread.start()

def client_handler(client_conn):
	recv_len = 1
	http_request = ''
	while recv_len:
		data = client_conn.recv(4096)
		recv_len = len(data)
		http_request += data.decode()
		if recv_len < 4096:
			break

	http_request_content = http_request.split()
	requested_filepath =http_request_content[1]
	
	try:
		if requested_filepath.endswith('html'):
			with open(webpages_abs_path+'/'+requested_filepath,'rb') as requested_file:
				body = requested_file.read()
				head = get_200response_head(len(body))
				http_response_byte = head+body
		else:
			http_response_byte = badrequest()
	except FileNotFoundError:
		http_response_byte = filenotfound()
	except Exception:
		http_response_byte = badrequest()
	client_conn.sendall(http_response_byte)
	client_conn.close()

def filenotfound():
	response_404 = 'HTTP/1.1 404 Not Found\r\n'\
	+'Content-Type: text/html\r\n\r\n'\
	+'<html>\n<head><title>404 Not Found</title></head>\n<body bgcolor="pink">\n<center><h1>404 Not Found baby</h1></center>\n<hr>\n</body>\n</html>'
	return response_404.encode()

def badrequest():
	response_400 = 'HTTP/1.1 400 Bad Request\r\n'\
	+'Content-Type: text/html\r\n\r\n'\
	+'<html>\n<head><title>400 Bad Request</title></head>\n<body bgcolor="pink">\n<center><h1><center>400</center></h1><br><h1>Bad Request</h1></center>\n<hr>\n</body>\n</html>'
	return response_400.encode()

def get_200response_head(content_len):
	status_line = 'HTTP/1.1 200 OK\r\n'
	header_server = 'Server: python3_custom_server\r\n'
	header_Content_Type = 'Content-Type: text/html\r\n'
	header_Content_Lenght = 'Content-Length: {0}\r\n'.format(content_len)
	#add other headers
	head = status_line+header_server+header_Content_Type+header_Content_Lenght+'\r\n'
	return head.encode()

if __name__ == '__main__':
	print('the server is up running...')
	main()