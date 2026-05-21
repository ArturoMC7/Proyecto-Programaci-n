import json
import csv
from datetime import datetime, timedelta

def load_db():
    try:
        with open('db.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"contracts": []}

def save_db(data):
    with open('db.json', 'w') as f:
        json.dump(data, f, indent=4)

def registerContract(number, contractor, obj, start, end, value, supervisor, status, email):
    db = load_db()
    for c in db['contracts']:
        if c['number'] == number:
            return "number already exists"
    try:
        d_start = datetime.strptime(start, "%d/%m/%Y")
        d_end = datetime.strptime(end, "%d/%m/%Y")
        if d_start > d_end: return "invalid dates"
    except ValueError: return "invalid date format"
    try:
        val_float = float(value)
        if val_float <= 0: return "invalid value"
    except ValueError: return "invalid value"
    if "@" not in email or "." not in email: return "invalid email"
    
    new_contract = {
        "number": number, "contractor": contractor, "object": obj,
        "start": start, "end": end, "value": val_float,
        "supervisor": supervisor, "status": status, "email": email, "trackings": []
    }
    db['contracts'].append(new_contract)
    save_db(db)
    return "ok"

def listContracts():
    db = load_db()
    return sorted(db['contracts'], key=lambda x: x.get('contractor', ''))

def searchContract(number):
    db = load_db()
    for c in db['contracts']:
        if c['number'] == number: return c
    return None

def addTracking(number, date, desc, progress, obs):
    db = load_db()
    try:
        prog_float = float(progress)
        if prog_float < 0 or prog_float > 100: return "invalid progress"
    except ValueError: return "invalid progress"

    for c in db['contracts']:
        if c['number'] == number:
            new_track = {
                "id": len(c['trackings']) + 1, "date": date,
                "desc": desc, "progress": prog_float, "obs": obs
            }
            c['trackings'].append(new_track)
            save_db(db)
            return "ok"
    return "contract not found"

def listTrackings(number):
    db = load_db()
    for c in db['contracts']:
        if c['number'] == number: return c['trackings']
    return "contract not found"

def avgProgress(number):
    db = load_db()
    for c in db['contracts']:
        if c['number'] == number:
            tracks = c['trackings']
            if not tracks: return {"avg": 0}
            promedio = sum(t['progress'] for t in tracks) / len(tracks)
            return {"avg": promedio}
    return "contract not found"

def stats():
    db = load_db()
    contracts = db['contracts']
    if not contracts: return {}
    valores = [float(c['value']) for c in contracts]
    hoy = datetime.now()
    en_un_mes = hoy + timedelta(days=30)

    estadis = {
        "total_by_status": {}, "total_value": sum(valores),
        "avg_value": sum(valores) / len(valores), "near_expiry": []
    }
    for c in contracts:
        estado = c['status']
        estadis["total_by_status"][estado] = estadis["total_by_status"].get(estado, 0) + 1
        try:
            fecha_fin = datetime.strptime(c['end'], "%d/%m/%Y")
            if hoy <= fecha_fin <= en_un_mes: estadis["near_expiry"].append(c['number'])
        except: pass
    return estadis

def exportCsv():
    db = load_db()
    with open('contracts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['numero', 'contratista', 'estado', 'valor'])
        for c in db['contracts']:
            writer.writerow([c['number'], c.get('contractor',''), c.get('status',''), c.get('value','')])
    with open('trackings.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['numero_contrato', 'fecha', 'avance', 'descripcion', 'observacion'])
        for c in db['contracts']:
            for t in c['trackings']:
                writer.writerow([c['number'], t.get('date',''), t.get('progress',''), t.get('desc',''), t.get('obs', '')])
    return True

# ==========================================
# 🔥 NUEVAS FUNCIONES DE MODIFICACIÓN Y CANCELACIÓN
# ==========================================
def updateContract(number, contractor, obj, start, end, value, supervisor, status, email):
    db = load_db()
    for c in db['contracts']:
        if c['number'] == number:
            try:
                datetime.strptime(start, "%d/%m/%Y")
                datetime.strptime(end, "%d/%m/%Y")
            except ValueError: return "invalid date format"
            try:
                val_float = float(value)
                if val_float <= 0: return "invalid value"
            except ValueError: return "invalid value"
            
            c['contractor'] = contractor
            c['object'] = obj
            c['start'] = start
            c['end'] = end
            c['value'] = val_float
            c['supervisor'] = supervisor
            c['status'] = status
            c['email'] = email
            save_db(db)
            return "ok"
    return "not found"

def cancelContract(number, reason):
    db = load_db()
    for c in db['contracts']:
        if c['number'] == number:
            c['status'] = "CANCELADO"
            new_track = {
                "id": len(c['trackings']) + 1,
                "date": datetime.now().strftime("%d/%m/%Y"),
                "desc": "CONTRATO CANCELADO IMPREVISTAMENTE",
                "progress": 0.0,
                "obs": f"Motivo de cancelación: {reason}"
            }
            c['trackings'].append(new_track)
            save_db(db)
            return "ok"
    return "contract not found"