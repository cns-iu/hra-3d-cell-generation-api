#include "cell_generation.h"
#include <unordered_map>
#include <fstream>
#include <boost/filesystem.hpp>

namespace fs = boost::filesystem;


Surface_mesh load_mesh(std::string file_path)
{
    std::ifstream input(file_path);
    Surface_mesh mesh;

    if (!input || !(input >> mesh) || mesh.is_empty())
    {
        std::cerr << file_path << " Not a valid mesh" << std::endl;
    }
    // std::cerr << file_path << PMP::volume(mesh) * 1e9 << std::endl;
    return mesh;
}


int main(int argc, char **argv)
{

    srand(time(0));

    if (argc < 3)
    {
        std::cerr << "Please provide the organ and the scene node" << std::endl;
        return 0;
    }

    auto body_path = "./model/plain_manifold_filling_hole_v1.4";
    // std::string output_file_path = std::string(argv[1]);
    std::string organ = std::string(argv[1]);
    std::string mesh_file_name = std::string(argv[2]);
    // std::string cell_type = std::string(argv[4]);
    // int cell_count = std::stoi(argv[5]);

    // std::ofstream points_csv;
    // points_csv.open(output_file_path);
    // points_csv << "organ,anatomical structure,cell_type,x,y,z\n";
    std::cout << "x,y,z,Cell Type\n";

    for (int i = 3; i < argc; i += 2)
    {
        if (i + 1 >= argc) break;
        
        std::string cell_type = std::string(argv[i]);
        int cell_count = std::stoi(argv[i+1]);

        // skip Skin because skin is special
        if (organ.find("Skin") != std::string::npos || organ.find("skin") != std::string::npos)
        {
            // Fill code later
            ;
        }
        else
        {
            fs::path tmp = fs::path(body_path) / fs::path(organ) / fs::path(mesh_file_name);
            std::string file_path = tmp.string() + ".off";

            if (fs::exists(file_path))
            {
                Surface_mesh mesh = load_mesh(file_path);
                auto points = generate_cells(mesh, cell_count);
                
                std::cerr << "generating " << cell_type << " count " << cell_count << std::endl;
                // Write to csv file with random uuid as file name. 
                for (auto &p: points) 
                    // points_csv << organ << "," << mesh_file_name << "," << cell_type << "," << p[0] << "," << p[1] << "," << p[2] << "\n";
                    std::cout << p[0] << "," << p[1] << "," << p[2] << "," << cell_type << "\n";

            }
            else
            {
                // File path does not exist. 
                std::cerr << file_path << " not exist" << std::endl;
                std::cerr << "Cannot generating " << cell_type << " count " << cell_count << std::endl;

            }
        }

    }

    // points_csv.close();
    

}