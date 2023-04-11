import pandas as pd
from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
import flask.scaffold
flask.helpers._endpoint_from_view_func = flask.scaffold._endpoint_from_view_func


def read_data():
    """Lê o dataset e retorna um DataFrame"""
    return pd.read_csv('iris.data.csv', sep=',')


def abort_if_doesnt_exist(index):
    """Verifica se a flor existe no dataset"""
    data = read_data()
    if index not in list(data.index):
        abort(404, message=f'Flower {index} não existe no dataset')


# Inicializa a API
app = Flask(__name__)
api = Api(app)


# Argumentos que serão passados para a API
parser = reqparse.RequestParser()
parser.add_argument('Sepal_length', type=float)
parser.add_argument('Sepal_width', type=float)
parser.add_argument('Petal_length', type=float)
parser.add_argument('Petal_width', type=float)
parser.add_argument('Species', type=str)


class Flower(Resource):
    def get(self, index):
        """Retorna uma flor específica"""
        abort_if_doesnt_exist(index)
        data = read_data()
        return jsonify(data.iloc[index].to_dict())

    def delete(self, index):
        """Deleta uma flor específica"""
        abort_if_doesnt_exist(index)
        data = read_data()
        data = data.drop(index, axis=0)
        data.to_csv('iris.data.csv', index=False)
        return '', 204

    def put(self, index):
        """Atualiza uma flor específica"""
        abort_if_doesnt_exist(index)
        data = read_data()
        args = parser.parse_args()
        data.iloc[index] = args
        data.to_csv('iris.data.csv', index=False)
        return '', 201


class FlowerList(Resource):
    def get(self):
        """Retorna todas as flores"""
        data = read_data()
        return jsonify(data.to_dict(orient='records'))

    def post(self):
        """Adiciona uma nova flor"""
        data = read_data()
        args = parser.parse_args()
        new_data = pd.DataFrame([args])
        data = pd.concat([data, new_data], ignore_index=True)
        data.to_csv('iris.data.csv', index=False)
        return '', 201


# Route para a classe Flower
api.add_resource(Flower, '/movie/<int:index>')
api.add_resource(FlowerList, '/movie')


if __name__ == '__main__':
    app.run(debug=True)
