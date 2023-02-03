from datetime import datetime, timedelta, time
from time import sleep
import pandas as pd
import os, sys, json, logging

def main(mode):
    #Get starting time
    start = datetime.now()

    #Create path variables
    path_excel = 'D:\\Python Projects\\Tempo de Estudo\\Horários de Estudo.xlsx'
    path = "D:\\Python Projects\\Tempo de Estudo\\errors.log"
    
    #Log basic configuration
    
    logging.basicConfig(filename=path, filemode='a', 
    format='%(asctime)s,Function (%(funcName)s), Line %(lineno)d: %(message)s')

    #-------------------------------------------------------------Main Loop-------------------------------------------------------------
    while True:
        try:
            print(f'Running... {datetime.now()-start}')
            sleep(600)
            pass

        #-----------------------------------------------------Code to Exit Program------------------------------------------------------
        #Intended Exception
        #Program saves information on Excel file just by closing it
        except KeyboardInterrupt as e:
            error1 = type(e).__name__
            print(error1)
            print('Ending application...')
            end = datetime.now()

            #Computes total time in hours:minutes:seconds
            h, hrest = divmod((end-start).total_seconds(), 3600)
            min, sec = divmod(hrest, 60)
            timet = time(int(h), int(min), int(sec))

            #Checks mode chosen to differentiate the "Tipo" feature
            if mode.upper() == 'P':
                vals = [start.date().strftime('%d/%m/%Y'), start.time().isoformat(timespec='seconds'),
                end.time().isoformat(timespec='seconds'), time.strftime(timet, '%H:%M:%S'), 'Prog']
            if mode.upper() == 'F':
                vals = [start.date().strftime('%d/%m/%Y'), start.time().isoformat(timespec='seconds'),
                end.time().isoformat(timespec='seconds'), time.strftime(timet, '%H:%M:%S'), 'Faculdade']
            if mode.upper() == 'T':
                vals = [start.date().strftime('%d/%m/%Y'), start.time().isoformat(timespec='seconds'),
                end.time().isoformat(timespec='seconds'), time.strftime(timet, '%H:%M:%S'), 'Trabalho']

            #Gets data from json file and compare data from Excel file with it
            last_data = pd.read_excel(path_excel).iloc[-1,:]
            try:
                with open(path_excel, 'r') as json_file:
                    last_val = pd.Series(json.load(json_file)).T

                #Inserts data from json file in excel if the values are different
                if last_data.equals(last_val) == False:
                    with pd.ExcelWriter(path_excel, engine='openpyxl', date_format='YYYY-MM-DD', mode='a', if_sheet_exists='overlay') as writer:
                        last_val.to_excel(writer, 'Tempo de Estudo', header=False, index=False, startrow = writer.sheets['Tempo de Estudo'].max_row)
                    print('Updating information in Excel file...')
                    print('Data from previous runtime inserted! All set.')
            except:
                pass

            #Transforms data format and insert it into Excel file
            df = pd.DataFrame(vals).T
            df.columns = ['Dia', 'Início', 'Final', 'Delta (hh:min:seg)', 'Tipo']
            print('First try.....')
            with pd.ExcelWriter(path_excel, engine='openpyxl', date_format='YYYY-MM-DD',
            mode='a', if_sheet_exists='overlay') as writer:
                df.to_excel(writer, 'Estudo', header=False, index=False, startrow = writer.sheets['Estudo'].max_row)
            print('All set! See you next time :)')

        #--------------------------------------------Code to Solve any Issue with Excel Input ---------------------------------------------
        finally:
            #Gets and logs error if application ends by itself
            if error1 != 'KeyboardInterrupt':
                print(f'Application failed. ERROR : {error1}')
                logging.basicConfig(filename=path, filemode='a', 
                format='%(asctime)s, Function (%(funcName)s), Line %(lineno)d: %(message)s')
                logging.exception(error1)
            
            #Gets last data from Excel file and try to insert it again into the file
            last_data = pd.read_excel(path_excel).iloc[-1,:]
            if df.squeeze().equals(last_data) == False:
                print('An error occured.')
                try:
                    print('Second try.....')
                    with pd.ExcelWriter(path_excel, engine='openpyxl', date_format='YYYY-MM-DD', mode='a', if_sheet_exists='overlay') as writer:
                        df.to_excel(writer, 'Estudo', header=False, index=False, startrow = writer.sheets['Estudo'].max_row)
                    print('All set! See you next time :)')
                #Log errors to errors file
                except Exception as e:
                    logging.exception(e)
                    pass

            #Writes new data into json file (in case of an error in the code above, the data will still be saved)
            dict_keys = ['Dia', 'Início', 'Final', 'Delta (hh:min:seg)', 'Tipo']
            with open('D:\\Python Projects\\Tempo de Estudo\\last_time.json', 'w') as file:
                res = {dict_keys[i]: vals[i] for i in range(len(dict_keys))}
                json.dump(res, file)
                print('Json file updated.')
            
            sleep(5)
            sys.exit()


if __name__ == '__main__':
    my_dict = {'P' : 'Programação', 'F' : 'Faculdade', 'T' : 'Trabalho'}
    mode = (input(f'{my_dict["P"]} (P), {my_dict["F"]} (F) ou {my_dict["T"]} (T)? ')).upper()
    print(f'Modo escolhido: {my_dict[mode]}\n-----------------------------------------------------------------------------------------------------------------------')
    main(mode)
