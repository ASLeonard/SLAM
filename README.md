# **S**quare **L**attice Tile **A**ssembly **M**odel 




## Install

Not 100% sure yet, but download the release, extract, and then install
```
cd /path/to/download
tar xvzf SLAM-0.2.0.tar.gz
cd /SLAM-0.2.0
python setup.py install --user 
```
ignore the compile warnings

## Usage


No promises, but should work as so::
```
import polyominomodel
polyominomodel.GrowPoly([1,2,3,3,4,0,0,0],0)
```
