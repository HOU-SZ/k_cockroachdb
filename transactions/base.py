from abc import ABC, abstractmethod
from models import database

class BaseTransaction(ABC):
    MAX_ATTEMPTS = 10

    def __init__(self):
        pass

    # def execute(self, *args, **kwargs):
    #     def execute_transaction(db_ref):
    #         return self._execute_transaction(*args, **kwargs)

    #     outputs = database.run_transaction(
    #         execute_transaction, max_attempts=10
    #     )

    
    def execute(self, *args, **kwargs):
        def thunk(db_ref):
            return self._execute_transaction(*args, **kwargs)
        return database.run_transaction(thunk, max_attempts=10)

    # @database.transaction()
    # def execute(self):
    #     print(f"model: {type(database)}")
    #     return self._execute_transaction()

    @abstractmethod
    def _execute_transaction(self, *args, **kwargs):
        pass
