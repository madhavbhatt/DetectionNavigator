import xlsxwriter
import mysql.connector
import re

def ConvertToExcel():
    workbook = xlsxwriter.Workbook('/var/www/DetectionNavigator/static/downloads/attackv8.xlsx')
    worksheet = workbook.add_worksheet('Detections')
    # worksheet2 = workbook.add_worksheet('Attempted TTPs')
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'font_size': '12',
        'fg_color': '#FFF8DC'})

    # Formatting based on detection scorecard present
    # 0 = don't detect, 1 = detect, but not variations, 2 = detect this TTP and variations, 3 = N/A not tested
    cell_format_score_0 = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#DC143C', 'border': 1})
    cell_format_score_1 = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#FF8C00', 'border': 1})
    cell_format_score_2 = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#90EE90', 'border': 1})
    cell_format_score_3 = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#D3D3D3', 'border': 1})

    db_connection = mysql.connector.connect(host="localhost", user="django", passwd="django-user-password",database="detectionnav")
    db_cursor = db_connection.cursor()

    db_cursor.execute('SELECT * FROM mitrenv_ttp')
    ttprow = db_cursor.fetchall()

    db_cursor.execute('SELECT * FROM mitrenv_tactic')
    tacrow = db_cursor.fetchall()

    db_cursor.execute('SELECT * FROM mitrenv_techniques')
    techrow = db_cursor.fetchall()

    lenttprow = len(ttprow)
    lentacrow = len(tacrow)
    lentechrow = len(techrow)

    q = 1
    s = 0

    for i in range(0, lenttprow):
        if str(ttprow[i][-2]) != "Reconnaissance" and str(ttprow[i][-2]) != "Resource Development":
            worksheet.merge_range(0, s, 0, s + 1, ttprow[i][-2], merge_format)

            row = 1
            col = q
            m = 0

            for k in range(0, lentechrow):
                if ttprow[i][0] == techrow[k][2]:
                    m += 1
                    Technique = techrow[k][1]
                    techRepeat = techrow[k][3]
                    techColor = techrow[k][-1]
                    Idonly = Technique.split(" :")[0]
                    if not re.findall('T\d{4}.\d{3}', Idonly):
                        if techRepeat > 1:
                            print(Technique)
                            row = m
                            if (techColor == "Crimson"):
                                worksheet.write(row + 1, s, Technique, cell_format_score_0)
                            elif (techColor == "DarkOrange"):
                                worksheet.write(row + 1, s, Technique, cell_format_score_1)
                            elif (techColor == "lightgreen"):
                                worksheet.write(row + 1, s, Technique, cell_format_score_2)
                            elif (techColor == "lightgrey"):
                                worksheet.write(row + 1, s, Technique, cell_format_score_3)
                            else:
                                worksheet.write(row + 1, s, Technique)
                        else:
                            print(Technique)
                            row = m
                            worksheet.write(row + 1, s, Technique, cell_format_score_3)
                            if (techColor == "Crimson"):
                                worksheet.write(row + 1, s, Technique, cell_format_score_0)
                            elif (techColor == "DarkOrange"):
                                worksheet.write(row + 1, s, Technique, cell_format_score_1)
                            elif (techColor == "lightgreen"):
                                worksheet.write(row + 1, s, Technique, cell_format_score_2)
                            elif (techColor == "lightgrey"):
                                worksheet.write(row + 1, s, Technique, cell_format_score_3)
                            else:
                                worksheet.write(row + 1, s, Technique)
                    else:
                        print(Technique, "Column B", k)
                        row = m - 1
                        if (techColor == "Crimson"):
                            worksheet.write(row + 1, s + 1, Technique, cell_format_score_0)
                        elif (techColor == "DarkOrange"):
                            worksheet.write(row + 1, s + 1, Technique, cell_format_score_1)
                        elif (techColor == "lightgreen"):
                            worksheet.write(row + 1, s + 1, Technique, cell_format_score_2)
                        elif (techColor == "lightgrey"):
                            worksheet.write(row + 1, s + 1, Technique, cell_format_score_3)
                        else:
                            worksheet.write(row + 1, s + 1, Technique)
            q = q + 2
            s = s + 2
    workbook.close()
