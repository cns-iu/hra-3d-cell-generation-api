# 3d-cell-generation-api

**Version:** 1.0.0

**Release date:** 15 June 2024

## Overview:
As the core algorithms for the paper *Constructing and Using Cell Type Populations for the Human Reference Atlas*, generating 3D cells inside anatomical structures includes two steps: estimating the number of cells in anatomical structures and generating the location of the cells inside the anatomical structures. We design an algorithm for the cell type estimation based on the experimental datasets by using the collision detection API https://github.com/hubmapconsortium/hra-tissue-block-annotation as well as a 3D cell generation algorithm using the Computational Geometry Algorithm Library (CGAL). This project provides 
1. the proposed algorithm for randomly generate 3D cell locations inside any mesh of anatomical structures using CGAL.
2. an Python API using Flask to generate 3D cells given the distribution of the cells and the mesh of the anatomical structure. 

## Installation Instructions
1. CMake
    ```bash
    sudo apt-get cmake
    ```
2. Boost
    ```bash
    sudo apt-get update
    sudo apt-get install libboost-all-dev
    ```
3. GMP
    ```bash
    sudo apt-get install libgmp-dev
    ```
4. MPFR
    ```bash
    sudo apt-get install libmpfr-dev
    ```
5. CGAL
    ```bash
    sudo apt-get install libcgal-dev
    ```
6. Eigen3
    ```bash
    sudo apt install libeigen3-dev
    ```

7. Flask
    ```bash
    pip3 install flask
    ```

## Compilation

We use CMake to configure the program with third-party dependencies and generate the native build system by creating a CMakeLists.txt file. 

1. for C++ server:
    ```bash
    cd $server
    mkdir build
    cd build
    cmake ..
    make
    ```
    Then, copy the binary executable to the main directory
    ```bash
    cp generate_cell_ctpop ../../
    ```

## Usage

1. Start Python API:
    ```bash
    python3 cell_generation_api.py
    ```

## Example

 POST http://server_ip:port/mesh-3d-cell-population
 - JSON request example:
```json
{
    "file": "https://ccf-ontology.hubmapconsortium.org/objects/v1.2/VH_F_Kidney_L.glb",
    "file_subpath": "VH_F_renal_pyramid_L_a",
    "num_nodes": 10,
    "node_distribution": {
        "KEY1": 0.1,
        "KEY2": 0.3
    }
}
```

- Request as a CURL command:
```bash
curl -d '@examples/request_example.json' -H "Content-Type: application/json" -X POST http://localhost:8000/mesh-3d-cell-population
```
- CSV/text response example:
```text
x, y, z, cell_type
0.0579039,0.269139,-0.103702,KEY1
0.0532916,0.258096,-0.104511,KEY2
0.0520264,0.279228,-0.110894,KEY2
0.0568783,0.264194,-0.10985,KEY2
```

## Docker
