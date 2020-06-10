from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='aiofcopy',
    version='0.1.0',
    description='Useful tool to copy object files with progress callbacks.',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    packages=find_packages(),
    author='Yann Cabral',
    author_email='iamyanndias@gmail.com',
    keywords=['async', 'copy', 'file'],
    url='https://github.com/yanncabral/aiofcopy',
    download_url='https://pypi.org/project/aiofcopy/'
)

install_requires = [
    'aiofile'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)
