# %load "firstcell.py"
import numpy
import matplotlib
from matplotlib import pylab, mlab, pyplot
np = numpy
plt = pyplot

from IPython.core.pylabtools import figsize, getfigs

from pylab import *
from numpy import *

import pathlib
import json
import bitstruct
import crcmod
import scipy.stats
from tqdm.notebook import trange, tqdm


run_times = array([7.3, 8.1, 57, 44, 23, 66, 90, 188, 189, 280, 370, 364, 217, 365, 173, 179])


fluences = array([1.13E+10, 1.25E+10, 1.02E+11, 5.18E+11, 2.61E+11, 7.96E+11, 9.98E+11, 2.03E+12, 2.03E+12, 3.03E+12, 4.01E+12, 4.03E+12, 2.47E+12, 4.06E+12, 4.01E+12, 4.05E+12])


hexa42_files = ['hexa42/Run_01_testReport_hexa42_2024-01-27_09-27-38.json',
                'hexa42/Run_02_testReport_hexa42_2024-01-27_09-35-37.json',
                'hexa42/Run_03_testReport_hexa42_2024-01-27_09-57-10.json',
                'hexa42/Run_04_testReport_hexa42_2024-01-27_10-14-15.json',
                'hexa42/Run_05_testReport_hexa42_2024-01-27_10-20-41.json',
                'hexa42/Run_06_testReport_hexa42_2024-01-27_10-28-05.json',
                'hexa42/Run_07_testReport_hexa42_2024-01-27_10-40-17.json',
                'hexa42/Run_08_testReport_hexa42_2024-01-27_10-48-27.json',
                'hexa42/Run_09_testReport_hexa42_2024-01-27_11-00-48.json',
                'hexa42/Run_10_testReport_hexa42_2024-01-27_11-14-24.json',
                'hexa42/Run_11_testReport_hexa42_2024-01-27_11-32-06.json',
                'hexa42/Run_12_testReport_hexa42_2024-01-27_11-47-10.json',
                'hexa42/Run_13_testReport_hexa42_2024-01-27_11-59-37.json',
                'hexa42/Run_14_testReport_hexa42_2024-01-27_12-20-04.json',
                'hexa42/Run_15_testReport_hexa42_2024-01-27_12-31-28.json',
                'hexa42/Run_16_testReport_hexa42_2024-01-27_13-03-00.json']


hexa43_files = ['hexa43/Run_01_testReport_hexa43_2024-01-27_09-27-37.json',
                'hexa43/Run_02_testReport_hexa43_2024-01-27_09-35-36.json',
                'hexa43/Run_03_testReport_hexa43_2024-01-27_09-57-10.json',
                'hexa43/Run_04_testReport_hexa43_2024-01-27_10-14-15.json',
                'hexa43/Run_05_testReport_hexa43_2024-01-27_10-20-41.json',
                'hexa43/Run_06_testReport_hexa43_2024-01-27_10-28-04.json',
                'hexa43/Run_07_testReport_hexa43_2024-01-27_10-40-18.json',
                'hexa43/Run_08_testReport_hexa43_2024-01-27_10-48-28.json',
                'hexa43/Run_09_testReport_hexa43_2024-01-27_11-00-49.json',
                'hexa43/Run_10_testReport_hexa43_2024-01-27_11-14-25.json',
                'hexa43/Run_11_testReport_hexa43_2024-01-27_11-32-08.json',
                'hexa43/Run_12_testReport_hexa43_2024-01-27_11-47-12.json',
                'hexa43/Run_13_testReport_hexa43_2024-01-27_11-59-39.json',
                'hexa43/Run_14_testReport_hexa43_2024-01-27_12-20-06.json',
                'hexa43/Run_15_testReport_hexa43_2024-01-27_12-31-29.json',
                'hexa43/Run_16_testReport_hexa43_2024-01-27_13-03-01.json']

PRBS_run_times = array([180., 180., 178.,  41.])

PRBS_fluences = array([4.03e+12, 4.04e+12, 4.03e+12, 9.18e+11])

hexa42_PRBS_files = ['hexa42/Run_17_PRBS_testReport_hexa42_2024-01-27_13-13-46.json',
                     'hexa42/Run_18_PRBS_testReport_hexa42_2024-01-27_13-21-17.json',
                     'hexa42/Run_19_PRBS_testReport_hexa42_2024-01-27_13-28-48.json',
                     'hexa42/Run_22_PRBS_testReport_hexa42_2024-01-27_13-52-10.json']


hexa43_PRBS_files = ['hexa43/Run_17_PRBS_testReport_hexa43_2024-01-27_13-13-25.json',
                     'hexa43/Run_18_PRBS_testReport_hexa43_2024-01-27_13-21-08.json',
                     'hexa43/Run_19_PRBS_testReport_hexa43_2024-01-27_13-28-38.json',
                     'hexa43/Run_22_PRBS_testReport_hexa43_2024-01-27_13-52-00.json']


def hexprint(N=8):
    return numpy.printoptions(formatter={"int": lambda x: f"{x:0{N}x}"}, threshold=10000000000)


@vectorize
def yerr(k):
    alpha = scipy.stats.chi(1).cdf(1)
    xs = linspace(0, scipy.stats.gamma(k+1).ppf(1-alpha)-1e-12, 1000)
    min_x = xs[argmin(scipy.stats.gamma(k+1).ppf(scipy.stats.gamma(k+1).cdf(xs) + alpha) - xs)]
    max_x = scipy.stats.gamma(k+1).ppf(scipy.stats.gamma(k+1).cdf(min_x) + alpha)
    return k - min_x, max_x - k


@vectorize
def pois_err(k):
    alpha = scipy.stats.chi(1).cdf(1)
    xs = linspace(0, scipy.stats.gamma(k+1).ppf(1-alpha)-1e-12, 1000)
    min_x = xs[argmin(scipy.stats.gamma(k+1).ppf(scipy.stats.gamma(k+1).cdf(xs) + alpha) - xs)]
    max_x = scipy.stats.gamma(k+1).ppf(scipy.stats.gamma(k+1).cdf(min_x) + alpha)
    return max_x - min_x


class items:
    def __init__(self, item_list):
        self.item_list = item_list
        
    def __getitem__(self, key):
        if isinstance(key, slice):
            return items(self.item_list[key])
        else:
            return self.item_list[key]
        
    def __len__(self):
        return len(self.item_list)
    
    def __iter__(self):
        return iter(self.item_list)
        
    def __getattr__(self, name):
        return array([batch.__getattribute__(name) for batch in self.item_list])
    
    def __add__(self, other):
        return items(self.item_list + other.item_list)
    
    
class packet_parser:
    def __init__(self, J):
        self.crc = crcmod.mkCrcFun(0x104c11db7,initCrc=0, xorOut=0, rev=False)
        self.J = J
        self.prebeam_data = array(J['tests'][1]['metadata']['daq_asic_before_beam'], dtype=uint32)
        flatdata = self.prebeam_data[:,::-1].flatten()
        B = bytes(flatdata.byteswap().data)
        total_len = len(B)
        progbar = tqdm(total=total_len)
        
        start = 0
        codes = []
        packet_nums = []
        self.packets = []
        packet_num = 0
        while len(B) >= 8:
            header, _, _, _ = self.parse_header(B)
            if header['header marker'] == 0x1e6:
                packet, B, size, packet_codes = self.parse_packet(B)
                self.packets.append(packet)
                codes.extend(packet_codes)
                packet_nums.extend([packet_num]*len(packet_codes))
                packet_num += 1
                start += size
                progbar.update(size)
            else:
                idle, B, idle_size, idle_codes = self.parse_idle(B)
                start += idle_size
                progbar.update(idle_size)
                codes.extend(idle_codes)
                packet_nums.append(-1)
                # assert idle['idle marker'] == 0x555555
        codes.append(0) # Final idle word that we don't attempt to process
        progbar.update(4)
        progbar.refresh()
        packet_nums.append(-1)
        
        self.code_data = array(codes, dtype=uint16).reshape(self.prebeam_data.shape)[:,::-1]
        self.packet_num = array(packet_nums, dtype=uint8).reshape(self.prebeam_data.shape)[:,::-1]
        
        self.subpack = self.code_data // 100
        self.subcode = self.code_data % 100
        self.subp_any = numpy.isin(self.subcode, (5,6,7,8))

    def get(self, F, B):
        format_string = ''.join([f'u{n}' for n, name in F])
        names = [name for n, name in F]
        return bitstruct.unpack_dict(format_string, names, B)

    def parse_idle(self, B):
        F = [(24, 'idle marker'),
             (2, 'RR'),
             (3, 'Err'),
             (3, 'Buffer status')]
        return self.get(F, B), B[4:], 4, [0]

    def parse_packet(self, B):
        ret = dict()
        codes = []
        ret["header"], Bbody, header_size, header_codes = self.parse_header(B)
        codes.extend(header_codes)
        payload_length = ret["header"]["payload length"]
        expected_crc = f"{self.crc(Bbody[:(payload_length-1)*4]):08x}"
        body_size = 0
        for i in range(12):
            ret[i], Bbody, subpacket_size, subpacket_codes = self.parse_subpacket(Bbody)
            body_size += subpacket_size
            codes.extend([c + 100*i for c in subpacket_codes])
        ret['CRC'] = Bbody[:4].hex()
        Bbody = Bbody[4:]
        ret['expCRC'] = expected_crc
        codes.append(3)
        body_size += 4
        idle, Bbody, _, _ = self.parse_idle(Bbody)
        ret['Mandatory idle'] = idle
        codes.append(4)
        body_size += 4

        # print(body_size, payload_length*4, payload_length)
        # assert body_size == payload_length*4

        return ret, Bbody, body_size+header_size, codes

    def parse_header(self, B):
        F = [(9, "header marker"),
             (9, "payload length"),
             (1, "P"),
             (1, "E"),
             (2, "HT"),
             (2, "EBO"),
             (1, "M"),
             (1, "T"),
             (6, "Event hamming"),
             (12, "BX"),
             (6, "L1A number"),
             (3, "Orbit"),
             (1, "S"),
             (2, "RR"),
             (8, "header CRC"),
            ]
        return self.get(F, B), B[2*4:], 2*4, [1, 2]

    def parse_subpacket(self, B):
        ret = dict()
        codes = []
        ret["header"], B, header_size, header_codes = self.parse_subpacket_header(B)
        codes.extend(header_codes)
        if ret["header"]["F"] == 0:
            ret["body"], B, body_size, body_codes = self.parse_subpacket_body(B, ret["header"]["channel map"])
            codes.extend(body_codes)
            return ret, B, header_size+body_size, codes
        else:
            return ret, B, header_size, codes

    def parse_subpacket_header(self, B):
        F = [(3, 'Stat'),
             (3, 'Ham'),
             (1, 'F'),

             (10, 'CM0'),
             (10, 'CM1'),
             (37, 'channel map')]
        result = self.get(F, B)
        if result["F"] == 0:
            result['raw'] = B[:8].hex()
            return result, B[2*4:], 2*4, [5, 6]

        F = [(3, 'Stat'),
             (3, 'Ham'),
             (1, 'F'),
             (10, 'CM0'),
             (10, 'CM1'),
             (1, 'E'),
             (4, 'zeros')]
        result = self.get(F, B)
        result['raw'] = B[:4].hex()
        return result, B[1*4:], 1*4, [7]

    def parse_subpacket_body(self, B, channel_map):
        ret = dict()
        body_size = 0
        for i in range(37):
            if ((channel_map >> i) & 0b1):
                result, B, size = self.parse_channel_data(B)
                ret[i] = result
                body_size += size
            else:
                ret[i] = None
        pad = (-body_size) % 4
        return ret, B[pad:], body_size+pad, [8]*int(ceil(body_size/4))

    def parse_channel_data(self, B):
        F = [(4, "code"),
             (10, "ADC-1"),
             (10, "ADC/TOT")]
        result = self.get(F, B)
        if result["code"] == 0b0000 or result["code"] == 0b0010:
            result['raw'] = B[:3].hex()
            return result, B[3:], 3

        F = [(4, "code"),
             (10, "ADC/TOT"),
             (2, "extra")]
        result = self.get(F, B)
        if result["code"] == 0b0001:
            result['raw'] = B[:2].hex()
            return result, B[2:], 2

        F = [(4, "code"),
             (10, "ADC/TOT"),
             (10, "TOA")]
        result = self.get(F, B)
        if result["code"] == 0b0011:
            result['raw'] = B[:3].hex()
            return result, B[3:], 3

        F = [(2, "code"),
             (10, "ADC-1"),
             (10, "ADC/TOT"),
             (10, "TOA")]
        result = self.get(F, B)
        if result["code"] == 0b01 or result["code"] == 0b11 or result["code"] == 0b10:
            result["code"] = result["code"] << 2
            result['raw'] = B[:4].hex()
            return result, B[4:], 4

        raise ValueError(f"Could not parse channel data {B[0]:08b}")
        
        
class capture_batch:
    def __init__(self, ASIC, EMU, percap, prebeam):
        self.ASIC = ASIC
        self.EMU = EMU
        self.percap = percap
        for i in range(percap):
            match = (EMU[i] == prebeam.prebeam_data).all(axis=1)
            if sum(match) == 1:
                self.row = match.nonzero()[0][0] - i
                break
            elif sum(match) > 1:
                self.row = 0
        self.packet = amin(prebeam.packet_num[self.row:self.row+percap])
        
        
class incident:
    def __init__(self, batch_group, percap, prebeam):
        ASIC = concatenate(batch_group.ASIC, dtype=uint32)
        EMU = concatenate(batch_group.EMU, dtype=uint32)
        
        rows = items(batch_group).row
        cap_rows = concatenate([row + arange(percap) for row in rows])
        
        packet = batch_group[0].packet
        if packet == 255:
            packet_rows = cap_rows
        else:
            packet_rows = (prebeam.packet_num == packet).nonzero()[0]
        
        first_row = min(rows[0], packet_rows[0])
        last_row = max(rows[-1] + percap, packet_rows[-1] + 1)
        self.N_row = last_row - first_row
        
        self.prebeam_packet = prebeam.prebeam_data[first_row : last_row]
        
        self.ASIC_packet = zeros_like(self.prebeam_packet)
        self.EMU_packet  = zeros_like(self.prebeam_packet)
        self.ASIC_packet[cap_rows - first_row] = ASIC
        self.EMU_packet [cap_rows - first_row] = EMU
        
        self.xor = self.ASIC_packet ^ self.EMU_packet
        
        self.cap = zeros_like(self.prebeam_packet, bool)
        self.cap[cap_rows - first_row] = True
        
        self.gap = zeros_like(self.prebeam_packet, bool)
        gap_indices = cap_rows - first_row + 4
        gap_indices = gap_indices[gap_indices < (last_row - first_row)]
        self.gap[gap_indices] = True
        
        self.known = self.cap | ~self.gap
        self.mismatch = self.ASIC_packet != self.EMU_packet
        code = prebeam.code_data[first_row : last_row]
        subpack = prebeam.subpack[first_row : last_row]
        subcode = prebeam.subcode[first_row : last_row]
        subp_any = prebeam.subp_any[first_row : last_row]
        
        tri_logic = 1 * ~self.known + 2 * self.mismatch
        
        idle = tri_logic[code == 0].max(initial=0)
        
        packet_header_0 = tri_logic[code == 1].max(initial=0)
        Payload_Length = any((self.xor[code == 1] & 0x007fc000) != 0) * packet_header_0
        Header_Hamming = any((self.xor[code == 1] & 0x0000003f) != 0) * packet_header_0
        
        packet_header_1 = tri_logic[code == 2].max(initial=0)
        L1A_orbit    = any((self.xor[code == 2] & 0x000ff800) != 0) * packet_header_1
        Header_CRC   = any((self.xor[code == 2] & 0x000000ff) != 0) * packet_header_1
        
        Event_Header = max(any((self.xor[code == 1] & 0xff803fc0) != 0) * packet_header_0,
                           any((self.xor[code == 2] & 0xfff00700) != 0) * packet_header_1)
        
        # Find which subpackets, if any, have some error, or even just unknowns
        subpacket_errors = array([tri_logic[(subpack == i) & subp_any].max(initial=0) for i in range(12)])
        
        # Find the first subpacket, if any, that definitely has an error
        if any(subpacket_errors == 2):
            first_subpacket = (subpacket_errors == 2).nonzero()[0][0]
        else:
            first_subpacket = -1
        
        # Examine the headers and data of that first subpacket with an error
        head0 = (subpack == first_subpacket) & ((subcode == 5) | (subcode == 7))
        head1 = (subpack == first_subpacket) & (subcode == 6)
        first_subp_head_0 = tri_logic[head0].max(initial=0)
        first_subp_head_1 = tri_logic[head1].max(initial=0)
        
        first_subp_CRC   = any((self.xor[head0] & 0x20000000) != 0) * first_subp_head_0
        first_subp_CM    = any((self.xor[head0] & 0x01ffffe0) != 0) * first_subp_head_0
        first_subp_head  = any((self.xor[head0] & 0xde000000) != 0) * first_subp_head_0
        first_subp_chmap = max(any((self.xor[head0] & 0x0000001f) != 0) * first_subp_head_0, first_subp_head_1)
        first_subp_data = tri_logic[(subpack == first_subpacket) & (subcode == 8)].max(initial=0)
            
        # Check whether any later subpackets had errors, too
        later_subp_errors = subpacket_errors[first_subpacket+1:].max(initial=0)
        
        # Packet CRC and Mandatory IDLE
        CRC  = tri_logic[code == 3].max(initial=0)
        Mand = tri_logic[code == 4].max(initial=0)

        #                       13           12               11               10                  9               8
        summary = array([first_subp_CRC, first_subp_CM, first_subp_head, first_subp_chmap, first_subp_data, later_subp_errors,
                         Payload_Length, Header_Hamming, L1A_orbit, Header_CRC, Event_Header, CRC, Mand, idle])
        #                        7            6              5           4          3          2     1     0
        
        self.pattern = int(sum(summary * 10**arange(summary.shape[0])[::-1]))
        
    def __str__(self):
        outputs = []
        with hexprint():
            for row in range(self.N_row):
                output_row = [self.prebeam_packet[row], ' ' if self.known[row].all() else 'G']
                if self.cap[row].any():
                    output_row.append(self.ASIC_packet[row])
                    
                if any(self.mismatch[row]):
                    output_row.append(str(self.xor[row]).translate(str.maketrans({'0': '-'})))
                outputs.append(' '.join([str(x) for x in output_row]))
        return '\n'.join(outputs)
    
    
class run:
    def __init__(self, J=None, percap=None, prebeam=None, swap=False):
        if J is not None:
            self.J = J
            self.percap = percap

            if swap:
                ASIC_name = 'emu'
                EMU_name = 'asic'
            else:
                ASIC_name = 'asic'
                EMU_name = 'emu'

            if 'daq_asic' in self.J['tests'][3]['metadata'] and 'daq_emu' in self.J['tests'][3]['metadata']:
                self.ASIC_beam = array(self.J['tests'][3]['metadata'][f'daq_{ASIC_name}'], dtype=uint32)
                self.EMU_beam  = array(self.J['tests'][3]['metadata'][f'daq_{EMU_name}'],  dtype=uint32)
            else:
                self.ASIC_data = []
                self.EMU_data = []
                for k in self.J['tests'][3]['metadata'].keys():
                    if ASIC_name in k:
                        self.ASIC_data.append(array(self.J['tests'][3]['metadata'][k], dtype=uint32))
                    if EMU_name in k:
                        self.EMU_data.append(array(self.J['tests'][3]['metadata'][k], dtype=uint32))

                self.ASIC_beam = concatenate(self.ASIC_data).reshape(-1, 6)
                self.EMU_beam = concatenate(self.EMU_data).reshape(-1, 6)
            # if swap:
            #     self.ASIC_beam = array(self.J['tests'][3]['metadata']['daq_emu_post_beam'], dtype=uint32)
            #     self.EMU_beam = array(self.J['tests'][3]['metadata']['daq_asic_post_beam'], dtype=uint32)
            # else:
            #     self.ASIC_beam = array(self.J['tests'][3]['metadata']['daq_asic_post_beam'], dtype=uint32)
            #     self.EMU_beam = array(self.J['tests'][3]['metadata']['daq_emu_post_beam'], dtype=uint32)

            self.batches = items([capture_batch(self.ASIC_beam[i*percap:(i+1)*percap],
                                                self.EMU_beam[i*percap:(i+1)*percap],
                                                percap, prebeam) for i in range(self.EMU_beam.shape[0] // percap)])

            def find_batch_groups(batches, percap):
                p = None
                r = None
                batch_group = []
                for b in batches:
                    if p is not None and (b.row < (r + percap) or b.packet != p or (b.packet == 255 and p == 255)):
                        yield batch_group
                        batch_group = []
                    batch_group.append(b)
                    p = b.packet
                    r = b.row
                if len(batch_group) > 0:
                    yield batch_group

            self.batch_groups = list(find_batch_groups(self.batches, self.percap))

            self.incidents = items([incident(items(batch_group), percap, prebeam) for batch_group in self.batch_groups])
    
    def __add__(self, other):
        out = run()
        out.ASIC_beam = concatenate([self.ASIC_beam, other.ASIC_beam])
        out.EMU_beam = concatenate([self.EMU_beam, other.EMU_beam])
        out.batches = self.batches + other.batches
        out.batch_groups = self.batch_groups + other.batch_groups
        out.incidents = self.incidents + other.incidents
        return out