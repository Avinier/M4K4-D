// RP-03 Layout 01 review controls. Geometry dimensions remain Python-owned.
const clamp = (value, min, max) => Math.max(min, Math.min(max, Number(value) || 0));

export default {
  manifest: {
    schemaVersion: 1,
    step: {
      path: "docs/02-prototypes/RP-03-locomotion/cad/body-chassis/layout-01/body-chassis.step"
    },
    parameters: {
      head_yaw_deg: {
        type: "number",
        label: "Head yaw",
        unit: "°",
        min: -55,
        max: 55,
        step: 1,
        default: 0
      },
      show_shell: {
        type: "boolean",
        label: "Show translucent shell",
        default: true
      },
      show_head: {
        type: "boolean",
        label: "Show RP-01 Layout 03 head",
        default: true
      },
      show_structure: {
        type: "boolean",
        label: "Show body/chassis structure",
        default: true
      },
      show_drive: {
        type: "boolean",
        label: "Show drivetrain",
        default: true
      },
      show_rear_tail: {
        type: "boolean",
        label: "Show rear skid / TCRT module",
        default: true
      },
      show_electronics: {
        type: "boolean",
        label: "Show electronics",
        default: true
      },
      show_sensors: {
        type: "boolean",
        label: "Show sensors",
        default: true
      },
      show_harness: {
        type: "boolean",
        label: "Show harness routes",
        default: true
      },
      show_physics: {
        type: "boolean",
        label: "Show physics overlays",
        default: false
      }
    },
    features: {
      shell: {
        names: ["BODY_SHELL", "BODY_PANELS", "LOWER_MOBILITY_BELT"]
      },
      head: {
        ref: "#o1.17"
      },
      structure: {
        ref: "#o1.1,o1.2"
      },
      drive: {
        ref: "#o1.3,o1.4,o1.5,o1.6,o1.7,o1.8,o1.9"
      },
      rear_tail: {
        ref: "#o1.10"
      },
      electronics: {
        ref: "#o1.11"
      },
      sensors: {
        ref: "#o1.12"
      },
      harness: {
        ref: "#o1.13,o1.17.3"
      },
      physics: {
        ref: "#o1.18,o1.17.2"
      }
    }
  },
  update({ params, effects }) {
    effects.transform("head", {
      transforms: [{
        rotate: {
          axis: [0, 0, 1],
          origin: [-37.9645316623177, 0, -60],
          angleDeg: clamp(params.head_yaw_deg, -55, 55)
        }
      }]
    });
    for (const key of ["shell", "head", "structure", "drive", "rear_tail", "electronics", "sensors", "harness", "physics"]) {
      effects.visible(key, params[`show_${key}`] !== false);
    }
  }
};
