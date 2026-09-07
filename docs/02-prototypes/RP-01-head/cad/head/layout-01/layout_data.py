"""Provisional spatial ledger; grams/mm. No W measurements or final inertia."""
import json
from pathlib import Path

CONTROLLER_MASS_G = 20.0  # scenario only, sweep 10/20/35 below
CROWN_INCREMENT_G = 6.0  # explicit new allowance; replace with detailed shell/mount mass

def ledger(c2=CONTROLLER_MASS_G):
    # Each original owner appears once, or is split without increasing its total.
    # Frame R rolls/pitches/yaws; P pitches/yaws; Y yaws only.
    data = [
      ('M002','display installed','R',133,(-10,0,43)),
      ('M003','window and mask','R',15,(-1,0,43)),
      ('M005','camera installed','R',10,(-10,0,94)),
      ('M006','camera cable','R',8,(-32,15,66)),
      ('M007','status light','R',5,(-8,20,94)),
      ('M008','C2 scenario','R',c2,(-27.5,-30,50)),
      ('M010','rolling cradle','R',25,(-30,0,47)),
      ('M011-P','pitch frame','P',20,(-60,0,34)),
      ('M011-Y','yaw yoke','Y',15,(-57,0,7)),
      ('M012','yaw interface','Y',20,(-40,0,-27)),
      ('M013-15-roll','roll servo housing','P',23,(-92,0,41.2)),
      ('M013-15-pitch','pitch servo housing','Y',23,(-45,39,47.5)),
      ('M013-15-horn-R','rolling horn/hub allowance','R',4,(-72,0,47)),
      ('M013-15-horn-P','pitch horn allowance','P',2,(-40,54,47)),
      ('M016-18-R','rotating bearing/shaft portions','R',6,(-54,0,47)),
      ('M016-18-P','pitch-carried bearing portions','P',8,(-54,0,47)),
      ('M016-18-Y','yaw-carried bearing portions','Y',8,(-40,0,15)),
      ('M019c','finished shell and ears','R',148,(-57.5,0,47.5)),
      ('CROWN-01','crown increment scenario','R',CROWN_INCREMENT_G,(-12,0,101)),
      ('M020-R','rolling harness','R',8,(-34,12,42)),
      ('M020-P','pitch harness','P',4,(-65,0,36)),
      ('M020-Y','yaw harness','Y',3,(-52,0,-10)),
      ('M021-R','rolling hidden/visible hardware','R',14,(-32,0,47)),
      ('M021-P','pitch hardware','P',3,(-58,0,47)),
      ('M021-Y','yaw hardware','Y',2,(-40,0,0)),
    ]
    return [dict(owner=o,name=n,frame=f,mass_g=m,center_mm=list(c),evidence='D/E allocation; M008 and CROWN-01 are scenarios') for o,n,f,m,c in data]

def com(rows, frames):
    a=[r for r in rows if r['frame'] in frames]; m=sum(r['mass_g'] for r in a)
    return dict(mass_g=m,center_mm=[sum(r['mass_g']*r['center_mm'][i] for r in a)/m for i in range(3)])

ROLL_COM=com(ledger(),'R')['center_mm']
PITCH_COM=com(ledger(),'RP')['center_mm']
ROLL_Y, ROLL_Z = ROLL_COM[1:]
PITCH_X, PITCH_Z = PITCH_COM[0],PITCH_COM[2]

if __name__=='__main__':
    result={'units':'g, mm','warning':'Provisional centre-of-mass allocation, not measured; centroid positions themselves need refinement.',
      'rows':ledger(),'scenarios':[{ 'c2_g':c,'roll':com(ledger(c),'R'),'pitch':com(ledger(c),'RP'),'yaw':com(ledger(c),'RPY')} for c in [10,20,35]]}
    Path(__file__).with_name('mass-placement.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['scenarios'],indent=2))
