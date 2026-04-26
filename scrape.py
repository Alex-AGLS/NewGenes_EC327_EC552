import requests
from bs4 import BeautifulSoup



custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.google.com/',
    'Accept': 'application/json, text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
}


# 1: promoter; 2: sequence; 3: terminator; 4: ribosome; 5: nothing
# uses ontobee database, takes id as "SO_???????""
def get_type(id:str) -> str:
    url = "https://ontobee.org/ontology/SO?iri=http://purl.obolibrary.org/obo/" + id
    response = requests.get(url, headers=custom_headers)
    #print(response.content)
    #print('\n')
    soup = BeautifulSoup(response.content, "xml")
    possible_ls = soup.find_all("rdfs:label")
    #print(possible_ls)
    #print('\n')
    for possible_entry in possible_ls:
        type = possible_entry.contents[0]
        print(type)
        if ('promoter' in str(type)):
            #print(type)
            return "promoter"
        elif 'sequence' in str(type) or 'CDS' in str(type):
            #print(type)
            return "coding sequence"
        elif 'terminator' in str(type):
            #print(type)
            return "terminator"
        elif 'ribosome' in str(type):
            #print(type)
            return "ribosome binding site"
        else:
            #print(type)
            pass
    return ""



# parts.igem.org database, takes in id as "BBa_R0040"
# get the text of the section following headers with specified keword
def get_section(id:str, key:str) -> str:
    url = "https://parts.igem.org/Part:" + id
    response = requests.get(url, headers=custom_headers)
    #print(response.content)
    #print('\n')
    soup = BeautifulSoup(response.content, "html.parser")
    possible_ls = soup.find_all(lambda tag: key in str(tag.get('id')))
    if (possible_ls == []): 
        possible_ls = soup.find_all(lambda tag: (tag.name == 'span' or 'h' in tag.name) and key in tag.getText())
    #print(possible_ls)
    results = ""
    count = 1
    for possible_entry in possible_ls:
        if(key in str(possible_entry)):
            
            while (possible_entry != None and possible_entry.find_next_siblings() == []):
                possible_entry = possible_entry.parent
                count += 1
            if (possible_entry != None):
                following = possible_entry.find_next_sibling()
                while True:
                    if (following == None):
                        break
                    results += following.getText() + '\n'
                    #print(following.name)
                    #if following.find_next_sibling() != None:
                        #print(following.find_next_sibling().name) 
                    if (following.find_next_sibling() == None):
                        break
                    elif (following.name != following.find_next_sibling().name):
                        break
                    #print(following.name)
                    following = following.find_next_sibling()

    return results




if __name__ == "__main__":
    tp = get_type("SO_0000316")
    print(tp)
    #print('\n')
    #result = get_section("BBa_C0062", "repressor")
    #print(result)