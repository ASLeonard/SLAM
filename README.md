# *S*quare *L*attice Tile *A*ssembly *M*odel (SLAM)

Note this is dependent on
> matplotlib

> c++11


## Install

This should work
```bash
cd /path/to/download
tar xvzf SLAM-0.2.0.tar.gz (or otherwise extract it)
cd /SLAM-0.2.0
python setup.py install --user 
```
ignore the compiler warnings

---

## Usage

Should (in theory) be able to use like 

TestScript.py
```python
#!/usr/bin/env python
import polyominomodel
polyominomodel.GrowPoly([1,1,1,1,2,0,0,0])
```

### Examples

Some nice examples to try

* [1,2,3,3,4,0,0,0]
* [1,5,3,0,2,4,0,0,6,0,0,0]
* [1,1,1,1,2,0,2,0]
* [1,1,1,1,2,0,3,0,4,9,5,9,6,7,7,7,8,0,9,0,10,0,0,0]
    
### Advanced bits

Can also pass additional arguments to GrowPoly

* tile_labels = False/True -> labels the tile edges
* write_it = String-> writes the animated gif of this name to the local directory
* fps_par  = float -> the number of frames per second in the written gif


---

## Misc

Homepage!

https://www.tcm.phy.cam.ac.uk/profiles/asl47/
