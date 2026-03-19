from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'scan_capture_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        (
            'share/ament_index/resource_index/packages',
            ['resource/' + package_name]
        ),
        (os.path.join('share', package_name), ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='vboxuser',
    maintainer_email='mmunoria@mtu.edu',
    description='ROS2 package for capturing LaserScan data and robot poses at waypoints',
    license='Apache-2.0',
    extras_require={
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'scan_capture_node = scan_capture_pkg.scan_capture_node:main',
            'keyboard_capture = scan_capture_pkg.keyboard_capture:main',
            'transform_node = scan_capture_pkg.transform:main'
        ],
    },
)
