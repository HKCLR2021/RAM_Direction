cmake_minimum_required(VERSION 3.0.0)
project(ori_detect VERSION 0.1.0)

IF(NOT CMAKE_BUILD_TYPE)
  SET(CMAKE_BUILD_TYPE Release)
ENDIF()

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

#set(PYTHON_INCLUDE_DIRS "/home/adminis/anaconda3/include/python3.8/")
set(PYTHON_INCLUDE_DIRS "/home/adminis/anaconda3/envs/graspnet/include/python3.7m/")
#set(PYTHON_INCLUDE_DIRS "/home/adminis/anaconda3/include/python/")
INCLUDE_DIRECTORIES(${PYTHON_INCLUDE_DIRS})
#link_directories(/home/adminis/anaconda3/lib/python3.8/config-3.8-x86_64-linux-gnu)
link_directories(/home/adminis/anaconda3/envs/graspnet/lib/python3.7/config-3.7m-x86_64-linux-gnu)
#set(PYTHON_LIBRARIES "/home/adminis/anaconda3/lib/libpython3.8.so")
set(PYTHON_LIBRARIES "/home/adminis/anaconda3/envs/graspnet/lib/libpython3.7m.so")

#include(CTest)
#enable_testing()

add_executable(ori_detect main.cpp)

target_link_libraries(ori_detect ${PYTHON_LIBRARIES})

#set(CPACK_PROJECT_NAME ${PROJECT_NAME})
#set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
#include(CPack)
