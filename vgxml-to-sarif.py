# import xml.etree.ElementTree as ET
import argparse
import xmltodict
from sarif_om import SarifLog, Run, Tool, ToolComponent, Result, Message, Location, PhysicalLocation, ArtifactLocation, Region, LogicalLocation
from jschema_to_python.to_json import to_json
import json

def parse_valgrind_xml(xml_file):
    xdict = xmltodict.parse(open(xml_file, "r").read())
    print(json.dumps(xdict))
    return xdict

def create_sarif(results):

    sarif = SarifLog(version="2.1.0", schema_uri="https://json.schemastore.org/sarif-2.1.0.json", runs=[])

    vgo = results["valgrindoutput"]
    tool = Tool(driver=ToolComponent(name=vgo["protocoltool"], version=vgo["protocolversion"], information_uri="https://valgrind.org"))
    results = []
    if "error" in vgo.keys():
        error = vgo["error"]
        # If there's only one type of memory error, this won't be a list
        if not isinstance(error, list):
            error = [error]
        # Each <error> corresponds to a Result
        for e in error:
            m = Message(text=e["kind"])
            result = Result(message=m, rule_id=f'{e["unique"]}', locations=[])
            for stack in e["stack"]:
                for frame in stack:
                    pl = None
                    r = None
                    if "dir" in frame.keys() and "file" in frame.keys():
                        al = ArtifactLocation(uri=f'file://{frame["dir"]}/{frame["file"]}')
                        if "line" in frame.keys():
                            r = Region(start_line=int(frame["line"]))
                        pl = PhysicalLocation(artifact_location=al, region=r)
                    ll = LogicalLocation(fully_qualified_name=frame["fn"])
                    l = Location(physical_location=pl, logical_locations=[ll])
                    result.locations.append(l)
            results.append(result)
    else:
        print("No errors in XML input")

    
    run = Run(tool=tool, results=results)
    sarif.runs.append(run)
    return sarif


def main():
    parser = argparse.ArgumentParser(description="Convert Valgrind XML to SARIF JSON")

    parser.add_argument("input", type=str, help="Input path to Valgrind XML")
    parser.add_argument("output", type=str, help="Output path to SARIF")

    args = parser.parse_args()

    # Parse Valgrind XML and generate SARIF
    parsed_results = parse_valgrind_xml(args.input)
    sarif_data = create_sarif(parsed_results)

    # Output SARIF JSON to file
    with open(args.output, 'w') as f:
        f.write(to_json(sarif_data))

if __name__ == "__main__":
    main()

