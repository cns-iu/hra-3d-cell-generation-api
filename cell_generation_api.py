from flask import Flask, request, Response
import subprocess
import os


app = Flask(__name__)


@app.route("/mesh-3d-cell-population", methods=['POST'])
def download_csv_direct():
    
    csv_data = ""

    # parse post request
    request_content_type = request.headers.get('Content-Type')
    if (request_content_type == 'application/json'):
        data = request.json
        glb_file_url = data["file"]
        glb_file = os.path.split(glb_file_url)[1]
        glb_stem = os.path.splitext(glb_file)[0]
        scene_node = data["file_subpath"]
        num_nodes = data["num_nodes"]

        if "node_distribution" in data:
            node_distribution = data["node_distribution"]
            
            # find the dir of the python file, add prefix
            cmd = ['./generate_cell_ctpop', glb_stem, scene_node]
            for i, (k, v) in enumerate(node_distribution.items()):
                cmd.extend([k, str(int(v*num_nodes))])
            # Invoke compiled exe.
            print(cmd)
            result = subprocess.run(cmd, capture_output=True)
            print('success')
            csv_data = result.stdout
            print(csv_data)

    
    else:
        return "Content type is not supported."
    

    # Create a CSV string from the user data
    # with open(output_file_name, 'r') as f:
    #     csv_data = f.read()
    # Ouput csv as response
    response = Response(csv_data, content_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=download.csv"

    return response
 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)