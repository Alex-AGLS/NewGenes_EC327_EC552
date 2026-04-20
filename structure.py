from extract_xml import *
from scrape import *
import json
import csv

# 
def get_table(xml_path, csv_path):
    results = ""
    result_ls = []
    json_path = "data.json"
    parse(xml_path, json_path)
    with open(json_path, "r") as file:
        data = json.load(file)
    dna_component = data["DNA Component"]
    print(dna_component)
    sub_component = data["Subcomponent"]
    num_entries = len(sub_component)
    print(num_entries)
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Component", dna_component])
        writer.writerow(["name", "type", "information"])
        for component in sub_component:
            tp = get_type(component['Resource'])
            id = component['DisplayId']
            info = get_section(id, "sage")  # usage
            writer.writerow([id, tp, info])


def get_template(temp, time, primer_forward, primer_reverse, txt_path):
    results =  f"protocol:\n " + f"1. Assemble all reaction components on ice.\n\
    Each component should be gently mixed before adding to the reaction in a sterile thin-walled PCR tube.\n\
    The Q5 High-Fidelity DNA Polymerase may be diluted in 1X Q5 Reaction Buffer just prior to use to reduce pipetting errors.\n\
    The entire reaction should be mixed again to ensure homogeneous, consistent mixture.\n\
    Collect all liquid to the bottom of the tube with a quick centrifuge spin if necessary.\n\
    Overlay the sample with mineral oil if using a PCR machine without a heated lid.\n" + f"2. Quickly transfer the reactions to a thermocycler preheated to the denaturation temperature (98 degrees celcius) and begin thermocycling.\n" + f"3. Cycle forward primer ({primer_forward}) and reverse primer ({primer_reverse}) {time} minutes with melting temperatures {temp}, see details in summary table."
    with open(txt_path, "w") as file:
        file.writelines(results)
    return results


if __name__ == '__main__':
    #get_table("BBa_I0462.xml", "parts_table.csv")
    print(get_template(21, 23, 24, 38, "sample.txt"))
