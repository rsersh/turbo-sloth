#! bin/python3.6 

import csv342 as csv
from requests_html import HTMLSession

### Define Global Functions ###

def is_phone(infostr):
    if infostr[0:3].isdecimal():
        if infostr[4:7].isdecimal():
            if infostr[8:12].isdecimal():
                return True
        return False
    return False

def is_email(infostr):
    return '@' in infostr

def is_title(infostr):
    if is_phone(infostr):
        return False
    elif is_email(infostr):
        return False
    else:
        return True

def scrape_err(detailstr):
    print("Unexpected Error: " + detailstr)

def parseforthree(infolist):
    if is_title(infolist[0]):
        title = infolist[0]
        if is_email(infolist[1]):
            email = infolist[1]
            if is_phone(infolist[2]):
                phone = infolist[2]  #title, email, phone
            else:
                phone = ''
                scrape_err("parseforthree: check for no phone")
        else:
            email = ''
            if is_phone(infolist[1]):
                phone = infolist[1]
            else:
                phone = ''
                scrape_err("parseforthree: check for no email, no phone")
    else:
        title = ''
        if is_email(infolist[0]):
            email = infolist[0]
            if is_phone(infolist[1]):
                phone = infolist[1]
            else:
                phone = ''
                scrape_err("parseforthree: check for no title, no phone")
        else:
            email = ''
            phone = ''
            scrape_err("parseforthree: check for no info")
    return title, email, phone

def parsefortwo(infolist):
    if is_title(infolist[0]):
        title = infolist[0]
        if is_email(infolist[1]):
            email = infolist[1]
            phone = ''
        elif is_phone(infolist[1]):
            phone = infolist[1]
            email = ''
        else:
            email = ''
            phone = ''
            scrape_err("parsefortwo: infolist[1]")
    elif is_email(infolist[0]):
        email = infolist[0]
        title = ''
        if is_phone(infolist[1]):
            phone = infolist[1]
        else:
            phone = ''
            scrape_err("parsefortwo: infolist[1]")
    else:
        scrape_err("parsefortwo: infolist[0]")
        title = ''
        email = ''
        phone = ''
    return title, email, phone

def parseforone(infolist):
    if is_title(infolist[0]):
        title = infolist[0]
        email = ''
        phone = ''
    if is_email(infolist[0]):
        email = infolist[0]
        title = ''
        phone = ''
    if is_phone(infolist[0]):
        phone = infolist[0]
        title = ''
        email = ''
    return title, email, phone

def parseinfo(infolist):
    length = len(infolist)
    if length == 3:
        return parseforthree(infolist)
    if length == 2:
        return parsefortwo(infolist)
    if length == 1:
        return parseforone(infolist)

divisionsel = "td.views-field.views-field-field-division.views-align-left"
namesel = "td.views-field.views-field-field-first-name.views-align-left.views-field-field-last-name.is-active.views-align-left"
infosel = "td.views-field.views-field-field-job-title.views-align-left.views-field-field-email.views-field-field-phone"
teamsel = "td.views-field.views-field-field-quadrant.views-align-left.views-field-field-team"


#################################

session = HTMLSession() 

csvfile = open("/home/purplehairedone/PyPlate/sfplanstaff.csv",'a')
header = ("Division", "FirstName", "LastName", "Title", "Email", "Phone", "Quadrant/Team")

try:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(header)


    for pagenum in range(16):    # last page only has 4 rows to scrape
        #print(pagenum)
        url = "https://sfplanning.org/staff-directory?key=&page=" + str(pagenum)
        #print(url)
        r = session.get(url)

        # scrape division column
        alldivisions = r.html.find(divisionsel)
        def get_division_at(rownumber):
            return alldivisions[rownumber].text

        # scrape name column
        allnames = r.html.find(namesel)
        def get_names_at(rownumber):
            firstname = (allnames[rownumber].text.split())[0]
            lastname = (allnames[rownumber].text.split())[1]
            return firstname, lastname

        # scrape info column
        allinfo = r.html.find(infosel)
        def get_info_at(rownumber):
            return allinfo[rownumber].text.split('\n')

        # scrape team column
        allteams = r.html.find(teamsel)
        def get_team_at(rownumber):
            return allteams[rownumber].text

        # loop for writing rows using get_line_at(rownum) function 
        if pagenum == 15:
            for rownum in range(4):
                # build entire line
                entireline = []
                division = get_division_at(rownum)
                first, last = get_names_at(rownum)
                title, email, phone = parseinfo(get_info_at(rownum)) 
                team = get_team_at(rownum)
                entireline = entireline+[division]+[first]+[last]+[title]+[email]+[phone]+[team]
                csv_writer.writerow(entireline)
        else:
            for rownum in range(15):
                # build entire line
                entireline = []
                division = get_division_at(rownum)
                first, last = get_names_at(rownum)
                title, email, phone = parseinfo(get_info_at(rownum)) 
                team = get_team_at(rownum)
                entireline = entireline+[division]+[first]+[last]+[title]+[email]+[phone]+[team]
                csv_writer.writerow(entireline)


finally:
    csvfile.close()

