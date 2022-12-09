import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import pandas as pd

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification

from aopssop import IzdapAlgo


def izdap_basic_example():
    data = make_classification(n_samples=200, n_features=4,
                               n_informative=2, n_classes=2,
                               random_state=42)

    class_column = 'class'
    positive_class_label = 1
    probability_threshold = 0.1

    test_data = pd.DataFrame(data[0], columns=['col1', 'col2', 'col3', 'col4'])
    test_data[class_column] = pd.Series(data[1])

    algo = IzdapAlgo(probability_threshold)
    algo.fit(test_data, class_column=class_column, positive_class_label=positive_class_label)

    rules = algo.get_rules()
    print(rules[0])

    transformed_data = algo.transform(test_data)
    print(transformed_data.info())


def izdap_ieee_data():
    
    print("Experiment with IEEE_smart_crane")
              
    DATA_PATH = "../datasets/IEEE_smart_crane.csv"
    ieee_data = pd.read_csv(DATA_PATH)
    
    ieee_data = ieee_data.drop(columns=['Date'])
    print(ieee_data.info(verbose=False))
    
    X_train, X_test, y_train, y_test = train_test_split (ieee_data.drop(columns=['Alarm']), ieee_data.Alarm, 
                                                         test_size = 0.3, shuffle = False)
    
    clf = RandomForestClassifier(random_state=5)
    clf.fit(X_train, y_train)
    
    y_test_pred = clf.predict(X_test)
    y_test_proba = clf.predict_proba(X_test)
    
    print('Random forest without IZDAP preproccesing')
    print(metrics.classification_report(y_true=y_test, y_pred=y_test_pred, digits=6))
    print(f"ROC-AUC: {metrics.roc_auc_score(y_true=y_test, y_score=y_test_proba[:, 1])}")
    print(f"Accuracy: {metrics.accuracy_score(y_true=y_test, y_pred=y_test_pred)}")
    
    algo = IzdapAlgo(0.1)
    algo.fit(ieee_data, class_column = "Alarm", positive_class_label = 1)

    rules = algo.get_rules()

    transformed_data = algo.transform(ieee_data)
    print(transformed_data.info())
    
    X_train, X_test, y_train, y_test = train_test_split (transformed_data.drop(columns=['Alarm']), transformed_data.Alarm, 
                                                         test_size = 0.3, shuffle = False)
    clf.fit(X_train, y_train)
    
    y_test_pred = clf.predict(X_test)
    y_test_proba = clf.predict_proba(X_test)
    
    print('Random forest with IZDAP preproccesing')
    print(metrics.classification_report(y_true=y_test, y_pred=y_test_pred, digits=6))
    print(f"ROC-AUC: {metrics.roc_auc_score(y_true=y_test, y_score=y_test_proba[:, 1])}")
    print(f"Accuracy: {metrics.accuracy_score(y_true=y_test, y_pred=y_test_pred)}")


def izdap_hai():
    
    print("Experiment with HAI test 2")
          
    DATA_PATH = "../datasets/HAI_test2.csv.zip"
    
    hai_data = pd.read_csv(DATA_PATH)
    
    hai_data = hai_data.drop(columns=['timestamp'])
    print(hai_data.info(verbose=False))
    
    X_train, X_test, y_train, y_test = train_test_split (hai_data.drop(columns=['Attack']), hai_data.Attack, 
                                                         test_size = 0.3, shuffle = False)    
    clf = RandomForestClassifier(random_state=5)
    clf.fit(X_train, y_train)
    
    y_test_pred = clf.predict(X_test)
    y_test_proba = clf.predict_proba(X_test)
    
    print('Random forest without IZDAP preproccesing')
    print(metrics.classification_report(y_true=y_test, y_pred=y_test_pred, digits=6))
    print(f"ROC-AUC: {metrics.roc_auc_score(y_true=y_test, y_score=y_test_proba[:, 1])}")
    print(f"Accuracy: {metrics.accuracy_score(y_true=y_test, y_pred=y_test_pred)}")
    
    algo = IzdapAlgo(0.2)
    algo.fit(hai_data, class_column = "Attack", positive_class_label = 1)

    rules = algo.get_rules()

    transformed_data = algo.transform(hai_data)

    print(transformed_data.info())
    
    X_train, X_test, y_train, y_test = train_test_split (transformed_data.drop(columns=['Attack']), 
                                                         transformed_data.Attack, 
                                                         test_size = 0.3, shuffle = False)    
    
    clf.fit(X_train, y_train)
    
    y_test_pred = clf.predict(X_test)
    y_test_proba = clf.predict_proba(X_test)
    
    print('Random forest with IZDAP preproccesing')
    print(metrics.classification_report(y_true=y_test, y_pred=y_test_pred, digits=6))
    print(f"ROC-AUC: {metrics.roc_auc_score(y_true=y_test, y_score=y_test_proba[:, 1])}")
    print(f"Accuracy: {metrics.accuracy_score(y_true=y_test, y_pred=y_test_pred)}")


if __name__ == '__main__':
    izdap_basic_example()
    # izdap_ieee_data()
    # izdap_hai()
