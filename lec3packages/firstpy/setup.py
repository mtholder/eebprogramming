from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='firstpy',
      version=version,
      description="just learning",
      long_description="""\
no long desc""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='bioinformatics',
      author='Mark T. Holder',
      author_email='mtholder@gmail.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      test_suite='firstpy.tests'
      )
