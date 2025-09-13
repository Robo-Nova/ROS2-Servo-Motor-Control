from setuptools import find_packages, setup

package_name = 'servo_motor_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ali-khaleghi',
    maintainer_email="ali.khaleghi.Original@gmail.com",
    description="Greetings, I'm Ali Khaleghi. Feel free to explore my GitHub projects at Robo-Nova.",
    license='Apache=2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	'servo_motor_control = servo_motor_controller.servo_motor_control:main',
        ],
    },
)
