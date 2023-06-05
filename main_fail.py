import parsing 
import data_extraction
# from user_interface import company_fail, company_name

error_file = open('error_file', 'a')

def main(*args):
    from_interface = args
    if len(from_interface) == 5:
        filename = args[0]
        column_name = args[1]
        login = args[2]
        password = args[3]
        result_file_name = args[4]
        company = data_extraction.read_company_fail(filename, column_name)[:10]
        try:
            companies_info = parsing.parsing(company, login, password)
            data_extraction.output_file(companies_info, result_file_name)
        except:
            pass
            # print(f'Компания "{company}" не найдена', file=error_file)
    elif len(from_interface) == 4:
        company_name = args[0]
        login = args[1]
        password = args[2]
        result_file_name = args[3]
        companies_info = parsing.parsing([company_name], login, password)
        data_extraction.output_file(companies_info, result_file_name)




if __name__ == '__main__':
    main()
    error_file.close()



