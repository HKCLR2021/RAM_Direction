#include <iostream>
//#include <Python.h>
#include <string>
#include "/home/adminis/anaconda3/envs/graspnet/include/python3.7m/Python.h"
using namespace std;


//int main(int, char**) {
int main() {
    Py_Initialize();
    //PySys_SetPath(L"/home/adminis/anaconda3/envs/graspnet/");
    PyRun_SimpleString("import os");
    PyRun_SimpleString("import cv2");
    PyRun_SimpleString("import numpy as np");
    PyRun_SimpleString("import matplotlib.pyplot as plt");
    PyRun_SimpleString("import copy");
    PyRun_SimpleString("from PIL import Image, ImageStat,ImageEnhance");
    PyRun_SimpleString("import argparse");
    PyRun_SimpleString("import sys");
    PySys_SetPath(L"/media/adminis/74e98a57-1d79-48a7-aa9e-f26c1aa4ca9c/2023/RAM缺口/c++/");
    //PyRun_SimpleString("print(sys.path)");

    PyObject *mod = PyImport_ImportModule("line_c");
    //PyObject* mod = PyImport_ImportModule("line_all");
    if (mod == nullptr)
    {
        PyErr_Print();
        std::exit(1);
    }

    
    cout << "[INFO] Get Module" << endl;
    PyObject *pFunction = PyObject_GetAttrString(mod, "image_infer");
    if (pFunction == nullptr){
        cout << "[Error] Import function error" << endl;
        return -1;
    }
    
    cout << "[INFO] Get Function" << endl;

    PyObject *args = PyTuple_New(1);
    //PyObject *args1 = PyUnicode_FromString("shot_normal_5_Color.png"); //图片路径
    PyObject *args1 = PyUnicode_FromString("/media/adminis/74e98a57-1d79-48a7-aa9e-f26c1aa4ca9c/2023/RAM缺口/c++/shot_inverse_1_Color.png"); //图片路径

    PyTuple_SetItem(args, 0, args1);

    PyObject *pRet = PyObject_CallObject(pFunction, args);

    PyObject *iter = PyObject_GetIter(pRet);

    
    while(true)
    {
        PyObject *next = PyIter_Next(iter);
        if (!next) {
            // nothing left in the iterator
            break;
        }
        if(!PyList_Check(next))
        {
            // error, we were expecting a list value
        }
//        PyObject *res = PyList_AsTuple(next);
        PyObject *iter2 = PyObject_GetIter(next);
        while(true)
        {
            PyObject *next2 = PyIter_Next(iter2);
            if(!next2)
                break;
            if (!PyFloat_Check(next2)) {
                // error, we were expecting a floating point value
            }
            double foo = PyFloat_AsDouble(next2);
            cout << foo << " ";
        }
        cout << endl;
    }
    
    
    Py_Finalize();
}
