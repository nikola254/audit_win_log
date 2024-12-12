import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder

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

mask = y_test != 2
y_test = y_test[mask]
y_pred = y_pred[mask]

# Оценка качества классификатора
accuracy = accuracy_score(y_test, y_pred)
print('Accuracy:', accuracy)
print('Classification Report:')
# Создайте отчет о классификации без класса 2
print(classification_report(y_test, y_pred))
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))