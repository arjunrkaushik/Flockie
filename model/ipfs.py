# import ipfsApi as ipfs
# import requests
# try:
#
#     # api = ipfs.connect('/ip4/127.0.0.1/tcp/5001/http','api/v0')
#     # print(api)
#     api = ipfs.Client('127.0.0.1',5001)
#     print(api)
#     res = api.add('welcome.txt')
#     print(res)
#     r = api.pin.add(res['Hash'])
#     # res = api.add('welcome.txt')
#     # print(res)
#     # s = api.pin_add('QmXCVVqBVryrbvJkxMtPZnDQADUno3RpT2CYn3YrQXCKPa')
#     # print(s)
#     # api.pin_ls(opts={'type':'all'})
# except ipfs.exceptions.ConnectionError as ce:
#     print(str(ce))

from ipyfs import Files,Add  # + Etc.

# Host and port can be modified for each IPyFS controller.
files = Files(
    host="http://localhost",  # Set IPFS Daemon Host
    port=5001  # Set IPFS Daemon Port
)
# files.mkdir(path="/test")
Add('welcome.txt')
files.ls()
