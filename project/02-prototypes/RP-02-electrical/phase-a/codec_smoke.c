#include "codec.h"
#include <stdio.h>

int main(void) {
    rp02_frame in = {0}, out = {0};
    uint8_t wire[RP02_MAX_WIRE];
    size_t used = 0;
    in.type = RP02_HEAD_GOAL;
    in.seq = 19;
    in.epoch = 7;
    in.src_ts_us = 123456789;
    for (unsigned i = 0; i < 16; ++i) in.boot_uuid[i] = (uint8_t)i;
    in.payload_len = 4;
    in.payload[0] = 0; in.payload[1] = 'a'; in.payload[2] = 0; in.payload[3] = 'b';
    if (rp02_encode(&in, wire, sizeof(wire), &used) || rp02_decode(wire, used, &out)) return 1;
    /* Golden vector from the generated Python codec, including delimiter. */
    static const uint8_t golden[] = {
        0x04,0x02,0x05,0x13,0x01,0x11,0x01,0x02,0x03,0x04,0x05,
        0x06,0x07,0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x0e,0x0f,0x07,
        0x01,0x01,0x05,0x15,0xcd,0x5b,0x07,0x01,0x01,0x01,0x02,
        0x04,0x02,0x61,0x04,0x62,0xfb,0xa8,0x00
    };
    if (used != sizeof(golden) || memcmp(wire, golden, used)) return 4;
    if (out.type != in.type || out.seq != in.seq || out.epoch != in.epoch ||
        out.src_ts_us != in.src_ts_us || out.payload_len != in.payload_len ||
        memcmp(out.boot_uuid, in.boot_uuid, 16) || memcmp(out.payload, in.payload, 4)) return 2;
    wire[10] ^= 1;
    if (rp02_decode(wire, used, &out) == 0) return 3;
    puts("C codec round-trip and CRC rejection OK");
    return 0;
}
