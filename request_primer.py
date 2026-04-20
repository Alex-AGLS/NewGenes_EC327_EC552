import requests
import time
import primer3
# def main():
#     sequence = 'aaagaggagaaatactagatgaaaaacataaatgccgacgacacatacagaataattaataaaattaaagcttgtagaagcaataatgatattaatcaatgcttatctgatatgactaaaatggtacattgtgaatattatttactcgcgatcatttatcctcattctatggttaaatctgatatttcaatcctagataattaccctaaaaaatggaggcaatattatgatgacgctaatttaataaaatatgatcctatagtagattattctaactccaatcattcaccaattaattggaatatatttgaaaacaatgctgtaaataaaaaatctccaaatgtaattaaagaagcgaaaacatcaggtcttatcactgggtttagtttccctattcatacggctaacaatggcttcggaatgcttagttttgcacattcagaaaaagacaactatatagatagtttatttttacatgcgtgtatgaacataccattaattgttccttctctagttgataattatcgaaaaataaatatagcaaataataaatcaaacaacgatttaaccaaaagagaaaaagaatgtttagcgtgggcatgcgaaggaaaaagctcttgggatatttcaaaaatattaggttgcagtgagcgtactgtcactttccatttaaccaatgcgcaaatgaaactcaatacaacaaaccgctgccaaagtatttctaaagcaattttaacaggagcaattgattgcccatactttaaaaattaataacactgatagtgctagtgtagatcactactagagccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata'
#     parameters = {'INPUT_SEQUENCE': sequence}
#     website = 'https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi'

#     with requests.session() as session:
#         poster = session.post(website, data=parameters)
#         with session.get(poster.url, stream=True) as getter:
#             print(getter.text)
   
def main():
    sequence_dna = "aaagaggagaaatactagatgaaaaacataaatgccgacgacacatacagaataattaataaaattaaagcttgtagaagcaataatgatattaatcaatgcttatctgatatgactaaaatggtacattgtgaatattatttactcgcgatcatttatcctcattctatggttaaatctgatatttcaatcctagataattaccctaaaaaatggaggcaatattatgatgacgctaatttaataaaatatgatcctatagtagattattctaactccaatcattcaccaattaattggaatatatttgaaaacaatgctgtaaataaaaaatctccaaatgtaattaaagaagcgaaaacatcaggtcttatcactgggtttagtttccctattcatacggctaacaatggcttcggaatgcttagttttgcacattcagaaaaagacaactatatagatagtttatttttacatgcgtgtatgaacataccattaattgttccttctctagttgataattatcgaaaaataaatatagcaaataataaatcaaacaacgatttaaccaaaagagaaaaagaatgtttagcgtgggcatgcgaaggaaaaagctcttgggatatttcaaaaatattaggttgcagtgagcgtactgtcactttccatttaaccaatgcgcaaatgaaactcaatacaacaaaccgctgccaaagtatttctaaagcaattttaacaggagcaattgattgcccatactttaaaaattaataacactgatagtgctagtgtagatcactactagagccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttata"
    result = primer3.bindings.design_primers(
        {'SEQUENCE_TEMPLATE': sequence_dna},
        global_args = {'PRIMER_PRODUCT_SIZE_RANGE': [[70, 1000]],
        'PRIMER_OPT_TM': 60.0,
        'PRIMER_MIN_TM': 57.0,
        'PRIMER_MAX_TM': 63.0,
        'PRIMER_MIN_GC': 40.0,
        'PRIMER_MAX_GC': 60.0}
    )

    
    # result = primer3.bindings.design_primers(
    # seq_args={
    #     'SEQUENCE_ID': 'MH1000',
    #     'SEQUENCE_TEMPLATE': (
    #         'GCTTGCATGCCTGCAGGTCGACTCTAGAGGATCCCCCTACATTTT'
    #         'AGCATCAGTGAGTACAGCATGCTTACTGGAAGAGAGGGTCATGCA'
    #         'ACAGATTAGGAGGTAAGTTTGCAAAGGCAGGCTAAGGAGGAGACG'
    #         'CACTGAATGCCATGGTAAGAACTCTGGACATAAAAATATTGGAAG'
    #         'TTGTTGAGCAAGTNAAAAAAATGTTTGGAAGTGTTACTTTAGCAA'
    #         'TGGCAAGAATGATAGTATGGAATAGATTGGCAGAATGAAGGCAAA'
    #         'ATGATTAGACATATTGCATTAAGGTAAAAAATGATAACTGAAGAA'
    #         'TTATGTGCCACACTTATTAATAAGAAAGAATATGTGAACCTTGCA'
    #         'GATGTTTCCCTCTAGTAG',
    #     ),
    #     'SEQUENCE_INCLUDED_REGION': [36,342]
    # },
    # global_args={
    #     'PRIMER_OPT_SIZE': 20,
    #     'PRIMER_PICK_INTERNAL_OLIGO': 1,
    #     'PRIMER_INTERNAL_MAX_SELF_END': 8,
    #     'PRIMER_MIN_SIZE': 18,
    #     'PRIMER_MAX_SIZE': 25,
    #     'PRIMER_OPT_TM': 60.0,
    #     'PRIMER_MIN_TM': 57.0,
    #     'PRIMER_MAX_TM': 63.0,
    #     'PRIMER_MIN_GC': 20.0,
    #     'PRIMER_MAX_GC': 80.0,
    #     'PRIMER_MAX_POLY_X': 100,
    #     'PRIMER_INTERNAL_MAX_POLY_X': 100,
    #     'PRIMER_SALT_MONOVALENT': 50.0,
    #     'PRIMER_DNA_CONC': 50.0,
    #     'PRIMER_MAX_NS_ACCEPTED': 0,
    #     'PRIMER_MAX_SELF_ANY': 12,
    #     'PRIMER_MAX_SELF_END': 8,
    #     'PRIMER_PAIR_MAX_COMPL_ANY': 12,
    #     'PRIMER_PAIR_MAX_COMPL_END': 8,
    #     'PRIMER_PRODUCT_SIZE_RANGE': [
    #         [75,100], [100,125], [125,150],
    #         [150,175], [175,200], [200,225]
    #     ],
    # })
    print(result['PRIMER_LEFT_0_SEQUENCE'])
    print(result['PRIMER_RIGHT_0_SEQUENCE'])

if __name__ == '__main__':
    main()

