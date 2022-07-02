from setuptools import setup, find_packages

setup(name='ucac4-convert',
      version='1.0.0',
      description='Convert UCAC4 Catalog',
      url='https://github.com/nvermaas/UCAC4-converter',
      author='Nico Vermaas',
      author_email='nvermaas@xs4all.nl',
      license='BSD',
      install_requires=['requests'],
      packages=find_packages(),
      include_package_data=True,
      entry_points={
            'console_scripts': [
                  'card-to-pano=ucac4-convert.main:main',
            ],
      },
      )