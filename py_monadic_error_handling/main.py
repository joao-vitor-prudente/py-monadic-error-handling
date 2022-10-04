from abc import ABC

class Result(ABC):
    def is_ok(self) -> bool:
        return isinstance(self, Ok)
    
    def is_err(self) -> bool:
        return isinstance(self, Err)
    
    def unwrap(self) -> any:
        if self.is_ok(): return self.Ok
        raise self.Err
    
    def unwrap_or(self, default: any) -> any:
        return self.Ok if self.is_ok() else default
    
    def unwrap_or_else(self, func: callable) -> any:
        return self.Ok if self.is_ok() else func(self.Err)
        

class Ok(Result):
    def __init__(self, Ok: any):
        self.Ok, self.Err = Ok, None
    
    def __repr__(self) -> str:
        return f"Ok({self.Ok})"


class Err(Result):
    def __init__(self, Err: Exception):
        self.Err, self.Ok = Err, None
    
    def __repr__(self) -> str:
        return f"Err({self.Err})"


def safe(func: callable) -> callable:

    def wrapper(*args, **kwargs) -> Ok | Err:
        args: list[Ok | Err] = [Ok(arg) if not isinstance(arg, Result) else arg for arg in args]
        kwargs: dict[any, Ok | Err] = {k: Ok(v) if not isinstance(v, Result) else v for k, v in kwargs.items()}
        
        all_args: list[Ok | Err] = args + list(kwargs.values())
        exceptions: list[Err] = [arg for arg in all_args if isinstance(arg, Err)]

        if exceptions: return exceptions[0]

        args: list = [arg.unwrap() for arg in args]
        kwargs: dict = {k: v.unwrap() for k, v in kwargs.items()}

        try: return Ok(func(*args, **kwargs))
        except Exception as e: return Err(e)

    return wrapper
