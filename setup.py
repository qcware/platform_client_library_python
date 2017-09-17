from distutils.core import setup
import setuptools


setup(
  name='qcware',
  packages=['qcware'],
  version='0.2.7',
  description='Functions for easily interfacing with the QC Ware Platform from Python',
  author='QC Ware Corp.',
  author_email='info@qcware.com',
  url='https://github.com/qcware/platform_client_library_python',
  download_url='https://github.com/qcware/platform_client_library_python/tarball/0.2.7',
  keywords=['quantum', 'computing', 'cloud', 'API'],
  classifiers=[],
  install_requires=[
    'protobuf',
  ],
)
