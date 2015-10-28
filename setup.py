from setuptools import setup

requires = [
    'fedmsg',
]

setup(
    name='bugyou',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='https://github.com/kushaldas/autocloud',
    install_requires=requires,
    packages=[],
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
            "bugyou_consumer = bugyou.consumer:BugFilerConsumer",
        ],
   },
)
