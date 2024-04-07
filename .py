import http.client
import json
import pandas as pd

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

def main():
    medicine_name = input("Enter the Medicine name: ")
    response1, response2 = search_medicine_details(medicine_name)

    # Display details from the first API
    if response1:
        print("\nDetails from First API:")
        print(f"Medicine Name: {response1[0]['medicineName']}")
        print(f"Details URL: {response1[0]['detailsUrl']}")
        print(f"Medicine Image: {response1[0]['medicineImage']}\n")
    else:
        print("No data found from First API.")

    # Display generic name, brand names, dosage form, and product type from the second API
    if response2.get('results'):
        print("Generic Name and Brand Names from Second API:")
        generic_name = response2['results'][0]['generic_name']
        brand_name = response2['results'][0]['brand_name']
        if generic_name == brand_name:
            print(f"Combined Name: {generic_name}")
        else:
            print(f"Generic Name: {generic_name}")
            print(f"Brand Name: {brand_name}")
        print(f"Dosage Form: {response2['results'][0]['dosage_form']}")
        print(f"Product Type: {response2['results'][0]['product_type']}\n")
    else:
        print("No data found from Second API.")

    # Load recalled drugs from Excel file
    recalled_drugs = load_recalled_drugs("2024recalls.xlsx")
    if medicine_name in recalled_drugs:
        print("\nThis medicine has been recalled.")
    else:
        print("\nThis medicine has not been recalled.")

if __name__ == "__main__":
    main()
