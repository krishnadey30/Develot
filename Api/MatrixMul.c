#include <Python.h>
#include <math.h>

static PyObject* Product(PyObject* self, PyObject* args)
{
    int numLines;       /* how many lines we passed for parsing */

    PyObject * Vector1; /* this will have the data of first vector */
    PyObject * Vector2;  /* this will have the data of first vector  */
    double value1,value2;

    /* the O! parses for a Python object (listObj) checked
       to be of type PyList_Type */
    if (! PyArg_ParseTuple( args, "O!O!", &PyList_Type, &Vector1,&PyList_Type, &Vector2))
    	return NULL;
    
    /* get the number of lines passed to us */
    numLines = PyList_Size(Vector1);

    /* should raise an error here. */
    if (numLines < 0)
    	return NULL; /* Not a list */

    /* iterate over items of the list, grabbing strings, and parsing
       for numbers */
    double sum=0;
    double mod_vec1=0,mod_vec2=0;
    for (int i=0; i<numLines; i++){
		/* retrieving the value */
		value1 = PyFloat_AsDouble( PyList_GetItem(Vector1, i) );
		value2 = PyFloat_AsDouble( PyList_GetItem(Vector2, i) );
        mod_vec1+=(value1*value1);/* calculating the x[i]^2 */
        mod_vec2+=(value2*value2); /* calculating the y[i]^2 */
		sum+=(value1*value2); /* calculating x[i]*y[i] */
	}
    mod_vec1=sqrt(mod_vec1); /*calculating the mod value of Vector 1*/
    mod_vec2=sqrt(mod_vec2); /*calculating the mod value of Vector 2*/
    double angle = sum/(mod_vec1*mod_vec2); /*calculating the angle between  & Vector 2 */
    return Py_BuildValue("d", angle);
}

static PyMethodDef VectorMethods[] = {
    { "Product", Product, METH_VARARGS, "Does Product" },
    { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef VectorModule = {
    PyModuleDef_HEAD_INIT,
    "VectorModule",
    "Module for Vector Dot Product",
    -1,
    VectorMethods
};

// Initializes our module using our above struct
PyMODINIT_FUNC PyInit_VectorModule(void)
{
    return PyModule_Create(&VectorModule);
}