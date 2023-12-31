from src.mlproject.logger  import logging
from src.mlproject.exception import CustomException
import sys

from src.mlproject.components.data_ingestion import DataIngestion
from src.mlproject.components.data_transformation import DataTransformation





if __name__=="__main__":
    logging.info("the execution has started")
    
    try:
        data_ingestion= DataIngestion()
        train_data_path,test_data_path=data_ingestion.initiate_data_ingestion()
        
        data_transformation=DataTransformation()
        data_transformation.initiate_data_transformation(train_data_path,test_data_path)
        
        
       
        
    
    except Exception as e:
        logging.info("custom exception ")
        raise CustomException(e,sys)    