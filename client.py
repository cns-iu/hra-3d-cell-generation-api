import json
import requests
import urllib.request

download_csv_url = 'http://localhost:8000/mesh-3d-cell-population'

post_request = {
  "file": "https://VH_F_Kidney_L.glb",
  "file_subpath": "VH_F_renal_pyramid_L_a",
  "num_nodes": 400,
 "node_distribution": {
  "KEY1": 0.1,
  "KEY2": 0.3 
 }
}


r = requests.post(url=download_csv_url, json=post_request)

print(r.content)