""" Setup for pypoint """

from setuptools import setup

setup(
  name='pypoint',
  version='0.1',
  description='Point API',
  long_description='Python implementation of Minut Point API.',
  url='',
  author='Viktor Nilsson',
  author_email='viktor.w.nilsson@gmail.com',
  license='',
  classifiers=[
    'Topic :: Home Surveillance',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
  ],
  keywords='point minut',
  install_requires=[''],
  packages=['pypoint'],
  zip_safe=True,
  entry_points={
    'console_scripts': [
      'pypoint=pypoint.__main__:main'
    ]
  })
