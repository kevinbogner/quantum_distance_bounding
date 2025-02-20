"""This module contains common functions used in quantum computing notebooks.

It includes functions to encode and decode messages using quantum circuits.

Some functions are adapted from:
https://github.com/Qiskit/textbook/blob/main/notebooks/ch-algorithms/quantum-key-distribution.ipynb
"""

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister, transpile
from qiskit_aer import Aer


def encode_message(bits, bases, n):
    message = []
    for i in range(n):
        qc = QuantumCircuit(1, 1)
        if bases[i] == 0:
            if bits[i] == 0:
                pass
            else:
                qc.x(0)
        else:
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)
        qc.barrier()
        message.append(qc)
    return message


def decode_message(message, bases, n, draw_circuit=False):
    backend = Aer.get_backend("aer_simulator")
    __ = backend
    measurements = []
    for q in range(n):
        if bases[q] == 1:
            message[q].h(0)
        message[q].measure(0, 0)

        aer_sim = Aer.get_backend("aer_simulator")
        result = aer_sim.run(
            transpile(message[q], aer_sim), shots=1, memory=True
        ).result()
        measured_bit = int(result.get_memory()[0])
        measurements.append(measured_bit)
    return measurements


def remove_garbage(a_bases, b_bases, bits, n):
    """This function removes 'garbage' bits where Alice's and Bob's bases don't
    align.

    Parameters:
    a_bases (list): A list representing Alice's bases.
    b_bases (list): A list representing Bob's bases.
    bits (list): A list representing the bits to be filtered.
    n (int): The range for the loop that checks alignment of bases.

    Returns:
    list: A list of 'good' bits where Alice's and Bob's bases align.
    """
    good_bits = []
    for q in range(n):
        if a_bases[q] == b_bases[q]:
            # If both used the same basis, add
            # this to the list of 'good' bits
            good_bits.append(bits[q])
    return good_bits


def sample_bits(bits, selection):
    """This function samples bits from a list at the indices specified in
    'selection'. The function uses modulo operation to ensure the sampled index
    is always within the list range. The sampled bit is removed from the
    original list to avoid duplication.

    Parameters:
    bits (list): A list of bits to sample from.
    selection (list): A list of indices to sample bits from.

    Returns:
    list: A list of sampled bits.
    """
    sample = []
    for i in selection:
        # use np.mod to make sure the
        # bit we sample is always in
        # the list range
        i = np.mod(i, len(bits))
        # pop(i) removes the element of the
        # list at index 'i'
        sample.append(bits.pop(i))
    return sample


def create_and_measure_bell_state(n):
    """Create a quantum circuit that prepares entangled Bell states and then
    measures them for two parties, using a specified basis for each qubit pair.

    Parameters:
    n (int): Number of Bell states to prepare and measure.

    Returns:
    QuantumCircuit: The created quantum circuit with Bell states and measurements.
    """
    # Create a quantum register
    qr = QuantumRegister(2 * n)

    # Create the quantum circuit
    bell = QuantumCircuit(qr)

    # Create entangled Bell states
    for i in range(0, 2 * n, 2):
        bell.h(qr[i])
        bell.cx(qr[i], qr[i + 1])

    # Create classical registers for measurement results
    m = ClassicalRegister(n, "m")
    m_prime = ClassicalRegister(n, "m_prime")

    # Add the classical registers to the circuit
    bell.add_register(m)
    bell.add_register(m_prime)

    # Measurements
    for i in range(n):
        bell.measure(qr[2 * i], m[i])  # Party A measures the first qubit of the pair
        bell.measure(
            qr[2 * i + 1], m_prime[i]
        )  # Party B measures the second qubit of the pair

    return bell


def execute_and_extract_results(bell_circuit, shots=1):
    """
    Execute the Bell state circuit on a quantum simulator, extract, and process the results.

    Parameters:
    bell_circuit (QuantumCircuit): The Bell state quantum circuit to execute.
    shots (int): Number of times to run the simulation.

    Returns:
    tuple: A tuple containing two lists with bit measurement results of m and m_prime registers.
    """
    # Execute the circuit on a quantum simulator
    backend = Aer.get_backend("qasm_simulator")
    transpiled_circuit = transpile(bell_circuit, backend=backend)

    aer_sim = Aer.get_backend("aer_simulator")
    job = aer_sim.run(transpiled_circuit, shots=shots)
    result = job.result()
    counts = result.get_counts()

    m_bits = []
    m_prime_bits = []
    for key in counts.keys():
        m_result, m_prime_result = key.split(" ")
        m_bits.extend([int(bit) for bit in m_result])
        m_prime_bits.extend([int(bit) for bit in m_prime_result])

    return m_bits, m_prime_bits
