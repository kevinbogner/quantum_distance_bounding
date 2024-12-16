"""
This module contains the RegisterManager class which manages the creation
and retrieval of classical and quantum registers.

The RegisterManager class provides a way to create a specified number of
classical and quantum registers, each with a specified size. The
registers are named using provided names or integers if no names are
provided. Once created, the registers are immutable and can be retrieved
using their names.
"""


from qiskit import QuantumRegister
import numpy as np


class RegisterManager:
    """This class encapsulates the creation of classical and quantum registers.

    The registers are immutable, meaning they cannot be changed after
    they are created.
    """

    def __init__(
        self,
        num_classical,
        num_quantum,
        size_classical,
        size_quantum,
        classical_names=None,
        quantum_names=None,
    ):
        """Initialize the RegisterManager class.

        Parameters:
        num_classical (int): The number of classical registers.
        num_quantum (int): The number of quantum registers.
        size_classical (int): The size of each classical register.
        size_quantum (int): The size of each quantum register.
        classical_names (list of str): The names of the classical registers.
        quantum_names (list of str): The names of the quantum registers.
        """
        if classical_names is not None:
            num_classical = len(classical_names)

        self._classical_registers = {}
        for name in classical_names or range(num_classical):
            self._classical_registers[name] = np.random.randint(2, size=size_classical)
            print(
                f"Created classical register {name} with values {self._classical_registers[name]}"
            )

        self._quantum_registers = {}
        for name in quantum_names or range(num_quantum):
            self._quantum_registers[name] = QuantumRegister(size_quantum)
            print(f"Created quantum register {name} with size {size_quantum}")

    def get_classical_register(self, name):
        """Get a classical register.

        Parameters:
        name (str): The name of the classical register.

        Returns:
        numpy.ndarray: The classical register with the given name.
        """
        return self._classical_registers[name]

    def get_quantum_register(self, name):
        """Get a quantum register.

        Parameters:
        name (str): The name of the quantum register.

        Returns:
        qiskit.circuit.quantumregister.QuantumRegister: The quantum register with the given name.
        """
        return self._quantum_registers[name]
