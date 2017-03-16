from setuptools import setup

setup(
    name='morphsvc',
    packages=['morphsvc'],
    include_package_data=True,
    test_suite="tests",
    install_requires=[
        'flask==0.12',
        "requests>=2.8.1",
        "Flask-Cache==0.13.1",
        "Flask-Restful",
        "requests-cache==0.4.9",
        "flask-cors==2.0.0",
        "xmljson"
    ],
    setup_requires=[
    ],
    tests_require=[
    ]
)
