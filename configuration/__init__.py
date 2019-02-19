import os

app_data = os.getenv('APPDATA')
app_directory = os.path.join(app_data, 'multitenancy-helper')

os.makedirs(app_directory, exist_ok=True)