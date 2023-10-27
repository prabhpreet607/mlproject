import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
import sys
from dataclasses import dataclass
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.pipeline import Pipeline

from src.mlproject.logger import logging
from src.mlproject.exception import CustomException
import os

from src.mlproject.utils import save_obj


@dataclass
class DataTrandformationConfig():
    preprocessor_obj_file_path=os.path.join("artifacts","preprocessor.pkl")
    
   
class DataTransformation():
    def __init__(self):
        self.data_transformation_config=DataTrandformationConfig()
        
    
    def get_data_transformer_obj(self):
         
        '''
        this function is responsible for data transformation
        '''
    
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]
            
            num_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scalar",StandardScaler())
            
            ])
           
            
            cat_pipeline=Pipeline(steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scalar",StandardScaler(with_mean=False))
            ])
            
            logging.info(f"categorical_pipelines: {categorical_columns}")
            logging.info(f"numerical columns :{numerical_columns}")
            
            preprocessor=ColumnTransformer(
                [
                ("numerical_pipelines",num_pipeline,numerical_columns),
                ("categorical_pipelines",cat_pipeline,categorical_columns)
                ]
            )
            
            return preprocessor
            
            
        except Exception as e:
            raise CustomException(e,sys)    
        
        
    def initiate_data_transformation(self,train_path,test_path):
        
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            
            logging.info("Reading train and test file")
            
            preprocessing_obj=self.get_data_transformer_obj()
            
            target_column_name="math_score"
            numerical_columns = ["writing_score", "reading_score"]

            ## divide the train dataset to independent and dependent feature
            
            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]
            
            ## divide the test dataset to independent and dependent feature
            
            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            
            logging.info("Applying Preprocessing on training and test dataframe")
            
            input_feature_train_arry=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arry=preprocessing_obj.transform(input_feature_test_df)
            
            train_arr=np.c_
            [
                input_feature_train_arry,np.array(target_feature_train_df)
                
            ]
            
            test_arr=np.c_[
                input_feature_test_arry,np.array(target_feature_test_df)
            ]
            
            logging.info(f"Saved preprocessing object")

            save_obj(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (

                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
            
            
            
            
            
            
            
        except Exception as e:
            raise CustomException(e,sys)