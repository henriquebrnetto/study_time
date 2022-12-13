from datetime import datetime, timedelta, time
from time import sleep
import pandas as pd
import os, sys, json

def main():
    start = datetime.now()
    while True:
        try:
            print(f'Running... {datetime.now()-start}')
            sleep(600)
            pass

        #Code to Exit Program and Dump Data Into Excel File
        except KeyboardInterrupt:
            end = datetime.now()
            h, hrest = divmod((end-start).total_seconds(), 3600)
            min, sec = divmod(hrest, 60)
            timet = time(int(h), int(min), int(sec))
            vals = [start.date().strftime('%d/%m/%Y'), start.time().isoformat(timespec='seconds'), end.time().isoformat(timespec='seconds'), time.strftime(timet, '%H:%M:%S'), 'Estudo']
            df = pd.DataFrame(vals).T
            with pd.ExcelWriter('Horários de Estudo.xlsx', engine='openpyxl', date_format='YYYY-MM-DD', mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, 'Estudo', header=False, index=False, startrow = writer.sheets['Estudo'].max_row)
            sys.exit()

        finally:
            #Get last data from Excel file
            last_data = pd.read_excel('Horários de Estudo.xlsx').iloc[-1,:]
            try:
                with open('last_time.json', 'r') as json_file:
                    last_val = pd.Series(json.load(json_file)).T

                #Insert data from json file in excel if necessary
                if last_data.equals(last_val) == False:
                    with pd.ExcelWriter('Horários de Estudo.xlsx', engine='openpyxl', date_format='YYYY-MM-DD', mode='a', if_sheet_exists='overlay') as writer:
                        last_val.to_excel(writer, 'Tempo de Estudo', header=False, index=False, startrow = writer.sheets['Tempo de Estudo'].max_row)
            except:
                pass

            #Write data into json file (in case of an error in the code above, the data will still be saved)
            dict_keys = ['Dia', 'Início', 'Final', 'Delta (hh:min:seg)', 'Tipo']
            with open('last_time.json', 'w') as file:
                res = {dict_keys[i]: vals[i] for i in range(len(dict_keys))}
                json.dump(res, file)


if __name__ == '__main__':
    main()
