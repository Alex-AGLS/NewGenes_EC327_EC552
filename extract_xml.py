#Python code to illustrate parsing of XML files
# importing the required modules
import csv
import requests
import xml.etree.ElementTree as ET
import json


extract_dna_list = []   
def write_json(object_data, filename='data.json'):
    with open(filename, 'w') as file:
        # file_data = json.load(file)
        # file_data.append(object_data)
        json.dump(object_data,file, indent=4)


def parse(xml_path, json_path):
    tree = ET.parse(xml_path) 
    root = tree.getroot()
    ns = {'default_ns': 'http://sbols.org/v1#',
    'prefix_ns' :'http://www.w3.org/1999/02/22-rdf-syntax-ns#' }
    for dna in root.findall("default_ns:DnaComponent",ns):

        count = 0
        #UNDO#print("Overall DNA") UNDO
        name = dna.find("default_ns:displayId",ns).text
        # # print(name)
        individual_dna = {
            "DNA Component" : name,
            "Subcomponent": []
        }
        print(individual_dna)
        for elem in dna.iter():
            if elem is not dna:
                print(elem.tag)
                if(elem.tag == "{http://sbols.org/v1#}DnaSequence"):
                    nucleotides = elem.find("default_ns:nucleotides",ns).text
                    individual_dna["Nucleotides"] = nucleotides
                    # print(nucleotides)                
                if (elem.tag == "{http://sbols.org/v1#}DnaComponent"):
                    count += 1
                    name1 = elem.find("default_ns:displayId",ns).text
                    #UNDO#print(name1)
                    about_value = elem.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}about")
                    
                    print("rdf:about =", about_value)
                    # print("Type: ", type(about_value))
                    part_about = about_value.split("Part:")
                    # print(f"Full Location: {part_about}") tested if properly split
                    dna_part_code = part_about[-1]
                    
                    # ###print(dna_part_code)  CHECK IF NEED THIS PART (CREATE LOOP)
                    for specific_dna in elem:
                        resource_value1 = specific_dna.attrib
                        # print("Attrib")
                        # print(specific_dna.attrib) 
                        # print("RESOURCE: ")
                        # print(resource_value1)
                        resource_value = specific_dna.get("{http://www.w3.org/1999/02/22-rdf-syntax-ns#}resource")
                        if resource_value is not None:
                            #UNDO#print("rdf:resource =", resource_value)
                            # print("Type: ", type(resource_value))
                            part_resource = resource_value.split("/")
                            dna_resource_code = part_resource[-1]
                            #UNDO#print(dna_resource_code)
                            individual_dna["Subcomponent"].append({"DisplayId": name1,
                                                                  "About" : dna_part_code,
                                                                  "Resource": dna_resource_code}
                                                                  )
                            
        print(individual_dna)
        write_json(individual_dna, json_path)


        #UNDO#print(count) #count
        # individual_dna.append("count": count)
if __name__ == '__main__':
    pass
