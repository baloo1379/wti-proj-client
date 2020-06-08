import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics
from joblib import dump, load
import matplotlib.pyplot as plt


class FruitsLabelingService:
    dir = ""
    file_dir = "data_files/"
    model_dir = "model_files/"

    def __init__(self, model_name, file_name):
        self.model_name = f"./{self.dir}{self.model_dir}{model_name}.joblib"
        self.file_name = f"./{self.dir}{self.file_dir}{file_name}"

        self.fruits = pd.read_table(self.file_name)
        self.look_up_fruit_name = dict(zip(self.fruits.fruit_label.unique(), self.fruits.fruit_name.unique()))

        self.X = self.fruits[['mass', 'width', 'height', 'color_score']]
        self.y = self.fruits['fruit_label']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, random_state=0)

        self.knn = None
        self.score = 0.0

    def load_model(self):
        self.knn = load(self.model_name)

    def save_model(self, new_model_file_name=None, *args, **kwargs):
        if new_model_file_name is not None:
            self.model_name = f"./{self.dir}{self.model_dir}{new_model_file_name}.joblib"
        dump(self.knn, self.model_name)

    def prepare_model(self):
        self.knn = KNeighborsClassifier(n_neighbors=5)
        self.knn.fit(self.X_train, self.y_train)
        self.score = self.knn.score(self.X_test, self.y_test)

    def predict(self, data):
        fruit_prediction = self.knn.predict(data)
        return self.look_up_fruit_name[fruit_prediction[0]]
