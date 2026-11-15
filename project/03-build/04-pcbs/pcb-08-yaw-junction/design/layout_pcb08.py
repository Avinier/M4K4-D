"""D-107 PCB-08 rev B: headless, explicitly hand-routed W47 junction.

KiCad 10.99 / kfile workflow. Coordinates are KiCad mm, world=(x-100,100-y).
J1 input and J3 output use identical numbered Micro-Fit land patterns; their
opposed mouths account for the reversed physical row order. No autorouter.
"""
import json
import re
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools"))
import kfile as K
BOARD = HERE / "pcb-08-yaw-junction.kicad_pcb"
LIB = Path("/Applications/KiCad-nightly/KiCad.app/Contents/SharedSupport/footprints")
MF = "Molex_Micro-Fit_3.0_43045-0621_2x03-1MP_P3.00mm_Horizontal"
GH = "JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical"
PLACE = {"J1": (85,138.5,90), "J2": (95.7,124.8,180),
         "J3": (105,133,270), "J4": (94,135,90),
         "J5": (81.5,124,0), "J6": (91.5,144,0),
         "R1": (104,124,0), "TP1": (110,124,0), "TP2": (110,145,0)}

def setup(b):
    b.drop(lambda kind, raw: kind in ("segment", "via", "zone") or
           kind in ("gr_line", "gr_rect") and ('(layer "Edge.Cuts")' in raw or '(layer "Dwgs.User")' in raw))
    # Swap before moving: replace_footprint keeps the old rotation; reset it
    # before the swap so library pad angles start at zero.
    for ref, folder, name in (("J3", HERE.parents[1]/"lib/pcb08.pretty", MF),
                              ("J4", LIB/"Connector_JST.pretty", GH)):
        b.move(ref, 100,130,0)
        K.replace_footprint(b,ref,folder,name)
    if '(4 "In1.Cu"' not in b.text:
        b.text=b.text.replace('(0 "F.Cu" signal)','(0 "F.Cu" signal)\n\t\t(4 "In1.Cu" signal)\n\t\t(6 "In2.Cu" signal)')
        b._index()
    manifest=json.loads((HERE/"circuit-manifest.json").read_text())
    for ref in ("J3", "J4"):
        b.set_pad_nets(ref,{p:"/"+n for p,n in manifest[ref]["pins"].items() if n})
        raw=next(s for s in b.blocks("footprint") if f'(property "Reference" "{ref}"' in s)
        new=re.sub(r'\(property "Value" "[^"]*"',f'(property "Value" "{manifest[ref]["value"]}"',raw,count=1)
        b.text=b.text.replace(raw,new); b._index()
    for ref,(x,y,rot) in PLACE.items(): b.move(ref,x,y,rot)
    for a,c in zip([(78,121),(112,121),(112,146),(78,146)],[(112,121),(112,146),(78,146),(78,121)]):
        b.add(K.edge_line(str(a),a,c,.05))
    b.text=b.text.replace('(rev "A")','(rev "B")').replace('(date "2026-11-09")','(date "2026-11-13")')
    # Assembly labels are on Fab, leaving no overlapping tiny silk.
    b.text=b.text.replace('(layer "F.SilkS")','(layer "F.Fab")')
    b._index()

def route(b):
    def t(name,layer,net,w,*pts): b.add(*K.track(name,pts,w,layer,"/"+net))
    def v(name,p,net): b.add(K.via(name,p,"/"+net))
    # Four independently planned B.Cu lanes; differential partners stay adjacent.
    for i,(net,j2,j4) in enumerate((("C0TX_P",2,2),("C0TX_N",3,3),("C2TX_N",4,4),("C2TX_P",5,5))):
        src=b.pad("J2",j2)["at"];dst=b.pad("J4",j4)["at"]
        sv=(src[0],124.5+i*.8);outer=99.2-i*.8;ev=(outer,138.8 if i==0 else dst[1])
        v(net+"_in",sv,net);v(net+"_out",ev,net)
        t(net+"_stub1","F.Cu",net,.2,src,sv)
        t(net+"_lane","B.Cu",net,.2,sv,(outer,sv[1]+outer-sv[0]),(outer,ev[1]),ev)
        if i==0:
            t(net+"_stub2","F.Cu",net,.2,ev,(99.2,137.475),(98.6,136.875),dst)
        else: t(net+"_stub2","F.Cu",net,.2,ev,dst)
    # Inner layers keep the six power nets separate without routing them
    # through the GH signal fan-out. No ground planes join their returns.
    t("head_supply","In1.Cu","+6V3_HEAD_PR",1.,(85,138.5),(85,141.8),(106.8,141.8),(106.8,131.2),(105,133))
    t("c2_supply","In1.Cu","+5V_C2",.5,(85,135.5),(86.4,134.1),(90.1,134.1),(93.4,130.8),(100,130.8),(100,134.1),(100.4,134.5),(103.5,134.5),(105,136))
    t("display_supply","In1.Cu","+5V_DISPLAY",.5,(85,132.5),(83,134.5),(83,137.25),(103.25,137.25),(105,139))
    t("head_return","In2.Cu","GND_HEAD",1.,(88,138.5),(89.5,140),(89.5,142),(100.5,142),(100.5,134.5),(102,133))
    t("c2_return","In2.Cu","GND_C2",.5,(88,135.5),(90,133.5),(91.5,132),(91.5,130),(103.5,130),(103.5,134.5),(102,136))
    t("display_return","In2.Cu","GND_DISPLAY",.5,(88,132.5),(86.5,134),(86.5,137.1),(98,137.1),(98,140))
    v("display_return_bridge",(98,140),"GND_DISPLAY")
    t("display_return_bridge","F.Cu","GND_DISPLAY",.5,(98,140),(101,140),(102,139))
    t("yaw_supply","B.Cu","+11V1_YAW",1.5,(84,124),(84,126),(83.3175,126.6825),(83.3175,140),(87.3175,144),(91.5,144))
    # GND_SIG remains separate from all three head power returns.
    t("yaw_ground","F.Cu","GND_SIG",1.5,(81.5,124),(81.5,126),(83.3175,127.8175),(83.3175,142.4175),(84.9,144),(89.5,144),(89.5,142),(94.1,142),(96.1,144))
    t("sig_return","F.Cu","GND_SIG",.3,(95.95,138.125),(96.1,138.275),(96.1,144))
    t("gnd_test_join","F.Cu","GND_SIG",.3,(96.1,144),(97.1,145),(110,145))
    v("r1_sig",(106.4,124),"GND_SIG")
    t("r1_stub","F.Cu","GND_SIG",.3,(104.9125,124),(106.4,124))
    t("r1_ground","B.Cu","GND_SIG",.3,(106.4,124),(111.55,124),(111.55,143.45),(110,145))
    v("ground_test",(110,145),"GND_SIG")
    t("link_ground","F.Cu","LINK_GND",.2,(98.825,122.85),(101.9375,122.85),(103.0875,124))
    # Single-ended bus; test pad branches only on the stationary board.
    sv=(94.8,131.875);v("servo_out",sv,"SERVO_DATA")
    t("servo_out_stub","F.Cu","SERVO_DATA",.2,(95.95,131.875),sv)
    t("servo_main","B.Cu","SERVO_DATA",.2,(86.5,124),(87.5,125),(87.5,126.3),(91,129.8),(92.725,129.8),sv)
    t("servo_test","F.Cu","SERVO_DATA",.2,sv,(97.875,128.8),(110,128.8),(110,124))
    # Dedicated fills, each carrying exactly one named power net. Solid
    # pad connections avoid thermal spokes bottlenecking the head rail.
    for name,layer,net in [('HEAD_POSITIVE_FILL','In1.Cu','+6V3_HEAD_PR'),
                           ('HEAD_RETURN_FILL','In2.Cu','GND_HEAD')]:
        b.add(K.pour(name,layer,'/'+net,[(78.3,121.3),(111.7,121.3),(111.7,145.7),(78.3,145.7)],
                     clearance=.2,min_width=.25,solid=True))

def main():
    b=K.Board(BOARD); setup(b); route(b); b.save()
    d=K.drc(BOARD,HERE/"placement-drc.json")
    print({k:v for k,v in d.items() if k!="report"})
    print(K.summary(d["report"]))
    for ref in PLACE:
        print(ref,[(p["num"],p["at"],p["net"]) for p in b.fp(ref)["pads"] if p["num"]!="MP"])
if __name__=="__main__": main()
