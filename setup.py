from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='unimr.red5.protectedvod',
      version=version,
      description="Manage, protect and present your video/audio content with Plone but delegate the streaming to Red5",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video",
        "Topic :: Multimedia :: Sound/Audio",
        ],
      keywords='Plone Flash FLV MP3 Zope Streaming Red5 rtmp',
      author='Andreas Gabriel',
      author_email='gabriel@hrz.uni-marburg.de',
      url='http://svn.plone.org/svn/collective/unimr.red5.protectedvod',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['unimr', 'unimr.red5'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'iw.fss',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
