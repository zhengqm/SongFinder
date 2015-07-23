# Song Finder

A spectrum analysis based music finder.

Write-up: [Blog post]() (in Chinese)

## Demo

### Set up

``` python
In [1]: from SFEngine import *

In [2]: engine = SFEngine()
```

### Index

```
In [3]: engine.index('original')
```

### Search

For record0.wav:

``` python
In [4]: engine.search('record/record0.wav')
original/周杰伦-枫 73
original/周杰伦-枫 31
original/周杰伦-枫 10
original/周杰伦-枫 28
original/我要快樂 - 張惠妹 28
```

For record8.wav:

Result:

```python
In [5]: engine.search('record/record8.wav')
original/光良 - 童话 67
original/光良 - 童话 39
original/光良 - 童话 33
original/光良 - 童话 135
original/光良 - 童话 69
```


