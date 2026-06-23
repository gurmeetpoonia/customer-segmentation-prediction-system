import pandas as pd 
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
from sklearn.decomposition import PCA
import seaborn as sns 
import joblib
df= pd.read_csv("customer_data.csv")


#print(df.info())
#print(df.isnull().sum())
df=df.drop("name",axis=1)
df=df.drop("country",axis=1)
numeric_features=["age","income","purchase_frequency","spending"]
categorical_features=["gender","education"]

numeric_transformer = StandardScaler()
categorical_transformer=OneHotEncoder(handle_unknown="ignore")

preprocessor=ColumnTransformer(transformers=[("num",numeric_transformer,numeric_features),("cat",categorical_transformer,categorical_features)])
X=df.copy()
X_processed=preprocessor.fit_transform(X)
wcss=[]
for k in range(1,11):
    kmeans=KMeans(n_clusters=k,random_state=42)
    kmeans.fit(X_processed)
    wcss.append(kmeans.inertia_)

plt.plot(range(1,11),wcss,marker='o')
plt.title("Eblow method")    
plt.xlabel("Number of clusters ")
plt.ylabel("WCSS")
plt.show()

final_model=Pipeline(steps=[("preprocessor",preprocessor),("kmeans",KMeans(n_clusters=4,random_state=42,n_init=10))])
clusters = final_model.fit_predict(df)
df["Cluster"] = clusters
#print(df.head())
#print(df.info())

X_scaled = preprocessor.fit_transform(df.drop("Cluster", axis=1))
pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_scaled)
plt.scatter(X_2d[:,0], X_2d[:,1], c=clusters, cmap="viridis")
plt.title("Customer Segments")
plt.show()



numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
clustor_summary=df.groupby("Cluster")[numeric_cols].mean()
print(clustor_summary)


labels = {
    0: "Low Value Older",
    1: "Young Low Value",
    2: "High Value",
    3: "Premium Customers"
}
df["Segment"] = df["Cluster"].map(labels)

sns.scatterplot(x="age", y="spending", hue="Cluster", data=df)
plt.title("Age vs Spending by Cluster")
plt.show()

sns.scatterplot(x="age", y="spending", hue="Segment", data=df)
plt.title("Age vs Spending by Segment")
plt.show()

joblib.dump(final_model, open("kmeans_model.pkl", "wb"))
print ("model ! saved successfully")