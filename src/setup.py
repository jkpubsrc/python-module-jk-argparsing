from setuptools import setup


def readme():
	with open('README.rst') as f:
		return f.read()


setup(name='jk_argparsing',
	version='0.2017.7.22',
	description='This is a logging framework',
	author='Jürgen Knauth',
	author_email='pubsrc@binary-overflow.de',
	license='Apache 2.0',
	url='https://github.com/jkpubsrc/python-module-jk-argparsing',
	download_url='https://github.com/jkpubsrc/python-module-jk-argparsing/tarball/0.2017.7.22',
	keywords=['exec', 'command'],
	packages=['jk_argparsing'],
	install_requires=[
	],
	include_package_data=True,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Programming Language :: Python :: 3.5',
		'License :: OSI Approved :: Apache Software License'
	],
	long_description=readme(),
	zip_safe=False)

