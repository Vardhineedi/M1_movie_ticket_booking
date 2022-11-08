
INTRODUCTION TO KERNEL PROGRAMMING
===========


## `INTRODUCTION`
* Initiated by Linux Torvalds as a hobby project in 1991
* Inspired by Minix OS designed by Andrew S Tanenbaum
* Popular kernal for Free and Open Source Operating System, e.g. GNU Linux


## Advantages 
* Secure,Stable and Reliable
* Rich set of generic drivers
* Rich set of networking drivers & protocol stacks
* Upstream(mainline) and Downstream kernel
* Supported Languages - C and Assembly

## QEMU

* QEMU is a generic and open source machine & userspace emulator and
virtualizer.

* QEMU is capable of emulating a complete machine in software without any
need for hardware virtualization support. By using dynamic translation,
it achieves very good performance. QEMU can also integrate with the Xen
and KVM hypervisors to provide emulated hardware while allowing the
hypervisor to manage the CPU. With hypervisor support, QEMU can achieve
near native performance for CPUs. When QEMU emulates CPUs directly it is
capable of running operating systems made for one machine (e.g. an ARMv7
board) on a different machine (e.g. an x86_64 PC board).

* QEMU is also capable of providing userspace API virtualization for Linux
and BSD kernel interfaces. This allows binaries compiled against one
architecture ABI (e.g. the Linux PPC64 ABI) to be run on a host using a
different architecture ABI (e.g. the Linux x86_64 ABI). This does not
involve any hardware emulation, simply CPU and syscall emulation.

* nQEMU aims to fit into a variety of use cases. It can be invoked directly
by users wishing to have full control over its behaviour and settings.
It also aims to facilitate integration into higher level management
layers, by providing a stable command line interface and monitor API.
It is commonly invoked indirectly via the libvirt library when using
open source applications such as oVirt, OpenStack and virt-manager.

* QEMU as a whole is released under the GNU General Public License,
version 2. For full licensing details, consult the LICENSE file.
