import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='openapitools',
    version='0.0.2',
    author='Anton Shabouta',
    author_email='zloyusr@gmail.com',
    description='OpenAPI v3 Object Model and Helpers',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zloyuser/openapi-tools',
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ),
)
