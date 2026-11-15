"""Check W47 against exported PCB-08 and PCB-12 netlists, including the head bonds."""
import json
from pathlib import Path
import audit_netlist as A
K=A.K
HERE=Path(__file__).resolve().parent

def netmap(path):
    doc=K.parse(path.read_text())
    return {(K.find(n,"ref")[1],K.find(n,"pin")[1]):K.find(net,"name")[1].lstrip("/")
            for net in K.find(doc,"nets")[1:] for n in K.find_all(net,"node")}

def main():
    a=netmap(HERE/"pcb-08-yaw-junction.net")
    b=netmap(HERE.parents[1]/"pcb-12-c2-head-carrier/design/pcb-12-c2-head-carrier.net")
    p=lambda d,r,n:d.get((r,str(n)))
    checks={"body_power": [p(a,"J3",n) for n in range(1,7)]==["+6V3_HEAD_PR","+5V_C2","+5V_DISPLAY","GND_HEAD","GND_C2","GND_DISPLAY"],
            "body_signals": [p(a,"J4",n) for n in range(1,7)]==["GND_SIG","C0TX_P","C0TX_N","C2TX_N","C2TX_P","SERVO_DATA"],
            "pcb12_j1": [p(b,"J1",n) for n in range(1,8)]==["GND_SIG","C0TX_P","C0TX_N","C2TX_N","C2TX_P","+5V_C2","GND"],
            "servo_branch_in_head": [p(b,"J2",n) for n in (1,2)]==["GND_HEAD_REF","SERVO_DATA"],
            "head_ground_bonds": all([p(b,r,1),p(b,r,2)]==[net,"GND"] for r,net in (("R1","GND_SIG"),("R7","GND_HEAD_REF"),("R10","GND_DISPLAY")))}
    out=dict(result="PASS" if all(checks.values()) else "FAIL",checks=checks,
             release_holds=["K2: status LED driver remains unassigned; assign and audit before PCB-12 order",
                            "K3: D1 power inlet and received servo cavity order remain unverified",
                            "Three servo conductors cross roll; GND_HEAD/SERVO_DATA branch to J2 is made in the head clamp fan-out"])
    (HERE/"w47-interface-audit.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2));raise SystemExit(not all(checks.values()))
if __name__=="__main__":main()
