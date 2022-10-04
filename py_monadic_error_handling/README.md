# Py Monadic Error Handling Documentation

## Instalation
<p>The library is available via pip through the following command:</p>

```
pip install py-monadic-error-handling
```

## How to use
<p>First import the safe decorator from py_monadic_error_handling.</p>

```
from py_monadic_error_handling import safe
```

<p>Then decorate your functions with the safe decorator.</p>

```
@safe
def func1(n1, n2): 
    return n1 + n2

@safe
def func2(n1, n2): 
    return n1 / n2
```

<p>Each of those functions will return a Ok or Err object, witch are subclasses of Result and may take Ok or Err objects as parameters.</p>
<p>If they return a Ok object, the function executed with no errors and the value can be accessed via the unwrap method.</p>

```
res = func1(1, 0).unwrap()
print(res)
>>> 1
```

<p>If they return a Err object, the function executed with an error and the error can be raised via the unwrap method.</p>
<p>unwrap takes no arguments and raise an exception or returns any</p>

```
res = func2(1, 0).unwrap()
>>> ZeroDivisionError: division by zero
```

<p>You can access the value of the Ok object directly by using the Ok property or the error type in an Err object directly by using the Err property.</p>

```
res = func1(1, 0).Ok
print(res)
>>> 1
res = func2(1, 0).Err
print(res)
>>> division by zero
```

<p>You can know if the function returned a Ok or Err object by using the is_ok and is_err methods.</p>
<p>Both methods take no arguments and return a bool</p>

```
res = func1(1, 0).is_ok()
>>> True
res = func2(1, 0).is_err()
>>> True
```

<p>You can safely unwrap an Ok or Err object with the unwrap_or method.</p>
<p>unwrap_or takes one argument of any type.</p>
<p>If the object is an instance of Ok, it returns object.Ok.</p>
<p>If the object is an instance of Err, it returns the argument you entered.</p>

```
res = func1(1, 0).unwrap_or(-1)
print(res)
>>> 1
res = func2(1, 0).unwrap_or(-1)
print(res)
>>> -1
```

<p>You can safely unwrap an Ok or Err object with the unwrap_or_else method.</p>
<p>unwrap_or_else takes a function as its argument.</p>
<p>The function takes an exception as its argument and may or may not return a value.</p>
<p>If the object is an instance of Ok, it returns object.Ok.</p>
<p>If the object is an instance of Err, it executes the function with the object.Err as its parameter and return its return value.</p>

```
def handle_error(e):
    print(e)
    return -1

res = func1(1, 0).unwrap_or_else(handle_error)
print(res)
>>> 1
res = func2(1, 0).unwrap_or_else(handle_error)
>>> division by zero
print(res)
>>> -1
```

## Railway Error Handling
<p>By chaining functions decorated with safe, each function will excecute and if there is an error, it will return an Err object that will be caried through every function that depends on its return without executing them, othewise it will return an Ok value that can be taken as normal as argument for any other function decorated with safe</p>
    
```
n1 = func1(1, 0)
>>> Ok(1)
n2 = func1(2, -2)
>>> Ok(0)
n3 = func2(n1, n2)
>>> Err(ZeroDivisionError)
n4 = func1(n3, 3)
>>> Err(ZeroDivisionError)
n5 = func1(n2, n1)
>>> Ok(0)
```

<p>In this exemple, func1(n3, 3) is never executed because it depends on the return of a function that executed with an error, but func1(n1, 4) executes, because even though it executes later on the chain, it depends only on the return of functions that executed without any errors</p>