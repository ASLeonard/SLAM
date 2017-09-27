# *S*quare *L*attice Tile *A*ssembly *M*odel 

Note this is currently dependent on


## Install

Not 100% sure yet, but download the release, extract, and then install
```bash
cd /path/to/download
tar xvzf SLAM-0.2.0.tar.gz
cd /SLAM-0.2.0
python setup.py install --user 
```
ignore the compile warnings for now

## Usage

No promises, but should be able to use like 

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

    * write_it = False/True -> writes the animated gif to the local directory
    * fps_par  = float -> the number of steps per second in the written gif
