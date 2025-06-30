cmake_minimum_required(VERSION 3.5)
project(dijkstra_algorithm)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

add_subdirectory(pybind11)
pybind11_add_module(dijkstra main.cpp)
