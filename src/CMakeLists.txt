cmake_minimum_required(VERSION 3.9)
project(CELL)

# set variables
set(CMAKE_BUILD_TYPE "Release")

# find packages
find_package(CGAL REQUIRED)
set(Boost_USE_STATIC_LIBS OFF) 
set(Boost_USE_MULTITHREADED ON)  
set(Boost_USE_STATIC_RUNTIME OFF) 
find_package(Boost 1.45.0 COMPONENTS filesystem)

# CTPop
add_executable(generate_cell_ctpop generate_cell_ctpop.cpp cell_generation.cpp)
target_include_directories(generate_cell_ctpop PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_link_libraries(generate_cell_ctpop CGAL::CGAL)

# CTPop skin
# add_executable(generate_cell_skin generate_cell_skin.cpp cell_generation.cpp)
# target_include_directories(generate_cell_skin PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
# target_link_libraries(generate_cell_skin CGAL::CGAL)

if(Boost_FOUND)
    include_directories(${Boost_INCLUDE_DIRS}) 
    target_link_libraries(generate_cell_ctpop ${Boost_LIBRARIES})
endif()
