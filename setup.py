from setuptools import setup, find_packages

requirements = ['requests']

setup(name='console_scripts',
      version='1.0.0',
      description='Convert UCAC4 Catalog',
      url='https://github.com/nvermaas/UCAC4_converter',
      author='Nico Vermaas',
      author_email='nvermaas@xs4all.nl',
      license='BSD',
      install_requires=requirements,
      packages=find_packages(),
      entry_points={
            'console_scripts': [
                  'ucac4-convert=ucac4_convert.main:main'
              ],
      })
