import setuptools


with open('README.md') as f:
    README = f.read()

# doesn't work with circleci for some reason?
# with open("requirements.txt") as f:
#     REQUIREMENTS = [line.strip() for line in f if line.strip()]

REQUIREMENTS = [
    "numpy",
    "requests",
    "protobuf==3.3.0"
]


setuptools.setup(
  name='qcware',
  packages=setuptools.find_packages(exclude=("tests", "docs")),
  version='0.2.19',
  description='Functions for easily interfacing with the QC Ware Platform from Python',
  long_description=README,
  long_description_content_type='text/markdown',
  author='QC Ware Corp.',
  author_email='info@qcware.com',
  url='https://github.com/qcware/platform_client_library_python',
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
