import sys
import ast
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

from PyQt5.QtCore import Qt
from matplotlib.ticker import MultipleLocator
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QFileDialog, QTableWidget, QTableWidgetItem,
    QMessageBox
)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Результаты Тестирования")
        self.resize(1800, 1020)


        # Основной виджет
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)


        # Кнопки
        button1 = QtWidgets.QPushButton("Кнопка 1")
        button2 = QtWidgets.QPushButton("Кнопка 2")

        # Layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(button1)
        layout.addWidget(button2)


        central_widget.setLayout(layout)

        # Применение стилей
        self.setStyleSheet("""
                    QWidget {
                        background-color: rgb(23, 23, 35);
                    }

                    QPushButton {
                        font-size: 14px;
                        font-weight: bold;
                        color: rgb(255, 255, 255);
                        background-color: rgb(33, 33, 85);
                        border: 6px solid;
                        border-color: rgb(154, 160, 231);
                        border-radius: 20px;
                        padding: 3px 3px 3px 3px;
                        height: 40px;
                        margin: 10px;
                    }

                    QPushButton:hover {
                        border: 3px solid;
                        background-color: rgb(12, 12, 52);
                        border-color: rgb(154, 160, 231);
                    }
                    
                    QTableWidget {
                        background-color: rgb(220, 220, 220);
                        gridline-color: gray;
                        font-size: 14px; 
                    }

                    QHeaderView::section {
                        background-color: rgb(180, 180, 180);
                        padding: 4px;
                        border: none;
                    }
                    QMessageBox
                    {
                        background-color: rgb(220, 220, 220);
                        gridline-color: gray;
                        border: none;
                    }
            
                """)

        self.loaded_file_path = None
        self.plot_list = []
        self.current_plot_index = 0
        self.plot_canvas = None

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        label_name_1 = QtWidgets.QLabel("Таблица для вывода результатов тестирования")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        label_name_1.setFont(font)
        label_name_1.setStyleSheet("color:rgb(212, 212, 212)")
        main_layout.addWidget(label_name_1, alignment=Qt.AlignCenter)

        # Таблица
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.resizeColumnsToContents()  # подогнать под содержимое
        self.table.setFixedHeight(260)

        # Или чтобы все столбцы равномерно заполняли ширину:
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table.setHorizontalHeaderLabels([
            'Тип кроссовера', 'Вероятность мутации', 'Вероятность мутации при эвристике',
            'Точка эвристики','Тип начального поколения', 'Количество поколений', 'Время работы (с)', 'Кол-во нерешённых задач'
        ])

        # Задаём фиксированную высоту, например 300 пикселей

        main_layout.addWidget(self.table)

        label_name_2 = QtWidgets.QLabel("Графики результатов тестирования")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        font.setBold(True)
        label_name_2.setFont(font)
        label_name_2.setStyleSheet("QLabel {\n"
                                   "padding: 5px 0px 0px 0px;"
                                   "color:rgb(212, 212, 212)"
                                   "}")
        main_layout.addWidget(label_name_2, alignment=Qt.AlignCenter)

        # Область для графика
        self.plot_area = QWidget()
        self.plot_area.setStyleSheet("background-color: rgb(33, 33, 45);")
        self.plot_layout = QVBoxLayout(self.plot_area)

        main_layout.addWidget(self.plot_area, stretch=1)

        # Кнопки загрузки и построения
        button_layout = QHBoxLayout()
        self.load_button = QPushButton("Загрузить результаты")
        self.load_button.clicked.connect(self.load_and_display)
        button_layout.addWidget(self.load_button)

        self.graph_button = QPushButton("Построить графики")
        self.graph_button.clicked.connect(self.build_graph)
        button_layout.addWidget(self.graph_button)

        # Навигация по графикам
        self.prev_button = QPushButton("←")
        self.prev_button.clicked.connect(lambda: self.show_plot(-1))
        self.prev_button.setEnabled(False)
        button_layout.addWidget(self.prev_button)

        self.next_button = QPushButton("→")
        self.next_button.clicked.connect(lambda: self.show_plot(1))
        self.next_button.setEnabled(False)
        button_layout.addWidget(self.next_button)

        main_layout.addLayout(button_layout)


    def process_test_results(self, input_file):
        try:
            with open(input_file, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            results = [ast.literal_eval(line.strip()) for line in lines]

            grouped_data = {}

            for result in results:
                key = (result['crossover_method'], result['mutation_rate'], result['mutation_rate_check'], result['gen_check'], result['gen_version'])
                if key not in grouped_data:
                    grouped_data[key] = {
                        'generations': 0,
                        'time': 0.0,
                        'fitness_zero_count': 0,
                        'not_found': 0,
                        'count': 0
                    }
                if result['fitness'] != 0:
                    grouped_data[key]['not_found'] += 1
                grouped_data[key]['generations'] += result['generations']
                grouped_data[key]['time'] += result['time']
                grouped_data[key]['fitness_zero_count'] += 1
                grouped_data[key]['count'] += 1

            aggregated_results = []
            for key, data in grouped_data.items():
                if data['fitness_zero_count'] > 0:
                    aggregated_results.append({
                        'crossover_method': key[0],
                        'mutation_rate': key[1],
                        'mutation_rate_check': key[2],
                        'gen_check': key[3],
                        'gen_version': key[4],
                        'generations': int(data['generations'] / data['fitness_zero_count']),
                        'time': data['time'] / data['fitness_zero_count'],
                        'not_found': data['not_found']
                    })

            aggregated_results.sort(key=lambda x: x['crossover_method'])
            return aggregated_results

        except Exception as e:
            self.show_error(f"Произошла ошибка при обработке файла: {e}")
            return None

    def load_data(self, filename):
        data = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    entry = ast.literal_eval(line.strip())
                    data.append(entry)
        except Exception as e:
            self.show_error(f"Ошибка чтения файла: {e}")
        return data

    def show_error(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Ошибка")
        msg.setText("Произошла ошибка")
        msg.setInformativeText(message)
        msg.exec_()

    def filter_data(self, data):
        dash_data = {'crossover_one': defaultdict(list), 'crossover_two': defaultdict(list)}
        check_data = {'crossover_one': defaultdict(list), 'crossover_two': defaultdict(list)}
        evr_data = {'crossover_one': defaultdict(list), 'crossover_two': defaultdict(list)}

        for entry in data:
            key = (entry['mutation_rate'], entry['gen_check'], entry['mutation_rate_check'], entry['gen_version'])
            if entry['mutation_rate_check'] == '-' and entry['gen_check'] != '-':
                dash_data[entry['crossover_method']][key].append(entry)
            elif entry['mutation_rate_check'] == '-' and entry['gen_check'] == '-':
                evr_data[entry['crossover_method']][key].append(entry)
            elif entry['mutation_rate_check'] != '-' and entry['gen_check'] != '-':
                check_data[entry['crossover_method']][key].append(entry)

        return dash_data, check_data, evr_data

    def average_data(self, data):
        averaged_data = {}
        for crossover, groups in data.items():
            averaged_data[crossover] = {}
            for key, entries in groups.items():
                avg_generations = round(np.mean([entry['generations'] for entry in entries]))
                avg_time = np.mean([entry['time'] for entry in entries])
                averaged_data[crossover][key] = (avg_generations, avg_time)
        return averaged_data

    def plot_data(self, averaged_data, title):
        figures = []

        for crossover, values in averaged_data.items():
            labels, generations, times = [], [], []

            for (mutation_rate, gen_check, mutation_rate_check, gen_version), (
            avg_generations, avg_time) in values.items():
                key = (mutation_rate, gen_check, mutation_rate_check, crossover, gen_version)
                row_number = self.key_to_row_index.get(key, 'Ошибка, обратитесь к разработчику')
                label = f"Набор данных {row_number}"
                labels.append(label)
                generations.append(avg_generations)
                times.append(avg_time)

            if not labels:
                continue

            x = np.arange(len(labels))
            width = 0.2

            fig, ax = plt.subplots(figsize=(14, 6))
            ax2 = ax.twinx()

            ax.bar(x - width / 2, generations, width, label='Generations', color='b')
            ax2.bar(x + width / 2, times, width, label='Time', color='g', alpha=0.6)
            ax.set_title(f'{title}  //  Кроссовер: {crossover}')
            ax.set_xticks(x)
            ax.set_xticklabels(labels, rotation=45, ha="right")
            ax.set_ylabel("Generations", color='b')
            ax2.set_ylabel("Time (s)", color='g')
            ax.grid(True, which='both', linestyle='--', linewidth=0.9, alpha=0.9)

            max_gen = max(generations) if generations else 0

            if max_gen <= 10:
                ax.yaxis.set_major_locator(MultipleLocator(1))
            elif max_gen <= 100:
                ax.yaxis.set_major_locator(MultipleLocator(5))
            elif max_gen <= 500:
                ax.yaxis.set_major_locator(MultipleLocator(25))
            elif max_gen <= 1000:
                ax.yaxis.set_major_locator(MultipleLocator(50))
            elif max_gen <= 2500:
                ax.yaxis.set_major_locator(MultipleLocator(125))
            elif max_gen <= 5000:
                ax.yaxis.set_major_locator(MultipleLocator(250))
            elif max_gen <= 10000:
                ax.yaxis.set_major_locator(MultipleLocator(500))
            elif max_gen <= 20000:
                ax.yaxis.set_major_locator(MultipleLocator(1000))
            elif max_gen <= 40000:
                ax.yaxis.set_major_locator(MultipleLocator(2000))
            elif max_gen <= 80000:
                ax.yaxis.set_major_locator(MultipleLocator(4000))
            elif max_gen <= 1200000:
                ax.yaxis.set_major_locator(MultipleLocator(5000))
            else:
                ax.yaxis.set_major_locator(MultipleLocator(10000))

            fig.tight_layout()
            figures.append(fig)

        return figures


    def load_and_display(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Выбор файла", "", "Text Files (*.txt)")
            if not file_path:
                return

            self.loaded_file_path = file_path
            aggregated_results = self.process_test_results(file_path)
            if aggregated_results is None:
                return

            self.table.setRowCount(len(aggregated_results))
            for row_idx, row in enumerate(aggregated_results):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(row['crossover_method'])))
                self.table.setItem(row_idx, 1, QTableWidgetItem(str(row['mutation_rate'])))
                self.table.setItem(row_idx, 2, QTableWidgetItem(str(row['mutation_rate_check'])))
                self.table.setItem(row_idx, 3, QTableWidgetItem(str(row['gen_check'])))
                self.table.setItem(row_idx, 4, QTableWidgetItem(str(row['gen_version'])))
                self.table.setItem(row_idx, 5, QTableWidgetItem(str(row['generations'])))
                self.table.setItem(row_idx, 6, QTableWidgetItem(f"{row['time']:.2f}"))
                self.table.setItem(row_idx, 7, QTableWidgetItem(str(row['not_found'])))

            self.key_to_row_index = {}
            for row_idx, row in enumerate(aggregated_results):
                key = (row['mutation_rate'], row['gen_check'], row['mutation_rate_check'], row['crossover_method'],row['gen_version'])
                self.key_to_row_index[key] = row_idx + 1
            self.prev_button.setEnabled(False)
            self.next_button.setEnabled(False)
        except ValueError:
            self.show_error("Ошибка1.")
            return False

    def build_graph(self):
        if not self.loaded_file_path:
            self.show_error("Сначала загрузите файл с результатами.")
            return

        data = self.load_data(self.loaded_file_path)
        dash_data, check_data, evr_data = self.filter_data(data)
        averaged_dash_data = self.average_data(dash_data)
        averaged_check_data = self.average_data(check_data)
        averaged_evr_data = self.average_data(evr_data)

        self.plot_list = self.plot_data(averaged_dash_data, "Эвристика без сохранения лучшей особи")
        self.plot_list += self.plot_data(averaged_check_data, "Эвристика с сохранением лучшей особи")
        self.plot_list += self.plot_data(averaged_evr_data, "Без эвристики")

        if not self.plot_list:
            self.show_error("Нет данных для построения графиков.")
            return

        self.current_plot_index = 0
        self.show_plot(0)
        self.prev_button.setEnabled(True)
        self.next_button.setEnabled(True)

    def show_plot(self, direction):
        if not self.plot_list:
            return

        self.current_plot_index += direction
        self.current_plot_index %= len(self.plot_list)

        if self.plot_canvas:
            # Удаляем старый график
            self.plot_canvas.setParent(None)
            self.plot_canvas.deleteLater()
            self.plot_canvas = None

        fig = self.plot_list[self.current_plot_index]
        self.plot_canvas = FigureCanvas(fig)
        self.plot_layout.addWidget(self.plot_canvas)
        self.plot_canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
