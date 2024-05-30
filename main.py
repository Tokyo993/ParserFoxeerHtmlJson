import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'parser_links')))

from parser_links.foxeer.foxeer_ThermalCamera import ThermalCameraParser
from parser_links.foxeer.foxeer_fpvCam import FpvCamParser
from parser_links.foxeer.foxeer_flightController import FlightControllerParser
from parser_links.foxeer.foxeer_esc import EscParser
from parser_links.foxeer.foxeer_propellers import PropellerParser
from parser_links.foxeer.foxeer_Vtx import VtxParser
from parser_links.foxeer.foxeer_antenna import AntennaParser
from parser_links.foxeer.foxeer_frame import FrameParser
from parser_links.foxeer.foxeer_elr import ElrParser
from parser_links.foxeer.foxeer_gps import GpsParser
from parser_links.foxeer.foxeer_hdCam import HdCamParser
from parser_links.foxeer.foxeer_monitor import MonitorParser
from parser_links.foxeer.foxeer_motor import MotorParser
from parser_links.foxeer.foxeer_other import OtherParser
from parser_links.foxeer.foxeer_rtf import RtfParser

# Список парсеров и их названий
parsers = [
    ("ThermalCamera", ThermalCameraParser),
    ("Rtf", RtfParser),
    ("FpvCam", FpvCamParser),
    ("FlightController", FlightControllerParser),
    ("Esc", EscParser),
    ("Propeller", PropellerParser),
    ("Vtx", VtxParser),
    ("Antenna", AntennaParser),
    ("Frame", FrameParser),
    ("Elr", ElrParser),
    ("Gps", GpsParser),
    ("HdCam", HdCamParser),
    ("Monitor", MonitorParser),
    ("Motor", MotorParser),
    ("Other", OtherParser)
]

if __name__ == '__main__':
    output_dir = os.path.join(os.path.dirname(__file__), 'OutputHtml')
    os.makedirs(output_dir, exist_ok=True)

    while True:
        print("Выберите раздел для парсинга (введите номер или 'q' для выхода):")
        for i, (name, _) in enumerate(parsers):
            print(f"{i + 1}. {name}")

        choice = input("Ваш выбор: ")

        if choice.lower() == 'q':
            break

        try:
            index = int(choice) - 1
            if index < 0 or index >= len(parsers):
                print("Неверный выбор. Попробуйте снова.")
                continue

            name, ParserClass = parsers[index]
            parser_instance = ParserClass()
            parsed_data = parser_instance.parse()

            output_file = os.path.join(output_dir, f'{name}.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(str(parsed_data))

            print(f'Данные {name} сохранены в {output_file}\n')

        except ValueError:
            print("Неверный ввод. Пожалуйста, введите номер.")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

