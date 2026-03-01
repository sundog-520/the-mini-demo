import json
data = {
    "ddl": 20,
    "demand": {"body": 10, "arm": 25},
    "suppliers": {
        "body": [
            {"id": "SupA", "cost": 60, "lead_time": 10, "moq": 5},
            {"id": "SupB", "cost": 50, "lead_time": 15, "moq": 20}
        ],
        "arm": [
            {"id": "SupX", "cost": 20, "lead_time": 5, "moq": 10},
            {"id": "SupY", "cost": 30, "lead_time": 3, "moq": 5}
        ]
    }
}
def a(data):
    p = []
    cost = 0 
    for item, needed in data['demand'].items():
        supplier = [
            s for s in data['suppliers'][item] 
            if s['lead_time'] <= data['ddl']
        ]
        supplier.sort(key=lambda x: x['cost'])
        remainingdemand = needed
        for sup in supplier:
            if remainingdemand <= 0:
                break
            purchase = max(remainingdemand, sup['moq'])      
            p.append({
                "item": item,
                "supplier": sup['id'],
                "quantity": purchase
            })          
            cost += purchase * sup['cost']
            remainingdemand -= purchase       
    return {"plan": p, "totalcost": cost}
result = a(data)
print(json.dumps(result, indent=4))