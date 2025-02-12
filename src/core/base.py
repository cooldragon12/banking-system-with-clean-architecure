from typing import TypeVar, Generic, List, Type

T = TypeVar('T')
class BaseRepository(Generic[T]):
    
    entity: Type[T]
    _data: List[T]
    
    def __init__(self):
        self._data = []

    def _add(self, entity: T):
        self._data.append(entity)
        return entity
    
    def find(self, value, by):
        for entity in self._data:
            if getattr(entity, by) == value:
                return entity
        return None
    
    def list(self):
        return self._data

    def save(self, entity: T):
        return self._add(entity)

    def __call__(self, *args, **kwds):
        return self.entity
    
class ValidationMixin:
    
    def validate(self, value):
        return value

    def __validate(self, value):
        value = self.validate(value)
        funcs = [func for func in dir(self) if callable(getattr(self, func)) and func.startswith('validate_')]
        for func in funcs:
            index = func.split('_')[-1]
            sub_value = getattr(self, index)
            getattr(self, func)(sub_value)
            
        return value

    def execute_validation(self, value):
        return self.__validate(value)

class BaseUseCase(ValidationMixin, Generic[T]):
    repository:BaseRepository[T] = None
    entity: Type[T] = None




