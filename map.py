import sys
import io
import requests
import folium
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


# Folium inside Pyqt5
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('SkateMap')
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # reading city data
        data = pd.read_csv('cities.csv', usecols=['name', 'lon', 'lat'])

        # loading map & setting default start location
        m = folium.Map(
            # tiles='Stamen Terrain',
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            zoom_start=6,
            location=[33.98813901349684, -118.46677927707837] # venice, CA
        )

        folium.TileLayer



        # goes through each location and adds marker to map
        for i in range(0,len(data)):
            folium.Marker(
                location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
                popup=data.iloc[i]['name'],
                icon=folium.Icon(color="orange", icon="info-sign"),
            ).add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)
        m.save('webmap.html')

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Program..')
