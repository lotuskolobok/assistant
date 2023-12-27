from setuptools import setup, find_namespace_packages

setup(
    name='Assistant_bot',
    version='1',
    description='Assistant with a command line interface',
    url='https://github.com/lotuskolobok/assistant',
    author='Psar Yelyzaveta',
    license='MIT',
    include_package_data=True,
    packages=find_namespace_packages(),
    install_requires=['markdown'],
    data_files=[("assistant", ["assistant/classes.py", "assistant/main.py",
                "assistant/normalize.py", "assistant/notes.py", "assistant/scan.py", "assistant/sort.py"])],
    entry_points={'console_scripts': ['assistant = assistant.main:assistant']}
)