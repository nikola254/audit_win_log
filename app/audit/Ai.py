import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import export_graphviz
import graphviz
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Загрузка данных
data = pd.read_csv('logs/logs.csv')

# Преобразование строковых значений в числовые
le = LabelEncoder()
data['LogMode'] = le.fit_transform(data['LogMode'])
data['LevelDisplayName'] = le.fit_transform(data['LevelDisplayName'])
data['LogName'] = le.fit_transform(data['LogName'])
data['TimeCreated'] = pd.to_datetime(data['TimeCreated'], format='%d.%m.%Y %H:%M:%S')
data['TimeCreated'] = data['TimeCreated'].apply(lambda x: x.timestamp())

# Определение признаков и классов
X = data[['LogMode', 'MaximumSizeInBytes', 'RecordCount', 'LogName', 'TimeCreated']]
y = data['LevelDisplayName']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создание классификатора
clf = RandomForestClassifier(n_estimators=100, random_state=42)

# Обучение классификатора
clf.fit(X_train, y_train)

# Предсказание классов для тестовой выборки
y_pred = clf.predict(X_test)

# Удаление класса 2 из тестовых данных и предсказаний
mask = y_test != 2
y_test = y_test[mask]
y_pred = y_pred[mask]

# Получение вероятностей для каждого класса
y_prob = clf.predict_proba(X_test)
y_prob = y_prob[mask]

# Оценка качества классификатора
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)
print('Classification Report:')
print(classification_report(y_test, y_pred))
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))

# Визуализация первого дерева из случайного леса
dot_data = export_graphviz(clf.estimators_[0], out_file=None, 
                           feature_names=X.columns,  
                           class_names=le.classes_,  
                           filled=True, rounded=True,  
                           special_characters=True)  # Убрали color_map
graph = graphviz.Source(dot_data)  
graph.render("random_forest_tree", format='png')  # Сохранит в файл random_forest_tree.png

# Данные матрицы путаницы
conf_matrix = np.array([[9, 0, 0],
                        [0, 6, 1],
                        [4, 0, 67]])

# Названия классов
class_names = ['Errors', 'Warnings', 'Criticals']

# Визуализация матрицы путаницы
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', 
            xticklabels=class_names, yticklabels=class_names)

# Настройка заголовков и подписей
plt.title('Матрица путаницы', fontsize=16)
plt.ylabel('Заданные', fontsize=12)
plt.xlabel('Предсказанные', fontsize=12)

# Сохранение графика матрицы путаницы
plt.savefig("confusion_matrix.png")  # Сохранение в файл
plt.close()  # Закрытие текущей фигуры

# Получение важности признаков
importances = clf.feature_importances_  # Получаем важность каждого признака
indices = np.argsort(importances)[::-1]  # Сортируем индексы признаков по важности в порядке убывания

# Визуализация важности признаков
plt.figure()  # Создаем новую фигуру
plt.title("Важность признаков")  # Заголовок графика
plt.bar(range(X.shape[1]), importances[indices], align="center")  # Столбчатая диаграмма
plt.xticks(range(X.shape[1]), X.columns[indices], rotation=90)  # Метки по оси X
plt.xlim([-1, X.shape[1]])  # У станавливаем пределы по оси X

# Сохранение графика важности признаков
plt.savefig("feature_importance.png")  # Сохранение в файл
plt.close()  # Закрытие текущей фигуры