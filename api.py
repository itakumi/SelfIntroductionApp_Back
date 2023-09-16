from flask import Flask, request, jsonify, render_template
import os
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import base64
import json
import io
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # SQLiteデータベースの設定
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 追跡の無効化
db = SQLAlchemy(app)
CORS(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    team = db.Column(db.String(255), nullable=False)
    others = db.Column(db.Text, nullable=True)  # 必要に応じて適切なデータ型を選択
    image_data = db.Column(db.Text, nullable=True)  # Base64エンコードされた画像データを保存

    def __init__(self, name, team, others=None, image_data=None):
        self.name = name
        self.team = team
        self.others = others
        self.image_data = image_data

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET'])
def get_items():
    if request.method == 'GET':
        items = Item.query.all()  # データベースからすべてのアイテムを取得

        item_list = []
        for item in items:
            item_data = {
                'id': item.id,
                'name': item.name,
                'team': item.team,
                'others': item.others,
                "image": item.image_data
                # 画像データはバイナリ形式で保存されているため、JSONに含めないことが一般的です
            }
            item_list.append(item_data)

        return jsonify({'items': item_list})

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.json
    print(data["name"])
    folder_name = data["name"]    
    if request.method == 'POST':
        name = data["name"]
        team = data["Team"]
        other = data["Other"]
        image_data = data["image"]

        new_item = Item(name=name, team=team, others=other, image_data=image_data)

        db.session.add(new_item)
        db.session.commit()
        return 'Item added successfully'

@app.route('/delete', methods=['POST'])
def delete_item():
    data = request.json
    item_id=data["id"]
    print("item_id=",item_id)
    # データベースセッションを取得
    session = db.session
    try:
        item = Item.query.get(item_id)

        if item:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": f"Item with ID {item_id} has been deleted."}), 200
        else:
            return jsonify({"message": f"Item with ID {item_id} not found."}), 404

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred while deleting the item."}), 500

if __name__ == '__main__':
    # app.debug
    # app.run(port=3004, debug=True)
    # app.run(debug=True)
    # app.run(host="0.0.0.0", debug=False)
    app.run(port=3004, host="0.0.0.0", threaded = False)








