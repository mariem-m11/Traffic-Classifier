from fastapi import FastAPI, HTTPException
from joblib import load
import numpy as np
from pydantic import BaseModel

# Load models
scaler = load('C:/Users/makni/Downloads/RT5/Futur_Reseaux_Mobil/projet_afif/refs/Repo/Traffic-Classifier-SDN/Traffic-Classifier/Models/KNN/scaler.joblib')
pca = load('C:/Users/makni/Downloads/RT5/Futur_Reseaux_Mobil/projet_afif/refs/Repo/Traffic-Classifier-SDN/Traffic-Classifier/Models/KNN/pca.joblib')
knn = load('C:/Users/makni/Downloads/RT5/Futur_Reseaux_Mobil/projet_afif/refs/Repo/Traffic-Classifier-SDN/Traffic-Classifier/Models/KNN/knn.joblib')

app = FastAPI()

class InputData(BaseModel):
    features: list  # Expect a list of features from the user

@app.post("/predict/")
async def make_prediction(data: InputData):
    try:
        # Convert input data to numpy array
        input_data = np.array(data.features).reshape(1, -1)
        
        # Apply scaling and PCA
        scaled_data = scaler.transform(input_data)
        pca_data = pca.transform(scaled_data)
        
        # Make prediction
        prediction = knn.predict(pca_data)
        
        return {"prediction": int(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
