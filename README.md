# NewGenes EC327/EC552

An LLM-powered educational tool that translates biological design intent into simulated genetic circuits and their electronic analogs.

## Goal

To automate the conversion of biological design specifications into executable wetlab protocols by parsing DNA component designs and generating step-by-step PCR protocols ready for laboratory implementation.

## Description

NewGenes is an integrated platform that bridges the gap between computational biology design and practical laboratory execution. The tool takes XML-formatted biological designs as input and produces comprehensive wetlab protocols that scientists can directly use in the laboratory.

**Key Features:**
- Automated DNA component identification and characterization
- Database-driven component information retrieval
- PCR parameter calculation
- Human-readable wetlab protocol generation
- Interactive GUI for design and protocol review

## Implementation Details

The application follows a four-step workflow to transform XML designs into wetlab protocols:

### 1. XML Parsing & DNA Component Extraction
- Parses XML input files to identify DNA components and their properties
- Extracts component metadata including:
  - Component identifiers and names
  - Design specifications
  - Database reference IDs for component lookup
  - Sequence information and length

### 2. Database Lookup & Component Characterization
- Uses extracted database IDs to retrieve detailed component information
- Scrapes biological part databases (such as iGEM Registry, Addgene, or other sources) to obtain:
  - Component type classification (promoters, RBS, genes, terminators, etc.)
  - Known characteristics and performance metrics

### 3. PCR Parameter Calculation
- Calculates optimal PCR parameters including:
  - Annealing temperature
  - Cylce time
  - Forward and reverse primer sequences
- Utilizes **Primer3** integration for primer design:
  - Generates forward and reverse primers and selects the most compatible

### 4. Markdown Protocol Generation
- Constructs comprehensive, step-by-step wetlab protocols in Markdown format
- Includes:
  - Reagent lists and concentrations
  - Detailed procedural steps with timing
  - Temperature and timing specifications

## Usage: How to Use the UI

The NewGenes interface is organized into five main sections working together to provide a seamless workflow from design to protocol:

### 1. **User Control Panel**
Located at the top/left of the interface, this section provides control buttons and inputs:
- **Upload**: Select and upload your XML design file
- **Refresh**: Clear current data and reset the interface
- **Run**: Process the uploaded XML file and generate component table and protocols (takes a few seconds to load)
- **Exit**: Close the application safely

### 2. **XML Viewer**
Displays the contents of your uploaded XML file:
- Shows the raw XML structure for verification
- Helps identify any formatting issues before processing
- Allows you to review components before execution
- Supports scrolling

### 3. **DNA Components Table**
Shows all identified DNA components with their properties:
- **Column Headers**: Name, Type, Other Information
- **Functionality**: 
  - View all components extracted from your XML
  - Verify correct identification before protocol generation

### 4. **PCR Parameters Table**
Displays calculated PCR parameters for each component or assembly reaction:
- **Column Headers**: Component, Forward Primer, Reverse Primer, Tm (°C), Cycle Time
- **Functionality**:
  - Review Primer3-generated primer sequences
  - Verify temperature and timing calculations

### 5. **PCR Protocol Section**
Displays the generated wetlab protocol in human-readable Markdown format:
- **Contents Include**:
  - Complete list of reagents with concentrations and volumes
  - Step-by-step PCR procedure

### Typical Usage:

1. **Prepare Your Design**: Create or obtain an XML file describing your genetic circuit design
2. **Upload File**: Use the Upload button to select your XML file
3. **Review in XML Viewer**: Verify the XML is properly formatted and contains expected data
4. **Execute**: Click Run to process the file
5. **Verify Components**: Check the DNA Components Table for correct identification
6. **Review PCR Parameters**: Examine the PCR Parameters Table for optimal settings
7. **Protocol Ready**: Read through the generated Protocol section
