import setuptools

setuptools.setup(
	name="PicoLCD",
	version="0.1.3b1",
	author="James Edington",
	author_email="james@ishygddt.xyz",
	description="Library for interacting with the PicoLCD USB LCD screens",
	packages=setuptools.find_packages(),
	py_modules=["PicoLCD"],
	include_package_data=True,
	classifiers=[
	 "Development Status :: 3 - Alpha",
	 "License :: OSI Approved :: MIT License"
	],
	install_requires=['pyusb', 'pypsf==0.3.2', 'Pillow']
)
