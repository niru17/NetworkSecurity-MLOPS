import os
import sys

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact, DataValidationArtifact,ModelTrainerArtifact
from networksecurity.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig, DataTransformationConfig,DataValidationConfig,ModelTrainerConfig

from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR

class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        
    def start_data_ingestion(self):
        try:
            dataingestionconfig=DataIngestionConfig(self.training_pipeline_config)
            logging.info("Initiate the data ingestion")
            data_ingestion=DataIngestion(dataingestionconfig)
            dataingestionartifact=data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Inititation Completed and artifact: {dataingestionartifact}")
            return dataingestionartifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=data_validation_config)
            logging.info("Initiate the data Validation")
            data_validation_artifact=data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact=data_validation_artifact,
            data_transformation_config=data_transformation_config)
            
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact)->ModelTrainerArtifact:
        try:
            self.model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(
                training_pipeline_config=self.training_pipeline_config
            )

            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )

            model_trainer_artifact = model_trainer.initiate_model_trainer()

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)