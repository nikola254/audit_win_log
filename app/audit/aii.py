import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_graphviz
import graphviz
from sklearn.preprocessing import LabelEncoder

# Шаг 1: Генерация искусственного набора данных
np.random.seed(42)  # Для воспроизводимости

# Генерация данных
num_samples = 100  # Увеличьте количество образцов
log_modes = ["Circular", "Linear"]
log_names = ["System", "Application", "Security"]
level_display_names = ["Предупреждение", "Ошибка", "Критическая"]

data = pd.DataFrame({
    "LogMode": np.random.choice(log_modes, num_samples),
    "MaximumSizeInBytes": np.random.randint(1000000, 30000000, num_samples),
    "RecordCount": np.random.randint(1000, 50000, num_samples),
    "LogName": np.random.choice(log_names, num_samples),
    "TimeCreated": pd.date_range(start='2024-12-12', periods=num_samples, freq='H'),
    "LevelDisplayName": np.random.choice(level_display_names, num_samples)
})

# Преобразование строковых значений в числовые
le = LabelEncoder()
data['LogMode'] = le.fit_transform(data['LogMode'])
data['LogName'] = le.fit_transform(data['LogName'])
data['LevelDisplayName'] = le.fit_transform(data['LevelDisplayName'])

# Преобразование времени в числовой формат (например, timestamp)
data['TimeCreated'] = pd.to_datetime(data['TimeCreated'])
data['TimeCreated'] = data['TimeCreated'].apply(lambda x: x.timestamp())

# Определение признаков и классов
X = data[['LogName', 'RecordCount', 'MaximumSizeInBytes']]
y = data['LevelDisplayName']

# Шаг 2: Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание и обучение модели
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Шаг 3: Визуализация дерева решений
dot_data = export_graphviz(clf, out_file=None, 
                           feature_names=X.columns,  
                           class_names=le.classes_,  
                           filled=True, rounded=True,  
                           special_characters=True)  
graph = graphviz.Source(dot_data)  
graph.render("decision_tree", format='png')  # Сохранит в файл decision_tree.png