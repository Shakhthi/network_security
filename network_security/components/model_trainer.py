import sys
import os

from network_security.exception.exception_handler import NetworksecurityException
from network_security.logging.logger import logging

from network_security.entity.config_entity import ModelTrainerConfig
from network_security.entity.artifact_config import DataTransformationArtifact, ModelTrainerArtifact

from network_security.utils.ml_utils.model.estimator import NetworkModel
from network_security.utils.main_utils.utils import (
    save_object, load_object,
    load_numpy_array_data, evaluate_models
)
from network_security.utils.ml_utils.metric.classification_metric import get_classification_score

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier,
)

import mlflow
import dagshub
dagshub.init(repo_owner='Shakhthi', repo_name='network_security', mlflow=True)

class ModelTrainer:
    def __init__(self, 
                 model_trainer_config:ModelTrainerConfig,
                 data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("Model Trainer class initiated.")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e:
            raise NetworksecurityException(e,sys)
        
    def track_model(self, best_model, classificationmetric):
        try:
            logging.info("mlflow initiated.")
            with mlflow.start_run():
                f1_score = classificationmetric.f1_score
                precision_score = classificationmetric.precision_score
                recall_score = classificationmetric.recall_score

                mlflow.log_metric("f1", f1_score)
                mlflow.log_metric("precision", precision_score)
                mlflow.log_metric("recall", recall_score)
                mlflow.sklearn.log_model(best_model, "model")
        except Exception as e:
            raise NetworksecurityException(e, sys)
    
    def train_model(self,X_train,y_train,x_test,y_test):
        try:
            models = {
                "Random Forest": RandomForestClassifier(verbose=1),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),
            }
            params={
                "Decision Tree": {
                    'criterion':['gini', 'entropy', 'log_loss'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['gini', 'entropy', 'log_loss'],
                    
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,128,256]
                },
                "Gradient Boosting":{
                    # 'loss':['log_loss', 'exponential'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Logistic Regression":{},
                "AdaBoost":{
                    'learning_rate':[.1,.01,.001],
                    'n_estimators': [8,16,32,64,128,256]
                }
                
            }
            logging.info("Model and params are gathered.")
            model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=x_test,y_test=y_test,
                                            models=models,param=params)
            
            ## To get best model score from dict
            best_model_score = max(sorted(model_report.values()))

            ## To get best model name from dict
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]
            y_train_pred=best_model.predict(X_train)

            logging.info("Model Evaluation completed.")
            classification_train_metric=get_classification_score(y_true=y_train,y_pred=y_train_pred)

            # tracking train metric with mlflow 
            self.track_model(best_model, classification_train_metric)

            y_test_pred=best_model.predict(x_test)
            classification_test_metric=get_classification_score(y_true=y_test,y_pred=y_test_pred)

            # tracking test metric with mlflow
            self.track_model(best_model, classification_test_metric)

            logging.info("classification report ready.")
            preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
                
            model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)

            Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(self.model_trainer_config.trained_model_file_path, obj=Network_Model)
            
            #model pusher
            save_object("final_model/model.pkl",best_model)
            

            ## Model Trainer Artifact
            model_trainer_artifact=ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                                train_metric_artifact=classification_train_metric,
                                test_metric_artifact=classification_test_metric
                                )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e:
            raise NetworksecurityException(e, sys)
    
    
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            #loading training array and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact=self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact

            
        except Exception as e:
            raise NetworksecurityException(e,sys)
