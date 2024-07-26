from flask import Flask, request, Response, make_response
import subprocess
import os


# Naive Hashing for url
def convert_url_to_file(url):
    # Replace illegal chars using underscore
    illegal_chars = ['/', ':', '@', '&', '*']
    
    for c in illegal_chars:
        url = url.replace(c, '_')
    
    return url

# Preprocessed body directory with OFF files
body_dir = "./model/all_preprocessed_off_models"

app = Flask(__name__)

@app.route("/mesh-3d-cell-population", methods=['POST'])
def download_csv_direct():
    
    csv_data = ""

    # parse post request
    request_content_type = request.headers.get('Content-Type')
    if (request_content_type == 'application/json'):
        data = request.json
        glb_file_url = data["file"]
        
        # glb_file = os.path.split(glb_file_url)[1]
        glb_file = convert_url_to_file(glb_file_url)
        glb_stem = os.path.splitext(glb_file)[0]

        if not os.path.exists(os.path.join(body_dir, glb_stem)):
            response = make_response('Submitted GLB is not preprocessed. This server does not process GLB files on the fly', 501)
            return response
        
        scene_node = data["file_subpath"]
        num_nodes = data["num_nodes"]

        if "node_distribution" in data:
            node_distribution = data["node_distribution"]
            
            # find the dir of the python file, add prefix
            cmd = ['./generate_cell_ctpop', glb_stem, scene_node]
            for i, (k, v) in enumerate(node_distribution.items()):
                cmd.extend([k, str(int(v*num_nodes))])
            
            # Invoke compiled exe.
            result = subprocess.run(cmd, capture_output=True)

            if result.returncode != 0:
                response = make_response('Error processing', 500)
            else:
                csv_data = result.stdout

                # Ouput csv as response
                response = Response(csv_data, content_type="text/csv")
                response.headers["Content-Disposition"] = "attachment; filename=download.csv"
        else:
            response = make_response('Malformed JSON. node_distribution is a required field.', 400)

    
    else:
        response = make_response('Only application/json content type is supported.', 400)

    return response
 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)