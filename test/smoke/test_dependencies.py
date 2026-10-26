import requests
import socket
from urllib.parse import urlsplit

import aiodns
import asyncio
from IPy import IP
import config

class TestDependencies(unittest.TestMethodClass):
    def _get_details(self, url):
        url_details=urlsplit(url)

        ipAddr = list([])
        try:
            IP(url_details.hostname)
        except ValueError:
            res = await resolver.query(url_details).hostname
            ipAddr.extend(res)
        else:
            ipAddr.append(config.AI_ENDPOINT)
        ports = list([])
        if isinstance(url_details.port,int):
            ports.append(url_details.port)
        elif url_details.scheme == "https" or url_details.scheme == "wss" or url_details.scheme == "oci":
            ports.append(443)
        elif url_details.scheme == "http" or url_details.scheme == "ws":
            ports.append(80)
        else:
            ports.append(80)
            ports.append(443)

        return (ipAddr, ports)

    def _test_firewall(self):

    async def test_ai(self):
        urlDetails=urlsplit(config.AI_ENDPOINT)

        ipAddr = list([])
        try:
            IP(urlDetails.hostname)
        except ValueError:
            res = await resolver.query(urlDetails).hostname
            ipAddr.extend(res)
        else:
            ipAddr.append(config.AI_ENDPOINT)
        ports = list([])
        if isinstance(urlDetails.port,int):
            ports.append(urlDetails.port)
        elif urlDetails.scheme == "https" or urlDetails.scheme == "wss" or urlDetails.scheme == "oci":
            ports.append(443)
        elif urlDetails.scheme == "http" or urlDetails.scheme == "ws":
            ports.append(80)
        else:
            ports.append(80)
            ports.append(443)
        for ip in ipAddr:
            for port in ports:
                tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    tcp_socket.connect(ip, port)
                except socket.error:
                
                finally:
                    tcp_socket.close()
                if http3_supported:
        if config.AI_HTTP3:
            for ip in ipAddr:
                for port in ports:
                    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    try:
                        udp_socket.connect(ip, port)
                    except socket.error:
                    
                    finally:
                        udp_socket.close()

        pass
    def test_otel(self):
        pass
    def test_oidc(self):
        pass