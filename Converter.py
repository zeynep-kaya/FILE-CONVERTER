import sys
import xml.etree.ElementTree as ET
import json
import lxml
from lxml import etree

#to keep information of files
#each file was put in the list in the same order so common converting functions can be used
array =[]

def readCSVFile(input_file):
    #read file and put in the list line by line
    file= open(input_file,"r")
    list_file = []
    list_file.append(file.readlines())
    file.close()
    list_file = list_file[0]

    #split file with ';'
    #the line character('\n) at the end of each file has been cleared
    #2 dimensional list was designed
    temp_array = list_file

    for i in range(len(list_file)):
        elements =[temp_array[i].split(";")]
        elements = elements[0]
        elements[13] = elements[13].replace("\n","")
        list_file[i] = elements


    return list_file    

def readXMLFile(input_file):
    #xml file was read and data extracted from xml file
    tree = ET.parse(input_file)
    root = tree.getroot()

    #columns names were appended list
    first_row =['ÜNİVERSİTE_TÜRÜ','ÜNİVERSİTE','FAKÜLTE','PROGRAM_KODU','PROGRAM',
    'DİL','ÖĞRENİM_TÜRÜ','BURS','ÖĞRENİM_SÜRESİ','PUAN_TÜRÜ','KONTENJAN','OKUL_BİRİNCİSİ_KONTENJANI',
    'GEÇEN_YIL_MİN_SIRALAMA','GEÇEN_YIL_MİN_PUAN']

    xml_list =[]
    xml_list.append(first_row)
    #data will be kept in temp_list first, it will be thrown into xml_list in the correct order
    temp_list = []
    #data was taken by using loops, from xml file consisting of dict and list structures.
    for elem in root:        
        for subelem in elem:
            temp_list = []
            for value in elem.attrib.values():
                temp_list.append(value)

            for value in subelem.attrib.values(): # 0-faculty 1-id
                temp_list.append(value)

            for text in subelem:
                if(len(text.attrib)>0):
                    for value in text.attrib.values(): 
                        temp_list.append(value)
                temp_list.append(text.text)

            #data came from xml file in mixed order
            #order was designed like first format
            row_list = [temp_list[1],temp_list[0],temp_list[2],temp_list[3],temp_list[6],temp_list[4],temp_list[5]
            ,temp_list[13],temp_list[7],temp_list[10],temp_list[9],temp_list[8],temp_list[11],temp_list[12]]
            xml_list.append(row_list)

    #editing information
    for i in range(len(xml_list)):
        if(xml_list[i][5] == "en"):
            xml_list[i][5] = "İngilizce"
        else:
            xml_list[i][5]=""
            
        if(xml_list[i][6] == "Yes"):
                xml_list[i][6] = "İkinci Öğretim"
        else: 
                xml_list[i][6] = ""
        
    return xml_list

def readJSONFile(input_file):
    data_dict = {}
    #json file was read and put in to dictioanry
    with open(input_file,'r') as json_file:
        data_dict = json.load(json_file)

    first_row =['ÜNİVERSİTE_TÜRÜ','ÜNİVERSİTE','FAKÜLTE','PROGRAM_KODU','PROGRAM',
    'DİL','ÖĞRENİM_TÜRÜ','BURS','ÖĞRENİM_SÜRESİ','PUAN_TÜRÜ','KONTENJAN','OKUL_BİRİNCİSİ_KONTENJANI',
    'GEÇEN_YIL_MİN_SIRALAMA','GEÇEN_YIL_MİN_PUAN']


    json_list =[]
    json_list.append(first_row)
    temp_list = []
    faculty_name=""
    university_name=""
    uType=""

    #read json file dict, take data and put temp_list
    for line in data_dict:
        for elem in line:
            if(elem == 'items'):
                for subelem in line[elem]:
                    for keys in subelem:
                        if(keys=='department'):
                            for info in subelem[keys]:
                                temp_list.append(university_name)
                                temp_list.append(uType)
                                temp_list.append(faculty_name)
                                for keys in info:
                                    temp_list.append(info[keys])
                                #to distinguish each line
                                temp_list.append('endoftheline')
                        else:
                            faculty_name=subelem[keys]
            else:
                if(elem=='university_name'):
                    university_name = line[elem]
                if(elem=='uType'):
                    uType = line[elem]


    line_list=[]
    line = []
    #split line by line
    for i in range(len(temp_list)):
        if(temp_list[i] != 'endoftheline'):
            line.append(temp_list[i])
        else:
            line_list.append(line)
            line=[]

    
    #create a new list
    for line in line_list:
        json_list.append(line)

    #for change of order
    for i in range(1,len(json_list)):

        university_name = json_list[i][0]
        university_type = json_list[i][1]
        grant = json_list[i][13]
        min_order = json_list[i][12]
        min_score = json_list[i][11]
        field = json_list[i][10]
        quota = json_list[i][9]
        spec_quota = json_list[i][8]
        peiod = json_list[i][7]

        json_list[i][0] = university_type
        json_list[i][1] = university_name
        json_list[i][7] = grant
        json_list[i][8] = peiod
        json_list[i][9] = field
        json_list[i][10] = quota
        json_list[i][11] = spec_quota
        json_list[i][12] = min_order
        json_list[i][13] = min_score

    #editing information
    for i in range(len(json_list)):
        if(json_list[i][5] == "en"):
                json_list[i][5] = "İngilizce"
        else:
                json_list[i][5]=""
            
        if(json_list[i][6] == "Yes"):
                json_list[i][6] = "İkinci Öğretim"
        else: 
                json_list[i][6] = ""

    
    return json_list

def convertToXML(array,output_file):
    #convert to XML format using list and dict structures
    university_name = "name_of_university"
    deparments = ET.Element('departments')

    for i in range(1,len(array)):

        if(university_name != array[i][1]):
            university_name = array[i][1]
            university = ET.SubElement(deparments,'university')
            university.set('name',array[i][1])
            university.set('uType',array[i][0])

            item = ET.SubElement(university, 'item')
            item.set('id',array[i][3])
            item.set('faculty',array[i][2])
            name = ET.SubElement(item,'name') 
            
            if(array[i][5] == "İngilizce"):
                lang = "en"
            else:
                lang="tr"
            
            if(array[i][6] == "İkinci Öğretim"):
                second = "Yes"
            else: 
                second = "No"

            if(array[i][7] == None):
                array[i][7] = ""
            
            if(array[i][11] == ""): #spec quota
                array[i][11] = "0"
            if(array[i][12] == ""): #min score
                array[i][12] = "0"
            if(array[i][13] == ""): #min order
                array[i][13] = "0"
        
            name.set('lang',lang)
            name.set('second',second)
            name.text = array[i][4]

            period = ET.SubElement(item,'period')
            period.text = array[i][8]

            quota = ET.SubElement(item,'quota')
            quota.set('spec',array[i][11])
            quota.text = array[i][10]

            field = ET.SubElement(item,'field')
            field.text = array[i][9]

            last_min_score = ET.SubElement(item,"last_min_score")
            last_min_score.set('order',array[i][12])
            last_min_score.text=array[i][13].replace("\n","")

            grant = ET.SubElement(item,'grant')
            grant.text = array[i][7].replace("\n","")
        else:
            item = ET.SubElement(university, 'item')
            item.set('id',array[i][3])
            item.set('faculty',array[i][2])
            name = ET.SubElement(item,'name')  

            if(array[i][5]== "İngilizce"):
                lang = "en"
            else:
                lang="tr"
            
            if(array[i][6] == "İkinci Öğretim"):
                second = "Yes"
            else: 
                second = "No" 
            
            if(array[i][7] == None):
                array[i][7] = ""

            if(array[i][11] == ""):
                array[i][11] = "0"
            if(array[i][12] == ""):
                array[i][12] = "0"
            if(array[i][13] == ""):
                array[i][13] = "0" 
            
            name.set('lang',lang)
            name.set('second',second)
            name.text = array[i][4]

            period = ET.SubElement(item,'period')
            period.text = array[i][8]

            quota = ET.SubElement(item,'quota')
            quota.set('spec',array[i][11])
            quota.text = array[i][10]

            field = ET.SubElement(item,'field')
            field.text = array[i][9]

            last_min_score = ET.SubElement(item,"last_min_score")
            last_min_score.set('order',array[i][12])
            last_min_score.text=array[i][13]

            grant = ET.SubElement(item,'grant')
            grant.text = array[i][7]
    
    CSVtoXML = ET.tostring(deparments)
    #open a xml file 
    output = open(output_file,"w")
    output.write(CSVtoXML.decode("utf-8"))

def convertToCSV(array,output_file):
    line=""
    #changing information type
    for i in range(len(array)):
        for j in range(len(array[i])):
            if(array[i][5] == "tr"):
                array[i][5] = ""
            elif(array[i][5] == "en"):
                array[i][5] = "İngilizce"

            if(array[i][6] == "No"):
                array[i][6] = ""
            elif(array[i][6] == "Yes"):
                array[i][6] = "İkinci Öğretim"
            
            if(array[i][j] == None):
                array[i][j] = ""
            
            if(array[i][j] == "0"):
                array[i][j] = ""

            #add line char('\n') and ';' for each line
            if(j==13):
                line = line +  array[i][j] +"\n"
            else:
                line = line +  array[i][j] +";"

    #open a file with output_file name
    output = open(output_file,"w")
    output.write(line)

def convertToJSON(array,output_file):
    university_name = " "
    dept_id = " "
    line_dict={}
    department_dict = {}
    items_dict = {}
    line_string = []

    for i in range(1,len(array)):
        if(array[i][5] == "İngilizce"):
         lang = "en"
        else:
         lang = "tr"
                
        if(array[i][6] == "İkinci Öğretim"):
         second = "Yes"
        else:
         second =  "No"
        
        if(array[i][7] == None):
            array[i][7] = ""

        if(array[i][11] == ""):
            array[i][11] = "0"
        if(array[i][12] == ""):
            array[i][12] = "0"
        if(array[i][13] == ""):
            array[i][13] = "0" 

        #grouping by faculty and school names and throwing them into the dict structure
        if(university_name != array[i][1]):
            university_name = array[i][1]  

            department_dict = {
               "id": array[i][3],
               "name": array[i][4],
               "lang":lang,
               "second":second,
                "period": array[i][8],
               "spec": array[i][11],
               "quota": array[i][10],
                "field": array[i][9],
               "last_min_score": array[i][13],
                "last_min_order": array[i][12],
               "grant": array[i][7]
            }

            items_dict = {
                "faculty" : array[i][2],
                "department" : [department_dict]
            }

            line_dict = { 
                "university_name": array[i][1],
                "uType" : array[i][0],
                "items": [items_dict]
            }
            
        else:
            if(dept_id != array[i][3]):
                dept_id= array[i][3]  
                department_dict = {
                   "id": array[i][3],
                    "name": array[i][4],
                   "lang":lang,
                   "second":second,
                   "period": array[i][8],
                   "spec": array[i][11],
                   "quota": array[i][10],
                   "field": array[i][9],
                   "last_min_score": array[i][13],
                   "last_min_order": array[i][12],
                    "grant": array[i][7]
                }
                items_dict["department"].append(department_dict)
        #collecting dictionaries in a list
        if(i<len(array)-1):
            if(university_name != array[i+1][1]):
                line_string.append(line_dict)
        else:
            line_string.append(line_dict) 


    #open json file and write data
    with open(output_file, 'w') as json_file:
       json.dump(line_string, json_file,ensure_ascii=False, indent=4)

def XSDValidation(input_file,xsd_file):
    #xsd validaiton for xml file
    xml_file = lxml.etree.parse(input_file)
    validator = lxml.etree.XMLSchema(file=xsd_file)

    is_valid = validator.validate(xml_file)

    print(is_valid)

#test command
#python 2017510048.py /home/deuceng/Documents/CME2202/test/DEPARTMENTS.csv 1.xml 1

#taken arguments
if(len(sys.argv)>1):
    input_file = sys.argv[1]
    output_file= sys.argv[2]
    type = sys.argv[3]
else:
    print("please enter necessarry arguments")

if(type=="1" ): #CSV2XML
    if(input_file.endswith('.csv') & output_file.endswith('.xml')):
        array = readCSVFile(input_file)
        convertToXML(array,output_file)
    else:
        print("invalid file!")

elif(type=="2"): #XML2CSV
    if(input_file.endswith('.xml') & output_file.endswith('.csv')):
        array=readXMLFile(input_file)
        convertToCSV(array,output_file)
    else:
        print("invalid file!")

elif(type=="3"): #XML2JSON
    if(input_file.endswith('.xml') & output_file.endswith('.json')):
        array=readXMLFile(input_file)
        convertToJSON(array,output_file)
    else:
        print("invalid file!")

elif(type=="4"): #JSON2XML
    if( input_file.endswith('.json') & output_file.endswith('.xml')):
        array = readJSONFile(input_file)
        convertToXML(array,output_file)
    else:
        print("invalid file!")

elif(type=="5" ): #CSV2JSON
    if(input_file.endswith('.csv') & output_file.endswith('.json')):
        array = readCSVFile(input_file)
        convertToJSON(array,output_file)
    else:
        print("invalid file!")

elif(type=="6" ): #JSON2CSV
    if(input_file.endswith('.json') & output_file.endswith('.csv')):
        array = readJSONFile(input_file)
        convertToCSV(array,output_file)
    else:
        print("invalid file!")

elif(type=="7"): #XML validate with XSD
    if( input_file.endswith('.xml') & output_file.endswith('.xsd')):
        XSDValidation(input_file,output_file) #output_file is xsd file
    else:
        print("invalid file!")

else:
    print("invalid input!")
