## designpatterns/strategyValidation.py
# @Import: designpatterns.strategyValidation
# @Author: @Grimoors
# @Date: 2024-04-22
# @Last Modified by: @Grimoors
# @Last Modified time: 2024-04-22 - 16:56 IST
# @Title: Strategy Design Pattern Form Validator
# @Description: Strategy Design Pattern Form Validator for Frontend Validation and Backend Validation

from abc import ABC, abstractmethod
import time
from datetime import datetime
import re

class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, data):
        pass

class NonEmptyValidation(ValidationStrategy):
    def validate(self, data):
        return data is not None and data != ""

class NumericValidation(ValidationStrategy):
    def validate(self, data):
        try:
            float(data)
            return True
        except ValueError:
            return False

class DateValidation(ValidationStrategy):
    def validate(self, day, month, year):
        try:
            datetime(year=int(year), month=int(month), day=int(day))
            return True
        except ValueError:
            return False

class UPIReferenceValidation(ValidationStrategy):
    def __init__(self):
        # Compile the regular expression for 12-digit UPI Reference ID
        self.pattern = re.compile(r'^\d{12}$')

    def validate(self, data):
        """Validate the UPI Reference ID to ensure it is exactly 12 digits."""
        if self.pattern.match(data):
            return True
        else:
            return False

class PaymentTypeValidation(ValidationStrategy):
    def validate(self, data):
        """Validate the payment type to ensure it is either 'Credit' or 'Debit'."""
        return data in ["Credit", "Debit"]
