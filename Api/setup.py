from distutils.core import setup, Extension
setup(name = 'VectorModule', version = '1.0',  \
   ext_modules = [Extension('VectorModule', ['MatrixMul.c'])])