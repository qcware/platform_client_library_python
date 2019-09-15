from distutils.core import setup
import setuptools


with open('README.md') as f:
    README = f.read()

with open("requirements.txt") as f:
    REQUIREMENTS = [line.strip() for line in f if line.strip()]

setup(
  name='qcware',
  packages=['qcware'],
  version='0.2.19',
  description='Functions for easily interfacing with the QC Ware Platform from Python',
  long_description=README,
  long_description_content_type='text/markdown',
  author='QC Ware Corp.',
  author_email='info@qcware.com',
  url='https://github.com/qcware/platform_client_library_python',
  download_url='https://github.com/qcware/platform_client_library_python/tarball/0.2.19',
  keywords=['quantum', 'computing', 'cloud', 'API'],
  test_suite="tests",
  install_requires=REQUIREMENTS,
  include_package_data=True,
  classifiers=[
      "Programming Language :: Python :: 3",
      "Operating System :: OS Independent",
  ],
  project_urls={
      "Source": "https://github.com/qcware/platform_client_library_python",
      "Docs": "https://qcware.readthedocs.io"
  }
)
