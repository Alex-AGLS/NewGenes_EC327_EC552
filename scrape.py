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
def get_type(id:str) -> int:
    url = "https://ontobee.org/ontology/SO?iri=http://purl.obolibrary.org/obo/" + id
    response = requests.get(url, headers=custom_headers)
    print(response.content)
    print('\n')
    soup = BeautifulSoup(response.content, "xml")
    possible_ls = soup.find_all("rdfs:label")
    print(possible_ls)
    print('\n')
    for possible_entry in possible_ls:
        type = possible_entry.contents[0]
        if ('promoter' in str(type)):
            print(type)
            return 1
        elif 'sequence' in str(type):
            print(type)
            return 2
        elif 'terminator' in str(type):
            print(type)
            return 3
        elif 'ribosome' in str(type):
            print(type)
            return 4
        else:
            print(type)
    return 5




# parts.igem.org database, takes in id as "BBa_R0040"
def get_protocal(id:str) -> str:
    url = "https://parts.igem.org/Part:" + id
    response = requests.get(url, headers=custom_headers)
    print(response.content)
    print('\n')
    soup = BeautifulSoup(response.content, "html.parser")
    possible_ls = soup.find_all(lambda tag: 'rotocol' in str(tag.get('id')))
    print(possible_ls)
    results = ""
    count = 1
    for possible_entry in possible_ls:
        if('Protocol' in str(possible_entry)):
            results += 'Protocol: \n'
            while (possible_entry != None and possible_entry.find_next_siblings() == []):
                possible_entry = possible_entry.parent
                count += 1
            if (possible_entry != None):
                following = possible_entry.find_next_sibling()
                while True:
                    results += following.getText() + '\n'
                    #print(following.name)
                    #print(following.find_next_sibling().name == following.name)
                    if (following != None and following.name != following.find_next_sibling().name):
                        break
                    #print(following.name)
                    
                    following = following.find_next_sibling()

    return results

if __name__ == "__main__":
    #type = get_type("SO_0000139")
    #print(type)
    protocal = get_protocal("BBa_C0012")
    print(protocal)