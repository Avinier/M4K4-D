"""Author PCB-09's review schematic from stock Nightly library symbols.

Run only while this schematic is closed in Eeschema. The PCB editor is driven
through KiPy; use Nightly F8 to transfer the circuit, never a second PCB writer.
"""
from pathlib import Path
import copy
import json
import re
import uuid

HERE = Path(__file__).resolve().parent
NAME = "pcb-09-c0-link-adapter"
LIB = Path("/Applications/KiCad-nightly/KiCad.app/Contents/SharedSupport/symbols")


class Atom(str):
    pass


def parse(text):
    stack, root = [], None
    for token in re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', text):
        if token == "(":
            node = []
            if stack:
                stack[-1].append(node)
            else:
                root = node
            stack.append(node)
        elif token == ")":
            stack.pop()
        else:
            stack[-1].append(json.loads(token) if token.startswith('"') else Atom(token))
    return root


def dump(node):
    if isinstance(node, list):
        return "("+" ".join(map(dump, node))+")"
    return str(node) if isinstance(node, Atom) else json.dumps(node)


def children(node, key):
    return [n for n in node if isinstance(n, list) and n and n[0] == key]


def child(node, key):
    return children(node, key)[0]


def uid(key):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, "makad/pcb09/"+key))


libraries = {}


def symbol(libid):
    lib, name = libid.split(":")
    if lib not in libraries:
        libraries[lib] = parse((LIB/(lib+".kicad_sym")).read_text())
    own = copy.deepcopy(next(n for n in children(libraries[lib], "symbol") if n[1] == name))
    bases = children(own, "extends")
    if bases:
        base = symbol(lib+":"+bases[0][1])
        overrides = [n for n in own[2:] if isinstance(n, list) and n[0] != "extends"]
        own = copy.deepcopy(base)
        own[1] = name
        for override in overrides:
            key = override[:2] if override[0] == "property" else override[:1]
            own = [n for n in own if not (isinstance(n, list) and n[:len(key)] == key)]
            own.append(override)
        for n in children(own, "symbol"):
            n[1] = name+re.search(r"(_\d+_\d+)$", n[1]).group(1)
    return own


rootid = uid("root")
instances, wires, labels, ncs, defs, manifest = [], [], [], [], {}, {}


def add(ref, libid, value, footprint, x, y, nets, bom=True):
    lib = symbol(libid)
    lib[1] = libid
    defs[libid] = lib
    properties = []
    for k, v, dy in [("Reference", ref, -5.08), ("Value", value, -2.54),
                     ("Footprint", footprint, 0), ("Datasheet", "", 0)]:
        tx, ty = x+8, y+dy
        if ref == "J1" and k in ("Reference", "Value"):
            tx, ty = x-12.7, y+(-35.56 if k == "Reference" else -33.02)
        elif ref.startswith("U") and k in ("Reference", "Value"):
            tx, ty = x+12.7, y+(-22.86 if k == "Reference" else -20.32)
        properties.append(f'(property {json.dumps(k)} {json.dumps(v)} (at {tx} {ty} 0) '
                          f'(effects (font (size 1.0 1.0)) (justify left)'+(' (hide yes)' if k in ("Footprint", "Datasheet") else '')+'))')
    pinids = []
    pinmap = {}
    for unit in children(lib, "symbol"):
        for pin in children(unit, "pin"):
            number = child(pin, "number")[1]
            px, py, a = map(float, child(pin, "at")[1:4])
            px, py = round(x+px, 4), round(y-py, 4)
            net = nets.get(number)
            pinmap[number] = net
            pinids.append(f'(pin "{number}" (uuid "{uid(ref+"/pin/"+number)}"))')
            if net is None:
                ncs.append(f'(no_connect (at {px} {py}) (uuid "{uid(ref+"/nc/"+number)}"))')
                continue
            dx, dy = {0: (-5.08, 0), 180: (5.08, 0), 90: (0, 5.08), 270: (0, -5.08)}[int(a)]
            ex, ey = round(px+dx, 4), round(py+dy, 4)
            wires.append(f'(wire (pts (xy {px} {py}) (xy {ex} {ey})) (stroke (width 0) (type default)) (uuid "{uid(ref+"/wire/"+number)}"))')
            justify = "right" if dx < 0 else "left"
            labels.append(f'(label "{net}" (at {ex} {ey} 0) (effects (font (size 1 1)) (justify {justify} bottom)) (uuid "{uid(ref+"/label/"+number)}"))')
    instances.append(f'(symbol (lib_id "{libid}") (at {x} {y} 0) (unit 1) '
                     f'(in_bom {"yes" if bom else "no"}) (on_board yes) (dnp no) '
                     f'(uuid "{uid(ref)}") '+" ".join(properties+pinids)+
                     f' (instances (project "{NAME}" (path "/{rootid}" (reference "{ref}") (unit 1)))))')
    manifest[ref] = {"value": value, "symbol": libid, "footprint": footprint, "pins": pinmap}


if __name__ == "__main__":
    RFP = "Resistor_SMD:R_0603_1608Metric"
    CFP = "Capacitor_SMD:C_0603_1608Metric"
    gpio = {1:"+3V3_PI",2:"+5V_PI",3:"I2C1_SDA",4:"+5V_PI",5:"I2C1_SCL",
            7:"BASE_TX",8:"HEAD_TX",10:"HEAD_RX",12:"BCLK",15:"SDI1",16:"AMP_SD",
            17:"+3V3_PI",18:"FAN_EN",29:"BASE_RX",35:"LRCLK",38:"SDI0",40:"SDO0"}
    gpio.update({n:"GND" for n in (6,9,14,20,25,30,34,39)})
    add("J1", "Connector_Generic:Conn_02x20_Odd_Even", "Pi_40_pin_socket_MPN_OPEN",
        "Connector_PinSocket_2.54mm:PinSocket_2x20_P2.54mm_Vertical", 55.88, 76.2,
        {str(n):v for n,v in gpio.items()})
    for index, role, y in [(1,"HEAD",76.2),(2,"BASE",147.32)]:
        other = "C2" if role == "HEAD" else "C3"
        pn = {"1":"+3V3_PI","2":role+"_RX","3":role+"_TX","4":"GND",
              "5":role+"_C0TX_P","6":role+"_C0TX_N","7":role+"_"+other+"TX_N","8":role+"_"+other+"TX_P"}
        add(f"U{index}","Interface_UART:THVD1451D","THVD1451DR","Package_SO:SOIC-8_3.9x4.9mm_P1.27mm",147.32,y,pn)
        add(f"J{index+1}","Connector_Generic:Conn_01x06",f"J9-{index}_{role}",
            "Connector_JST:JST_GH_SM06B-GHS-TB_1x06-1MP_P1.25mm_Horizontal" if index == 1 else
            "Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical",228.6,y,
            {"1":"GND","2":pn["5"],"3":pn["6"],"4":pn["7"],"5":pn["8"]})
        add(f"R{index}","Device:R","4.7k",RFP,101.6,y,{"1":"+3V3_PI","2":role+"_TX"})
        add(f"R{index+2}","Device:R","120",RFP,190.5,y+17.78,{"1":pn["8"],"2":pn["7"]})
        add(f"C{index}","Device:C","100n",CFP,147.32,y+35.56,{"1":"+3V3_PI","2":"GND"})
    add("J4","Connector_Generic:Conn_01x10","J9-3_AUDIO_W26",
        "Connector_JST:JST_GH_BM10B-GHS-TBT_1x10-1MP_P1.25mm_Vertical",330.2,76.2,
        dict(zip(map(str,range(1,11)),["+3V3_PI","LRCLK","GND","BCLK","GND","SDO0","SDI1","SDI0","AMP_SD","5V_SENSE_TP_ONLY"])))
    add("Q1","Transistor_FET:AO3400A","AO3400A","Package_TO_SOT_SMD:SOT-23",299.72,167.64,
        {"1":"FAN_GATE","2":"GND","3":"FAN_SW"})
    add("R5","Device:R","100",RFP,259.08,167.64,{"1":"FAN_EN","2":"FAN_GATE"})
    add("R6","Device:R","100k",RFP,299.72,208.28,{"1":"FAN_GATE","2":"GND"})
    add("J5","Connector_Generic:Conn_01x02","J9-4_FAN",
        "Connector_JST:JST_XH_B2B-XH-A_1x02_P2.50mm_Vertical",355.6,157.48,{"1":"+5V_PI","2":"FAN_SW"})
    add("D1","Device:D_Schottky","1N5819HW","Diode_SMD:D_SOD-123",345.44,187.96,{"1":"+5V_PI","2":"FAN_SW"})
    add("C3","Device:C","10u_10V","Capacitor_SMD:C_0805_2012Metric",345.44,218.44,{"1":"+5V_PI","2":"GND"})
    add("C4","Device:C","100n",CFP,375.92,218.44,{"1":"+5V_PI","2":"GND"})
    for n,net in enumerate(["I2C1_SDA","I2C1_SCL","GND","5V_SENSE_TP_ONLY","+3V3_PI","+5V_PI"],1):
        add(f"TP{n}","Connector:TestPoint",net,"TestPoint:TestPoint_Pad_D1.0mm",50.8+40.64*(n-1),243.84,{"1":net},False)
    for n,net in enumerate(["+3V3_PI","+5V_PI","GND"],1):
        add(f"#FLG0{n}","power:PWR_FLAG","PWR_FLAG","",50.8+25.4*(n-1),269.24,{"1":net},False)
    head = f'(kicad_sch (version 20261015) (generator "eeschema") (generator_version "10.99") (uuid "{rootid}") (paper "A3") '
    head += '(title_block (title "PCB-09 C0 link adapter - review schematic") (date "2026-10-31") (rev "A-draft") (company "Makad") (comment 1 "D-073 / D-074; socket mating height, retention and CR-02 evidence remain open"))'
    text = head+' (lib_symbols '+" ".join(dump(n) for n in defs.values())+') '
    text += " ".join(instances+wires+labels+ncs)
    for title, x, y in [("PI HEADER / D-073",30.48,30.48),("HEAD RS-422 / UART0",121.92,30.48),
                         ("BASE RS-422 / UART2",101.6,121.92),("AUDIO / W26 SIGNALS ONLY",304.8,45.72),
                         ("ENCLOSURE FAN / GPIO24",254,137.16),("SERVICE / TEST PADS",40.64,226.06)]:
        text += f'(text "{title}" (at {x} {y} 0) (effects (font (size 1.8 1.8)) (justify left bottom)) (uuid "{uid(title)}"))'
    text += f' (sheet_instances (path "/" (page "1"))) (embedded_fonts no))\n'
    (HERE/(NAME+".kicad_sch")).write_text(text)
    (HERE/"circuit-manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(f"Wrote {len(instances)} symbols; {len(wires)} labelled pin connections; {len(ncs)} no-connects")
