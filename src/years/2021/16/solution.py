
from math import prod
from operator import eq, gt, lt
from typing import Callable

from aocpuzzle import AoCPuzzle

hex_to_bin = {
    '0': '0000', '1': '0001', '2': '0010', '3': '0011',
    '4': '0100', '5': '0101', '6': '0110', '7': '0111',
    '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
    'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111',
}

OPS: dict[int, Callable] = {
    0: sum,
    1: prod,
    2: min,
    3: max,
    4: next,
    5: lambda x: int(gt(*x)),
    6: lambda x: int(lt(*x)),
    7: lambda x: int(eq(*x)),
}


class Packet:
    def __init__(self, binary: str) -> None:
        self.binary = binary
        self.version = self.next_bits(3)
        self.type_id = self.next_bits(3)
        self.packets_bits = 6
        self.literal_value = 0
        self.sub_packets: list[Packet] = []

        self.parse()

    def next_bits(self, bits: int) -> int:
        value = int(self.binary[0:bits], 2)

        self.binary = self.binary[bits:]

        return value

    def parse(self) -> None:
        if self.type_id == 4:
            self.process_literal()
        else:
            self.process_non_literal()

    def process_literal(self) -> None:
        literal_value = 0
        num_ones = 0

        while self.next_bits(1) == 1:
            literal_value = (literal_value << 4) + self.next_bits(4)
            num_ones += 1

        self.literal_value = (literal_value << 4) + self.next_bits(4)

        self.packets_bits += (num_ones + 1) * 5

    def process_non_literal(self) -> None:
        self.length_type_id = self.next_bits(1)
        self.packets_bits += 1

        if self.length_type_id == 1:
            subpacket_count = self.next_bits(11)
            self.packets_bits += 11

            for _ in range(subpacket_count):
                packet = Packet(self.binary)
                self.sub_packets.append(packet)

                self.packets_bits += packet.packets_bits

                self.next_bits(packet.packets_bits)

        if self.length_type_id == 0:
            bits_count = self.next_bits(15)
            self.packets_bits += 15

            while bits_count > 0:
                packet = Packet(self.binary)
                self.sub_packets.append(packet)

                self.packets_bits += packet.packets_bits
                bits_count -= packet.packets_bits

                self.next_bits(packet.packets_bits)

    def sum_versions(self) -> int:
        return self.version + sum(
            sub_packet.sum_versions()
            for sub_packet in self.sub_packets
        )

    def evaluate(self) -> int:
        return (
            self.literal_value
            if self.type_id == 4
            else OPS[self.type_id]([sub_packet.evaluate() for sub_packet in self.sub_packets])
        )


class Puzzle16(AoCPuzzle):
    def common(self, input_data: str) -> None:
        self.packet = Packet(''.join([hex_to_bin[char]for char in input_data]))

    def part1(self) -> int:
        return self.packet.sum_versions()

    def part2(self) -> int:
        return self.packet.evaluate()

    def test_cases(self, input_data: str) -> int:
        tests: list[dict] = [
            {
                'input_data': 'D2FE28',
                'part1': 6,
                'part2': 2021,
            },
            {
                'input_data': '38006F45291200',
                'part1': 9,
                'part2': 1,
            },
            {
                'input_data': 'EE00D40C823060',
                'part1': 14,
                'part2': 3,
            },
            {
                'input_data': '8A004A801A8002F478',
                'part1': 16,
                'part2': 15,
            },
            {
                'input_data': '620080001611562C8802118E34',
                'part1': 12,
                'part2': 46,
            },
            {
                'input_data': 'C0015000016115A2E0802F182340',
                'part1': 23,
                'part2': 46,
            },
            {
                'input_data': 'A0016C880162017C3686B18A3D4780',
                'part1': 31,
                'part2': 54,
            },
            {
                'input_data': 'C200B40A82',
                'part1': 14,
                'part2': 3,
            },
            {
                'input_data': '04005AC33890',
                'part1': 8,
                'part2': 54,
            },
            {
                'input_data': '880086C3E88112',
                'part1': 15,
                'part2': 7,
            },
            {
                'input_data': 'CE00C43D881120',
                'part1': 11,
                'part2': 9,
            },
            {
                'input_data': 'D8005AC2A8F0',
                'part1': 13,
                'part2': 1,
            },
            {
                'input_data': 'F600BC2D8F',
                'part1': 19,
                'part2': 0,
            },
            {
                'input_data': '9C005AC2F8F0',
                'part1': 16,
                'part2': 0,
            },
            {
                'input_data': '9C0141080250320F1802104A08',
                'part1': 20,
                'part2': 1,
            },
        ]
        for test in tests:
            self.common(test['input_data'])
            assert self.part1() == test['part1']
            self.common(test['input_data'])
            assert self.part2() == test['part2']

        self.common(input_data)
        assert self.part1() == 943
        self.common(input_data)
        assert self.part2() == 167737115857

        return len(tests) + 1
