cmake_minimum_required(VERSION 3.16)

find_package(Qt6 COMPONENTS Network REQUIRED)

add_library(PostRequest)
qt_add_qml_module(PostRequest
    URI PostRequest
    VERSION 1.0
    SOURCES post.cpp post.h
)

target_link_libraries(PostRequest
    PRIVATE Qt6::Network)


