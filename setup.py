from setuptools import setup, find_packages

requires = [
    'fedmsg',
]

setup(
    name='bugyou',
    version='0.1',
    description='Automated Bug Reporting Tool',
    author='Sayan Chowdhury',
    author_email='sayanchowdhury@fedoraproject.org',
    url='https://pagure.io/bugyou',
    license='GPLv3',
    install_requires=requires,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Environment :: Web Environment',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
    entry_points={
        'moksha.consumer': [
            "bugyou_consumer = bugyou.consumer:BugyouConsumer",
        ],
    },
)
