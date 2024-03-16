from flask import Flask, render_template, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="static", static_url_path='')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secret_key'

from views import *   

import unittest
from check import *
from tables import *
import datetime

class Test(unittest.TestCase):
    def test_process_substances(self):
        table_name = 'Substances'
        model = dct_models[table_name]
        headers = model.attr()

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)

        # Новое значение
        new_line = ['test', 'test', 5.0]
        new_df.loc[len(new_df)] = new_line

        # Добавить в датафрейм
        process_model(new_df, model)

        # Считать датафрейм
        line = list(read_table(table_name)[-1][1:])
        
        # Проверить соответствие            
        self.assertEqual(new_line, line)

    def test_process_incidents(self):
        table_name = 'Incidents'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)

        # Новое значение
        new_line = ['2001-02-12 15:15:15', substances[0][1], posts[0][1]]
        new_df.loc[len(new_df)] = new_line

        # Добавить в датафрейм
        process_model(new_df, model)

        # Считать датафрейм
        new_line = ['2001-02-12 15:15:15', substances[0][0], posts[0][0]]
        line = list(read_table(table_name)[-1][1:])
        
        # Проверить соответствие            
        self.assertEqual(new_line, line)

    def test_process_posts(self):
        table_name = 'Posts'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)

        # Новое значение
        new_line = ['test', '15.5, 12.5', 2]
        new_df.loc[len(new_df)] = new_line

        # Добавить в датафрейм
        process_model(new_df, model)

        # Считать датафрейм
        line = list(read_table(table_name)[-1][1:])
        
        # Проверить соответствие            
        self.assertEqual(new_line, line)

    def test_process_emissioninventory(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)

        # Новое значение
        new_line = [5, 'Точечный', 100, 4.5, 0, 38.8, 14.5, 70, 39.1, 31.9, '15.5, 12.5']
        print(len(headers))
        print(len(new_line))
        new_df.loc[len(new_df)] = new_line

        # Добавить в датафрейм
        process_model(new_df, model)

        # Считать датафрейм
        line = list(read_table(table_name)[-1][1:])
        
        # Проверить соответствие            
        self.assertEqual(new_line, line)

    def test_edit_substances(self):
        table_name = 'Substances'
        model = dct_models[table_name]
        headers = model.attr()

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)

        # Новое значение
        id = read_table(table_name)[-1][0]
        new_line = [id, 'test2', 'test2', 10.0]
        new_df.loc[len(new_df)] = new_line

        # Изменить датафрейм
        edit_model(new_df, model)

        # Считать датафрейм
        line = list(read_table(table_name)[-1])
        
        # Проверить соответствие            
        self.assertEqual(new_line, line)

    def test_edit_incidents(self):
        table_name = 'Incidents'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)

        # Новое значение
        id = read_table(table_name)[-1][0]
        new_line = [id, '2001-02-12 15:15:15', substances[0][1], posts[0][1]]
        new_df.loc[len(new_df)] = new_line

        # Изменить датафрейм
        edit_model(new_df, model)

        # Считать датафрейм
        new_line = [id, '2001-02-12 15:15:15', substances[0][0], posts[0][0]]
        line = list(read_table(table_name)[-1])
        
        # Проверить соответствие            
        self.assertEqual(new_line, line)

    def test_edit_posts(self):
        table_name = 'Posts'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)

        # Новое значение
        id = read_table(table_name)[-1][0]
        new_line = [id, 'test', '15.5, 12.5', 2]
        new_df.loc[len(new_df)] = new_line

        # Изменить датафрейм
        edit_model(new_df, model)

        # Считать датафрейм
        line = list(read_table(table_name)[-1])
        
        # Проверить соответствие            
        self.assertEqual(new_line, line)

    def test_edit_emissioninventory(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)

        # Новое значение
        id = read_table(table_name)[-1][0]
        new_line = [id, 5, 'Точечный', 100, 4.5, 0, 38.8, 14.5, 70, 39.1, 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line

        # Изменить датафрейм
        edit_model(new_df, model)

        # Считать датафрейм
        line = list(read_table(table_name)[-1])
        
        # Проверить соответствие            
        self.assertEqual(new_line, line)
    
    def test_delete_substances(self):
        table_name = 'Substances'
        model = dct_models[table_name]
        headers = model.attr()

        # Значение
        id = read_table(table_name)[-1][0]
        new_line = list(read_table(table_name)[-1])

        # Изменить датафрейм
        delete_from_table(table_name, id)

        # Считать датафрейм
        line = list(read_table(table_name)[-1])
        
        # Проверить соответствие            
        self.assertNotEqual(new_line, line)

    def test_delete_incidents(self):
        table_name = 'Incidents'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Значение
        id = read_table(table_name)[-1][0]
        new_line = list(read_table(table_name)[-1])

        # Изменить датафрейм
        delete_from_table(table_name, id)

        # Считать датафрейм
        line = list(read_table(table_name)[-1])
        
        # Проверить соответствие            
        self.assertNotEqual(new_line, line)

    def test_delete_posts(self):
        table_name = 'Posts'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Значение
        id = read_table(table_name)[-1][0]
        new_line = list(read_table(table_name)[-1])

        # Изменить датафрейм
        delete_from_table(table_name, id)

        # Считать датафрейм
        line = list(read_table(table_name)[-1])
        
        # Проверить соответствие            
        self.assertNotEqual(new_line, line)

    def test_delete_emissioninventory(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Значение
        id = read_table(table_name)[-1][0]
        new_line = list(read_table(table_name)[-1])

        # Изменить датафрейм
        delete_from_table(table_name, id)

        # Считать датафрейм
        line = list(read_table(table_name)[-1])
        
        # Проверить соответствие            
        self.assertNotEqual(new_line, line)
    
    def test_check_substances_0(self):
        table_name = 'Substances'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['test2', 'test2', 10.0]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertTrue(check_model(new_df, model))

    def test_check_substances_1(self):
        table_name = 'Substances'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['test2', 'test2', 'djj']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))

    def test_check_incidents_0(self):
        table_name = 'Incidents'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['2001-02-12 15:15:15', substances[0][1], posts[0][1]]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertTrue(check_model(new_df, model))
        
    def test_check_incidents_1(self):
        table_name = 'Incidents'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['2001-02-12 15:15:--', substances[0][1], posts[0][1]]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_check_posts_0(self):
        table_name = 'Posts'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['test', '15.5, 12.5', 2]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertTrue(check_model(new_df, model))
        
    def test_check_posts_1(self):
        table_name = 'Posts'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['test', '15.5, 12.5', '2dfghj']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkemissioninventory_0(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [5, 'Точечный', 100, 4.5, 0, 38.8, 14.5, 70, 39.1, 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertTrue(check_model(new_df, model))
        
    def test_checkemissioninventory_1(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['fghj', 'Точечный', 100, 4.5, 0, 38.8, 14.5, 70, 39.1, 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))

    def test_checkemissioninventory_2(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [5, 'Точечный', 'ff100', 4.5, 0, 38.8, 14.5, 70, 39.1, 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkemissioninventory_3(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [5, 'Точечный', 100, 'dfghj', 0, 38.8, 14.5, 70, 39.1, 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))

    def test_checkemissioninventory_4(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [5, 'Точечный', 100, 4.5, 'dfghjk', 38.8, 14.5, 70, 39.1, 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))

    def test_checkemissioninventory_5(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [5, 'Точечный', 100, 4.5, 0, 'dfghj', 14.5, 70, 39.1, 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))

    def test_checkemissioninventory_6(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [5, 'Точечный', 100, 4.5, 0, 38.8, 'fghj', 70, 39.1, 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkemissioninventory_7(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [5, 'Точечный', 100, 4.5, 0, 38.8, 14.5, 'dfghj', 39.1, 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkemissioninventory_8(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [5, 'Точечный', 100, 4.5, 0, 38.8, 14.5, 70, 'dfghjk', 31.9, '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkemissioninventory_9(self):
        table_name = 'EmissionInventory'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [5, 'Точечный', 100, 4.5, 0, 38.8, 14.5, 70, 39.1, 'dfghj', '15.5, 12.5']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkmeteo_0(self):
        table_name = 'Meteo'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['2001-02-12 15:15:15', 1.2, 999, 4, 260, 80]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertTrue(check_model(new_df, model))
        
    def test_checkmeteo_1(self):
        table_name = 'Meteo'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['2001-02-12 15:15:15', 'dfghj', 999, 4, 260, 80]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkmeteo_2(self):
        table_name = 'Meteo'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['2001-02-12 15:15:15', 1.2, 'fghj', 4, 260, 80]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkmeteo_3(self):
        table_name = 'Meteo'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['2001-02-12 15:15:15', 1.2, 999, 'fghj', 260, 80]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkmeteo_4(self):
        table_name = 'Meteo'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['2001-02-12 15:15:15', 1.2, 999, 4, 'fghj', 80]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkmeteo_5(self):
        table_name = 'Meteo'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['2001-02-12 15:15:15', 1.2, 999, 4, 260, 'dfghj']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))

    def test_checkmeteo_6(self):
        table_name = 'Meteo'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = ['2001-02-12 15:15:--', 1.2, 999, 4, 260, 80]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkmeasurements_0(self):
        table_name = 'Measurements'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [posts[0][1], '2001-02-12 15:15:15', 1, 80, 1021, 0]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertTrue(check_model(new_df, model))
        
    def test_checkmeasurements_1(self):
        table_name = 'Measurements'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [posts[0][1], '2001-02-12 15:15:--', 1, 80, 1021, 0]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))

    def test_checkmeasurements_2(self):
        table_name = 'Measurements'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [posts[0][1], '2001-02-12 15:15:15', 'dfgh', 80, 1021, 0]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkmeasurements_3(self):
        table_name = 'Measurements'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [posts[0][1], '2001-02-12 15:15:15', 1, 'fgh', 1021, 0]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))

    def test_checkmeasurements_4(self):
        table_name = 'Measurements'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [posts[0][1], '2001-02-12 15:15:15', 1, 80, 'dfghj', 0]
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))
        
    def test_checkmeasurements_5(self):
        table_name = 'Measurements'
        model = dct_models[table_name]
        headers = model.attr()
        posts = [elm for elm in get_posts()]
        substances = [elm for elm in get_substances()]

        # Новый датафрейм
        new_df = pd.DataFrame(columns=headers)
        new_df = new_df.drop('id', axis=1)
        new_line = [posts[0][1], '2001-02-12 15:15:15', 1, 80, 1021, 'fghj']
        new_df.loc[len(new_df)] = new_line
        
        # Проверить соответствие            
        self.assertFalse(check_model(new_df, model))


unittest.main()