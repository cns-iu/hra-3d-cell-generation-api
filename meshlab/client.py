import json
import requests
import urllib.request
from io import StringIO
import csv


def compute_exact_total_nodes(post_request):
	# handle float number rounding issue
	node_distribution = post_request['node_distribution']
	total_nodes = 0
	num_nodes = post_request['num_nodes']
	for key, value in node_distribution.items():
		total_nodes += int(value * num_nodes)
	return total_nodes


def generate_cells(post_request):
	download_csv_url = 'https://apfvtab7fp.us-east-2.awsapprunner.com/mesh-3d-cell-population'

	r = requests.post(url=download_csv_url, json=post_request)

	content = r.content.decode()
	file = StringIO(content)
	csv_data = csv.reader(file, delimiter=",")
	
	# skip csv header
	next(csv_data)

	# generate OFF file for the cells
	off_file_name = post_request['file_subpath'] + '.off'
	# total_nodes = post_request['num_nodes']
	total_nodes = compute_exact_total_nodes(post_request)
	with open(off_file_name, 'w') as file:
		file.write('OFF\n')
		file.write(str(total_nodes) + ' 0 0\n')
		for row in csv_data:
			file.write(row[0] + ' ' + row[1] + ' ' + row[2] + '\n')


if __name__ == "__main__":

	post_request_1 = {
		"file": "//https://ccf-ontology.hubmapconsortium.org/objects/v1.2/VH_M_Kidney_L.glb",
		"file_subpath": "VH_M_renal_column_L",
  		"num_nodes": 999,
 		"node_distribution": {
  		"KEY1": 0.9, 
		"KEY2": 0.1
		}
	}

	post_request_2 = {
		"file": "//https://ccf-ontology.hubmapconsortium.org/objects/v1.2/VH_M_Liver.glb",
		"file_subpath": "VH_M_diaphragmatic_surface",
  		"num_nodes": 1000,
 		"node_distribution": {
  		"KEY1": 1, 
		}
	}

	post_request_3 = {
		"file": "//https://ccf-ontology.hubmapconsortium.org/objects/v1.2/VH_M_Liver.glb",
		"file_subpath": "VH_M_gastric_impression_of_liver",
  		"num_nodes": 1000,
 		"node_distribution": {
  		"KEY1": 1, 
		}
	}
	
	generate_cells(post_request_1)
	generate_cells(post_request_2)
	generate_cells(post_request_3)
	