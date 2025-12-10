# 🥗 Food Nutrition Analyzer  
A smart and interactive health-focused web application that analyzes food items, predicts nutritional values using machine learning, and recommends healthier alternatives.  
It also includes features such as a healthy recipes finder, nutrition tips, and an intuitive UI for users to explore health-related insights.

---

## 🚀 Features

### 🔍 **1. Nutrition Analyzer (ML-Powered)**
- Accepts natural language input (e.g., “2 dosa 1 chicken biryani”).  
- Detects food items and their quantities.  
- Predicts:
  - Calories
  - Protein
  - Carbohydrates
  - Fat  
- Uses a trained ML model (`nutrition_predictor.pkl`).

### 🥗 **2. Healthy Recipes Finder**
- Search recipes instantly.
- Provides external verified healthy recipe links.
- User-friendly cards and search preview.

### 📊 **3. Nutrients Explorer**
- Displays nutrient details for foods from the dataset.
- Easy-to-read structured UI.

### 💡 **4. Healthy Eating Tips**
- Provides curated health & diet tips.
- Clean, card-based layout.

### 📘 **5. About Section**
- Professional overview of nutrition & wellness.

---

## 🏗️ **Tech Stack Used**

### **Frontend**
- HTML5  
- CSS3  
- Vanilla JavaScript  
- Responsive UI Components

### **Backend**
- Flask (Python)
- Flask-CORS  
- Pandas  
- Joblib (ML model loading)

### **Machine Learning**
- Custom trained model: `nutrition_predictor.pkl`
- Dataset: `Food.csv`
- Encoding: Food, Cuisine, Category encodings

---

## 🧠 **How It Works (Workflow)**

### **1. User enters food text**
Example: *“2 idli and 1 dosa”*

### **2. Backend detects foods**
- Regex matching  
- Quantity extraction  
- Food encoding

### **3. ML model predicts nutrition**
For each food item:
- calories  
- protein  
- carbs  
- fat  

### **4. Results returned to frontend**
- Total nutrition  
- Food-wise recommendations:
  - Alternatives  
  - Low-calorie options  
  - High-protein options  
  - Healthy additions

---

## 🏛️ **System Architecture**


