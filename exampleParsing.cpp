#include "sbol.h"
using namespace sbol;

int main()
{
    Document &doc = *new Document();
    doc.read("pIKE_pTAK_toggle_switches.xml");
    std::cout << doc.size() << std::endl;

    return 0;
}
