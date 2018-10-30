#API functions

from abc import ABC, abstractmethod
import requests
import json
import configparser as cfparser
#import Configparser

class APIrequester(ABC):
    def __init__(self):
        #print("init base APIrequester")
        pass

    @abstractmethod
    def request(self):pass

    @abstractmethod
    def run(self):pass

    @abstractmethod
    def activate(self):pass
    @abstractmethod
    def inactivate(self):pass
    
    @abstractmethod
    def stop(self):pass
        
