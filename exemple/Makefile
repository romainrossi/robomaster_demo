## Sample Makefile to be placed at the ROS Workspace root

all: build

build: Makefile
	colcon build --symlink-install

rebuild: clean build

clean:
	rm -fR build/
	rm -fR install/

rosdep_update:
	rosdep update

rosdep_install:
	rosdep install --from-paths src --ignore-src -r -y

extdep_install:
	sudo apt install libopus-dev python3-pip
	python3 -m pip install -U numpy==1.24.4 numpy-quaternion pyyaml
	python3 -m pip install git+https://github.com/jeguzzi/RoboMaster-SDK.git
	python3 -m pip install git+https://github.com/jeguzzi/RoboMaster-SDK.git#"egg=libmedia_codec&subdirectory=lib/libmedia_codec"

run:
	ros2 launch robomaster_demo epcore_square.launch

.PHONY: build clean
