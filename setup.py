import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'django',
    'pgintranet',
    'djinn_forms',
    'djinn_likes',
    'djinn_contenttypes>=1.4.9',
    'easy-thumbnails',
    'django-image-cropping',
    ]

setup(name='djinn_news',
      version="1.3.0",
      description='Djinn Intranet News',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Framework :: Django",
          "Intended Audience :: Developers",
          "License :: Freely Distributable",
          "Programming Language :: Python",
          "Topic :: Internet :: WWW/HTTP :: Site Management",
          "Topic :: Software Development :: Libraries :: "
          "Application Frameworks"
      ],
      author='PythonUnited',
      author_email='info@pythonunited.com',
      license='beer-ware',
      url='https://github.com/PythonUnited/djinn_news',
      keywords='Djinn Core',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="djinn_news",
      entry_points="""\
      [djinn.app]
      urls=djinn_news:get_urls
      js=djinn_news:get_js
      """
      )
