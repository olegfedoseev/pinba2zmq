try:
  from setuptools import setup, Extension
except ImportError:
  from distutils.core import setup, Extension

setup(name="proto_wrapper",
      version="1.0",
      packages=[
        
      ],
      package_dir={
        
      },
      ext_modules=[
        
          Extension("Pinba", ["pinba.cc", "pinba.pb.cc"], libraries=['protobuf']),
        
      ],
      test_suite="test.suite")