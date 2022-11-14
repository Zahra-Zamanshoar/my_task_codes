import os
import argparse


def outer_inner(End_point):
    """
    writes outer and inner in neginex.

    Parameters:
    End_point (str): End point that  used  as outer and inner locations
    point: point that  used  as outer and inner locations

    Returns:
    string: outer and inner

    """
    outer = '##outer users'

    inner = "##inner users, has no version because it should be updated instantly"

    common = '      proxy_set_header Host $host; \n       proxy_set_header X-Real-IP $remote_addr;' \
             '\n       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for'

    point = End_point.split('/')[-1]
    return f'\n{outer:2s} \n    location ^~ /ai{End_point} \n'+'    {\n'+ \
           f'       proxy_pass $address_parser_upstream:660 {point}; \n {common}\n' + '   }\n'\
           f'\n{inner:2s} \n    location ^~ {End_point} \n'+'   {\n'+ \
           f'       proxy_pass $address_parser_upstream:660 {point}; \n {common}\n' \
           f'       allow 172.16.0.0/12; \n ' \
           f'      deny all;\n '+ '   }\n\n'


def server(listen=[80], server_name='0.0.0.0'):
    """
    server

    Parameters:
    listen (list):
    server_name: name of server

    Returns:
    string: server

    """

    upstream_minio = 'upstream minio\n{ \n server_minio \n}\n'

    upstream_consol = 'upstream consol\n{ \n  ip_hash; \n  server minio:9001;\n}\n'

    server_minio =  f'    listen 9000; \n ' \
           f'   listen [::]:9000; \n ' \
           f'   server_name localhost; \n \n' \
           f'    # To allow special characters in headers \n' \
           f'   ignore_invalid_headers off; \n ' \
           f'   # Allow any size file to be uploaded.\n ' \
           f'   # Set to a value such as 1000m; to restrict file size to a specific value \n ' \
           f'   client_max_body_size 0; \n ' \
           f'   # To disable buffering \n ' \
           f'   proxy_buffering off; \n ' \
           f'   proxy_request_buffering off; \n ' \
           f'   location / \n '+ '  {\n' \
           f"       proxy_set_header X-Real-IP $remote_addr; \n " \
           f"      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n" \
           f"       proxy_set_header X-Forwarded-Proto $scheme;\n\n" \
           f"       proxy_connect_timeout 300; \n" \
           f"       # Default is HTTP/1, keepalive is only enabled in HTTP/1.1\n" \
           f"       proxy_http_version 1.1;\n" \
           f'       proxy_set_header Connection "";\n\n' \
           f'       chunked_transfer_encoding off;\n\n' \
           f'       proxy_pass http://minio;\n'+ '   }\n' \

    server_console =  f'    listen 9001; \n ' \
           f'   listen [::]:9001; \n ' \
           f'   server_name localhost; \n \n' \
           f'    # To allow special characters in headers \n' \
           f'   ignore_invalid_headers off; \n ' \
           f'   # Allow any size file to be uploaded.\n ' \
           f'   # Set to a value such as 1000m; to restrict file size to a specific value \n ' \
           f'   client_max_body_size 0; \n ' \
           f'   # To disable buffering \n ' \
           f'   proxy_buffering off; \n ' \
           f'   proxy_request_buffering off; \n ' \
           f'   location / \n '+ '  {\n' \
           f"       proxy_set_header X-Real-IP $remote_addr; \n " \
           f"      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n" \
           f"       proxy_set_header X-Forwarded-Proto $scheme;\n\n" \
           f"       proxy_set_header X-NginX-Proxy true\n" \
           f"       proxy_connect_timeout 300; \n " \
           f"       # To support websocket\n" \
           f"       proxy_http_version 1.1;\n" \
           f"       proxy_set_header Upgrade $http_upgrade;\n" \
           f'       proxy_set_header Connection "upgrade";\n\n' \
           f'       chunked_transfer_encoding off;\n\n' \
           f'       proxy_pass http://console;\n'+ '   }\n' \


    return f'{upstream_minio} \n' \
           f'{upstream_consol}\n' \
           f'server \n'+ '{\n' \
           f'{server_minio}\n ' \
           f'server\n '+ '{\n' \
           f'{server_console}\n' \
           f'server\n '+ '{\n' \
           f'  listen {listen};\n ' \
           f'  server_name {server_name};\n  ' \
           f' resolver 127.0.0.11 valid=30s;\n  ' \
           f' client_max_body_size 20M;\n '


def title(name):
    """
    writes title in neginex.

    Parameters:
    name (str): Titles that are used both as a title and as outer and inner locations

    Returns:
    string: outer and inner

    """
    title = f'##{name}'
    return f'{title} \n   set ${name}_upstream http://{name};\n \n'


# parser = argparse.ArgumentParser(description='The file  want to make negix from')
# parser.add_argument("--docker", help='The file  want to make negix from', default='docker-compose.yml')
# args = parser.parse_args()
# docker = args.docker()

# Creating a dictionary of titles along with endpoints
dic = dict()
with open('docker-compose.yml', encoding="utf-8") as docker_file:
    deta = docker_file.readlines()
    for line in deta:
        count = 0
        # count space
        for item in line[:5]:
            if item == ' ':
                count += 1
            else:
                break
        # Find based on distance
        if count == 2:
            line_ = line.strip().strip(':').strip('# ')
            # Add titles as key (along with a list of values that are empty)
            dic[line_] = []
            pass

        if 'ENDPOINT' in line:
            line_end_point = line.strip().strip(':').strip('# ').strip('-')
            end_point = line_end_point.split('=')[-1]
            # Add endpoint as value
            dic[line_].append(end_point)
with open('nginx.conf', 'w+') as nginx:
    nginx.write(server())
    for key, value in dic.items():
        if value:
            nginx.write(title(key))
            for i in range(len(value)):
                nginx.write(outer_inner(value[i]))
