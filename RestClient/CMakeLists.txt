cmake_minimum_required(VERSION 3.16)

project(Rest VERSION 0.1 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 COMPONENTS Core Quick Multimedia REQUIRED)

add_subdirectory(PostRequest)

qt_add_executable(appRest
    main.cpp
)
#set(QML_IMPORT_PATH ${CMAKE_SOURCE_DIR} ${CMAKE_BINARY_DIR} CACHE STRING "" FORCE)

qt_add_qml_module(appRest
    URI Rest
    VERSION 1.0
    QML_FILES main.qml 
)


set_target_properties(appRest PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER my.example.com
    MACOSX_BUNDLE_BUNDLE_VERSION ${PROJECT_VERSION}
    MACOSX_BUNDLE_SHORT_VERSION_STRING ${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}
    MACOSX_BUNDLE TRUE
    WIN32_EXECUTABLE TRUE
    MACOSX_BUNDLE_INFO_PLIST ${CMAKE_CURRENT_SOURCE_DIR}/Info.plist.in
)

target_compile_definitions(appRest
    PRIVATE $<$<OR:$<CONFIG:Debug>,$<CONFIG:RelWithDebInfo>>:QT_QML_DEBUG>)
target_link_libraries(appRest
    PRIVATE Qt6::Core Qt6::Quick Qt6::Multimedia PostRequestplugin)
