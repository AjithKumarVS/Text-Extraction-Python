import textract
import re
import regex
import unicodedata
def convert_pdf_to_txt_v2(path):
    try:
        text = textract.process(path)
        text=text.decode("ascii", "ignore")
        return text
    except Exception as e:
        print(e)
        pass
    
outputDictionary={}
claim=convert_pdf_to_txt_v2("/home/ubuntu/environment/Claim.pdf")
claim=repr(claim)
claimUpdated=re.sub(r"\\n\\n",r"\\n",claim)

insuredName=re.search(r"(?<=Name and address of Insured\\n)[A-Za-z ]+",claimUpdated)[0]
outputDictionary["Insured Name:"]=insuredName

insuredAddressL1=regex.search(r"Name and address of Insured\\n[A-Za-z ]+\\n\K\S.*?(?=\\n)",claimUpdated)[0]
insuredAddressL2=regex.search(r"Name and address of Insured\\n[A-Za-z ]+\\n[1-9A-Za-z ]+\\n\K\S.*?(?=\\n)",claimUpdated)[0]
insuredAddressL3=regex.search(r"Name and address of Insured\\n[A-Za-z ]+\\n[1-9A-Za-z ]+\\n[A-Za-z ]+\\n\K\S.*?(?=\\n)",claimUpdated)[0]
insuredAddress=insuredAddressL1+" "+insuredAddressL2+" "+insuredAddressL3
outputDictionary["Insured Address:"]=insuredAddress

dob=regex.search(r"DOB:\s*\K\S.*?(?=\\n)",claimUpdated)[0]
outputDictionary["Date of birth:"]=dob

employersName=regex.search(r"Name:\s*\K\S.*?(?=\\n)",claimUpdated)[0]
outputDictionary["Employer's Name:"]=employersName

employersLocation=regex.search(r"Location:\s*\K\S.*?(?=\\n)",claimUpdated)[0]
outputDictionary["Employer's Location:"]=employersLocation

claim=re.search(r"(?<=Medical History).*$",claim)[0]
claim=re.sub(r"\\x0c\'","",claim)

diseases=re.findall(r"(?<=\\n)[A-Za-z ]+(?!\\n\d)(?!\\n\\n\d)\b",claim)

claimers=re.findall(r"(?<=\\n)[A-Za-z ]+(?=\\n\\n\d|\\n\d)",claim)

tempList=[]

for val in claimers:
    key=val+"'s history"
    tempRegex=val+r"\\n\K[^A-Z]+"
    checkString=regex.search(tempRegex,claim)[0]
    checkList=checkString.split("\\n")
    checkList=checkList[:len(checkList)-2]
    i=0
    for temp in checkList:
        if(temp!=""):
            tempList.append(diseases[i])
        else:
            pass
        i=i+1
    outputDictionary[key]=tempList
    tempList=[]
    
print(outputDictionary)