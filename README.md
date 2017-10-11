# Square Lattice tile Assembly Model (SLAM)

Note this module is dependent on
> matplotlib
> c++11 (and a suitably recent compiler)


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

### Functions

```python
GenerateGenotype
GenerateBDGenotype
GraphAssemblyOutcome
GrowPoly
```

### Examples

Some other nice examples to try

* SIFs
  * [0,0,1,0,2,0,0,3,0,4,0,5,7,6,0,0,0,0,8,0]
  * [1,1,1,1,2,0,3,0,4,9,5,9,6,7,7,7,8,0,9,0,10,0,0,0]
* Loops
  * [1,2,3,3,4,0,0,0]
  * [1,5,3,0,2,4,0,0,6,0,0,0]
* Nested Loops
  * [1,1,1,1,0,3,2,5,0,0,6,4]
  * [1,2,3,5,4,7,0,0,0,0,8,6]
* Unbounds
  * [1,1,1,1,2,0,2,0]
  * [1,2,0,3,0,4,0,4]
* Sterics
  * [0,5,2,0,1,3,0,0,1,0,0,4,0,0,0,6]
  * [1,3,0,0,4,5,2,0,0,0,0,6]


    
### Advanced bits

More information can be found via source or using 

```python
help(NAME_OF_FUNCTION)
```
in an interactive setting

---

## Misc

Homepage!

https://www.tcm.phy.cam.ac.uk/profiles/asl47/
