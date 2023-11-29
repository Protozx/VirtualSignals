import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load the dataset (replace 'path_to_dataset.csv' with the actual file path)
df = pd.read_csv('losingmyreligion.csv', delimiter='\t')

# Initialize a LabelEncoder for each categorical column
# We will create a dictionary of label encoders for the categorical columns
label_encoders = {}
for column in df.columns:
    if df[column].dtype == 'object':
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column].astype(str))
        label_encoders[column] = le

# Now df has all the categorical columns encoded as integers

# Save the preprocessed data to a new CSV file
df.to_csv('verruga_doctor.csv', index=False)
