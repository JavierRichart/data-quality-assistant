from abc import ABC, abstractmethod

import pandas as pd

class BaseValidator(ABC):

    @abstractmethod
    def validate(self, dataframe: pd.DataFrame):
        pass