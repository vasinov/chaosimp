from abc import ABC, abstractmethod


class Parser(ABC):
    @abstractmethod
    def to_ssm_document(self, experiment_path):
        pass