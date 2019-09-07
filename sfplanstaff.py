#! bin/python3 

import csv342 as csv
from requests_html import HTMLSession

session = HTMLSession()

csvfile = open("/home/purplehairedone/PyPlate/test.csv",'a')
header = ('Division', 'FirstName', 'LastName', 'Title', 'Email', 'Phone', 'Team')



for pagenum in range(0):    # last page only has 4 rows to scrape
    baseurl = "https://sfplanning.org/staff-directory?key&page&"
    r = session.get(baseurl + str(pagenum))

    # scrape division column
    divisionsel = "td.views-field.views-field-field-division.views-align-left"
    alldivisions = r.html.find(divisionsel)
    
    # scrape name column
    namesel = "td.views-field.views-field-field-first-name.views-align-left.views-field-field-last-name.is-active.views-align-left"
    allnames = r.html.find(namesel)
    def get_names_at(rownumber):
        firstname = (allnames[rownumber].text.split())[0]
        lastname = (allnames[rownumber].text.split())[1]
        return firstname, lastname

    # scrape info column
    infosel = "td.views-field.views-field-field-job-title.views-align-left.views-field-field-email.views-field-field-phone"
    allinfo = r.html.find(infosel)
    def get_info_at(rownumber):
        title = (allinfo[rownumber].text.split())[0]
        email = (allinfo[rownumber].text.split())[1]
        phone = (allinfo[rownumber].text.split())[2]
        return title, email, phone

    # scrape team column
    teamsel = "td.views-field.views-field-field-quadrant.views-align-left.views-field-field-team"
    allteams = r.html.find(teamsel)
    
   

    # loop for writing rows using get_line_at(rownum) function 
    try:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        
        for rownum in range(14):
            # build entire line
            entireline = []
            # grab names
            name = get_names_at(rownum)
            # grab info
            info = get_info_at(rownum)
            #
            entireline = entireline + [alldivisions[rownum].text] +
                         [name[0].text] + [name[1].text] + [info[0].text] +
                         [info[1].text] + [info[2].text] + 
                         [allteams[rownum].text]
            #csv_writer.writerow([alldivisions[rownum].text])
            csv_writer.writerow(entireline)
    finally:
        csvfile.close()

