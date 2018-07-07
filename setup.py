import setuptools

setuptools.setup(
	name="PicoLCD",
	version="0.1.2b2",
	author="James Edington",
	author_email="james@ishygddt.xyz",
	description="Library for interacting with the PicoLCD USB LCD screens",
	py_modules=["PicoLCD"],
	classifiers=[
	 "Development Status :: 3 - Alpha",
	 "License :: OSI Approved :: MIT License"
	],
	install_requires=['pyusb']
)
