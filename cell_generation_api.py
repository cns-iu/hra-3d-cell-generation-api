from flask import Flask, request
import subprocess
import os


@app.route('/mesh-3d-cell-population', methods=['POST'])
def handle_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.json
        glb_file_url = data["file"]
        glb_file = os.path.split(glb_file_url)[1]
        glb_stem = os.path.splitext(glb_file)
        
        scene_node = data["file_subpath"]
        num_nodes = data["num_nodes"]
        
        if "node_distribution" in data:
            node_distribution = data["node_distribution"]
            for i, (k, v) in enumerate(node_distribution.items()):
                if i == 0:
                    subprocess.call(["./cell-generation", glb_stem, scene_node, k, int(v*num_nodes), 0])
                else:
                    subprocess.call(["./cell-generation", glb_stem, scene_node, k, int(v*num_nodes), 1])
    else:
        return "Content type is not supported."