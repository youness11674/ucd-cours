from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chouaib.db'
app.config['SECRET_KEY'] = 'ucd2024'
db = SQLAlchemy(app)
class Cours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200))
    filiere = db.Column(db.String(50))
    prof = db.Column(db.String(100))
    lien = db.Column(db.String(400))
    duree = db.Column(db.String(50))
def page(content):
    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>UCD</title><style>body{{margin:0;font-family:Arial;background:#f5f7fb}}.top{{background:white;padding:12px 30px;display:flex;justify-content:space-between;box-shadow:0 2px 10px #0001}}.logo{{color:#0d47a1;font-weight:900}} .hero{{background:#0d47a1;color:white;padding:40px 30px}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:15px;padding:20px}} .card{{background:white;padding:15px;border-radius:10px;box-shadow:0 2px 8px #0001}} .btn{{background:#0d47a1;color:white;padding:6px 12px;border-radius:15px;text-decoration:none}}</style></head><body><div class=top><div class=logo>UCD - جامعة شعيب الدكالي</div><a href=/admin style=text-decoration:none>Admin</a></div>{content}</body></html>"""
@app.route('/')
def home():
    cours = Cours.query.all()
    grid = '<div class=grid>' + "".join([f'<div class=card><b>{c.titre}</b><br><small>{c.filiere} - {c.prof}</small><br><br><a class=btn href={c.lien} target=_blank>Voir</a></div>' for c in cours]) + '</div>'
    hero = '<div class=hero><h1>Université Chouaib Doukkali</h1><p>SMIA SMP SVT Droit - Cours & TD</p><a class=btn href=/cours style=background:white;color:#0d47a1>Voir tous les cours</a></div>'
    return page(hero+grid)
@app.route('/cours')
def cours_list():
    f = request.args.get('f'); q = Cours.query.filter_by(filiere=f).all() if f else Cours.query.all()
    html = '<div style=padding:20px><a class=btn href=/cours>Tous</a> <a class=btn href=/cours?f=SMIA>SMIA</a> <a class=btn href=/cours?f=SMP>SMP</a> <a class=btn href=/cours?f=SVT>SVT</a> <a class=btn href=/cours?f=Droit>Droit</a></div><div class=grid>' + "".join([f'<div class=card><b>{c.titre}</b><br>{c.filiere}<br><br><a class=btn href={c.lien} target=_blank>Download</a></div>' for c in q]) + '</div>'
    return page(html)
@app.route('/admin', methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        db.session.add(Cours(titre=request.form['titre'],filiere=request.form['filiere'],prof=request.form['prof'],lien=request.form['lien'],duree="10h"))
        db.session.commit(); return redirect('/')
    return page('<div style="max-width:400px;margin:20px auto;background:white;padding:20px;border-radius:10px"><form method=POST><input name=titre placeholder="Titre" style="width:100%;padding:8px;margin:5px 0" required><select name=filiere style="width:100%;padding:8px"><option>SMIA</option><option>SMP</option><option>SVT</option><option>Droit</option></select><input name=prof placeholder="Prof" style="width:100%;padding:8px;margin:5px 0"><input name=lien placeholder="Lien Drive" style="width:100%;padding:8px;margin:5px 0" required><button class=btn style="width:100%;padding:10px">Ajouter</button></form></div>')
@app.route('/delete/<int:id>')
def delete(id):
    c=Cours.query.get(id)
    if c: db.session.delete(c); db.session.commit()
    return redirect('/')
with app.app_context():
    db.create_all()
    if not Cours.query.first():
        for t,f,p in [("Analyse 1","SMIA","Pr Alami"),("Algebre 1","SMIA","Pr Bounoua"),("Mecanique","SMP","Pr Fadil"),("Thermo","SMP","Pr Asbik"),("Bio Cell","
