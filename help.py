from flask import Flask, render_template, request
import http.client
import json
import pandas as pd

app = Flask(__name__)

def search_medicine_details(medicine_name):
    # First API
    conn1 = http.client.HTTPSConnection("medicine-name-and-details.p.rapidapi.com")
    headers1 = {
        'X-RapidAPI-Key': "9571f24d31msh2933b7a634e1e8ep131659jsnd11c268375f9",
        'X-RapidAPI-Host': "medicine-name-and-details.p.rapidapi.com"
    }
    conn1.request("GET", f"/?medicineName={medicine_name}", headers=headers1)
    res1 = conn1.getresponse()
    data1 = res1.read().decode("utf-8")
    response1 = json.loads(data1)

    # Second API
    conn2 = http.client.HTTPSConnection("api.fda.gov")
    params2 = f"?search=generic_name:\"{medicine_name}\"&limit=1"
    conn2.request("GET", f"/drug/ndc.json{params2}")
    res2 = conn2.getresponse()
    data2 = res2.read().decode("utf-8")
    response2 = json.loads(data2)

    return response1, response2

def load_recalled_drugs(file_path):
    # Load recalled drugs from Excel file into a DataFrame
    try:
        df = pd.read_excel(file_path)
        recalled_drugs = df["Brand-Names"].tolist()
    except Exception as e:
        print(f"Error loading recalled drugs: {e}")
        recalled_drugs = []
    return recalled_drugs

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        medicine_name = request.form['medicine_name']
        response1, response2 = search_medicine_details(medicine_name)
        recalled_drugs = load_recalled_drugs("2024recalls.xlsx")
        return render_template('results.html', response1=response1, response2=response2, recalled_drugs=recalled_drugs)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
