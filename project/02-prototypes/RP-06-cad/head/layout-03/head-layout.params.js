// Generated; presentation only. Per-part scene-tree controls remain available.
const axes={"roll_y": -1.1053356325240153, "roll_z": 46.9191299433943, "pitch_x": -37.9645316623177, "pitch_z": 45.55341378595055};
const clamp=(v,a,b)=>Math.max(a,Math.min(b,Number(v)||0));
export default {manifest:{
  "schemaVersion": 1,
  "step": {
    "path": "head/layout-03/head-layout.step"
  },
  "parameters": {
    "roll_deg": {
      "type": "number",
      "label": "Roll",
      "unit": "\u00b0",
      "min": -18,
      "max": 18,
      "step": 1,
      "default": 0
    },
    "pitch_deg": {
      "type": "number",
      "label": "Pitch",
      "unit": "\u00b0",
      "min": -22,
      "max": 40,
      "step": 1,
      "default": 0
    },
    "yaw_deg": {
      "type": "number",
      "label": "Yaw",
      "unit": "\u00b0",
      "min": -55,
      "max": 55,
      "step": 1,
      "default": 0
    },
    "show_physical": {
      "type": "boolean",
      "label": "Show physical",
      "default": true
    },
    "show_physics": {
      "type": "boolean",
      "label": "Show physics",
      "default": true
    },
    "show_harness": {
      "type": "boolean",
      "label": "Show harness",
      "default": true
    },
    "show_annotations": {
      "type": "boolean",
      "label": "Show annotations",
      "default": false
    },
    "show_fov": {
      "type": "boolean",
      "label": "Show fov",
      "default": true
    },
    "show_shell": {
      "type": "boolean",
      "label": "Show shell",
      "default": true
    }
  },
  "features": {
    "frame_R": {
      "ref": "#o1.3.3.1,o1.3.3.2,o1.3.3.3,o1.3.1.1,o1.3.1.2,o1.3.1.3,o1.3.5.1,o1.4.3.1,o1.4.3.2,o1.4.4.5,o1.4.2.3,o1.4.2.5,o1.4.4.3,o1.4.4.1,o1.4.2.7,o1.4.2.4,o1.4.1.6,o1.4.1.7,o1.4.1.5,o1.4.1.4,o1.4.1.10,o1.4.1.11,o1.4.1.9,o1.4.1.8,o1.4.1.1,o1.4.1.2,o1.4.2.6,o1.4.1.3,o1.4.4.4,o1.4.4.2,o1.4.2.2,o1.4.2.1,o1.2.3.4,o1.3.2.1,o1.3.2.2,o1.3.2.3,o1.2.2.1,o1.1.1.3,o1.1.1.4,o1.1.1.2,o1.1.1.5,o1.1.1.1,o1.2.3.2"
    },
    "frame_P": {
      "ref": "#o1.4.5.3,o1.4.7.3,o1.4.7.4,o1.4.7.1,o1.4.7.2,o1.4.7.5,o1.4.5.4,o1.4.5.1,o1.4.5.2,o1.4.5.5,o1.4.5.6,o1.2.2.2,o1.1.2.3,o1.1.2.2,o1.1.2.1,o1.2.3.3,o1.2.1.2,o1.3.4.1,o1.3.4.2,o1.3.4.3"
    },
    "frame_Y": {
      "ref": "#o1.3.6.2,o1.4.6.1,o1.4.6.2,o1.4.8.4,o1.4.8.1,o1.4.8.2,o1.4.8.3,o1.2.2.3,o1.3.6.1,o1.1.3.1,o1.1.3.2,o1.2.1.3"
    },
    "physical": {
      "ref": "#o1.1"
    },
    "physics": {
      "ref": "#o1.2"
    },
    "harness": {
      "ref": "#o1.3"
    },
    "annotations": {
      "ref": "#o1.4"
    },
    "fov": {
      "ref": "#o1.2.3.4"
    },
    "shell": {
      "names": [
        "front_bezel_integral_camera_crown",
        "main_octagonal_skin",
        "removable_octagonal_rear_cover",
        "ear_-1_ridged_inner_mount",
        "ear_-1_hollow_removable_cap",
        "ear_-1_amber_inlay",
        "ear_-1_dark_centre",
        "ear_1_ridged_inner_mount",
        "ear_1_hollow_removable_cap",
        "ear_1_amber_inlay",
        "ear_1_dark_centre"
      ]
    }
  }
},
update({params,effects}) {
 const r={rotate:{axis:[1,0,0],origin:[0,axes.roll_y,axes.roll_z],angleDeg:clamp(params.roll_deg,-18,18)}};
 const p={rotate:{axis:[0,1,0],origin:[axes.pitch_x,0,axes.pitch_z],angleDeg:clamp(params.pitch_deg,-22,40)}};
 const y={rotate:{axis:[0,0,1],origin:[axes.pitch_x,0,-60],angleDeg:clamp(params.yaw_deg,-55,55)}};
 effects.transform('frame_R',{transforms:[r,p,y]});
 effects.transform('frame_P',{transforms:[p,y]});
 effects.transform('frame_Y',y);
 for (const key of ['physical','physics','harness','annotations']) effects.visible(key,params['show_'+key]!==false);
 effects.visible('fov',params.show_physics!==false && params.show_fov!==false);
 effects.visible('shell',params.show_physical!==false && params.show_shell!==false);
}};
