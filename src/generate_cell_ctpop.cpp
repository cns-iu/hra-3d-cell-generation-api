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
    // std::cout << file_path << PMP::volume(mesh) * 1e9 << std::endl;
    return mesh;
}


int main(int argc, char **argv)
{

    srand(time(0));

    if (argc < 3)
    {
        std::cout << "Please provide the surface mesh folder" << std::endl;
    }

    auto body_path = "./model/";
    std::string organ = std::string(argv[1]);
    std::string mesh_file_name = std::string(argv[2]);
    std::string cell_type = std::string(argv[3]);
    int cell_count = std::stoi(argv[4]);
    int append = std::stoi(argv[4]);

    std::ofstream points_csv;
    auto output_file_path = "./cell_location_" + organ + "_" + mesh_file_name + ".csv";
    
    if (append)
        points_csv.open(output_file_path, std::ios_base::app);
    else
    {
        points_csv.open(output_file_path);
        points_csv << "organ, anatomical structure, cell_type, x, y, z\n";
    }

    // skip Skin because skin is special
    if (organ.find("Skin") != std::string::npos || organ.find("skin") != std::string::npos)
    {
        ;
    }
    else
    {
        fs::path tmp = fs::path(body_path) / fs::path(organ) / fs::path(mesh_file_name);
        std::string file_path = tmp.string() + ".off";

        if (!fs::exists(file_path)) 
        {
            std::cout << file_path << " not exist" << std::endl;
            continue; 
        }

        std::cout << "generating " << cell_type << " count " << count << std::endl;
        Surface_mesh mesh = load_mesh(file_path);
        auto points = generate_cells(mesh, count);

        points_csv.close();
    }

}