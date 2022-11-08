
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



# BUILDING KERNEL

## `Defining our Kernel`
At first, we have to download kernel from https://kernel.org/

* Create a clean Workspace
* Don't use Desktop,Downloads,Documents,Music,Videos,Pictures etc,which are meant for other purpose.
* Extract the downloaded kernel in your Workspace using following command:
```Defining our kernel
tar xvf filename
```

## Bulid Kernel
After Extract, navigate to the linux-6.0.6 folder and run the below commands 
* Follow the commands to build the kernel
```Build Kernel
make ARCH=arm mrproper
make ARCH=arm vexpress_defconfig
```
* Note: mrproper will remove built files,including the configuration.
* So run this only for any new build.

(OR) 

* customize kernal using menuconfig using following command:
```
make ARCH=arm menuconfig
```

* Now finally run this command for kernel to be bulid.
```
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi-
```
* If the kernel is not build check with upadating it 
```
sudo apt install make
sudo apt-get upgrade make
sudo apt install build-essential
```

## Qemu setup
After kernel build, navigate to your workspace and follow commands
* Install Qemu,a full system emulator for ARM target architecture
```
sudo apt install qemu-system-arm
qemu-system-arm -version
qemu-system-arm -M ?
qemu-system-aarch64 -version
```

* Download core-image-minimal-qemuarm.ext4 using the below link
```
https://downloads.yoctoproject.org/releases/yocto/yocto-2.5/machines/qemu/qemuarm/
```
* Rename the file into rootfs.img and resize it using following commands
```
e2fsck -f rootfs.img
resize2fs rootfs.img 16M
```

* Install the requried toolchain
```
sudo apt install gcc-arm-linux-gnueabi
sudo apt install gcc-arm-linux-gnueabihf
```

## Qemu Run
Now you prepare yourself for the first boot 

* At first, in your workspace create a file called images/bootables
* Second, navigate to the ## linux-6.0.6/arch/arm/boot and copy the zImage file and paste it in the images/bootables folder
* Third, navigate to the ## linux-6.0.6/arch/arm/boot/dtb and copy the vexpress-v2p-ca9.dtb file and paste it in the images/bootables folder

* Now navigate to the images/bootables and type the following to make your first boot
```
qemu-system-arm -M vexpress-a9 -nographic -kernel zimage -dtb vexpess-v2p-ca9.dtb -sd rootfs.img -append "console=ttyAMA0 root=/dev/mmcblk0 ip=192.168.7.100" -net nic -net tap,ifname=tap0
```

* If the qemu is not running or throwing structural error resize the rootfs.img

* Login as root by typing "root"

* Now type this command to now the version of Qemu 
```
uname -r
umane -v
```

## Running program in Qemu 
Now create a sample hello_world.c to print hello world using printk

* Now, save and compile the program using the following command to run the program in arm architecture
```
gcc-arm-linux-gnueabi filename.c
```

* It will generate a a.out which will only excute in arm architecture
* We can send a.out file to qemu in many ways. We are using two ways to send outputfile to qemu
The two ways 1> Copying using mount  2> By network.

## 1. Mount
* create a mounting named folder in images
* copy the a.out file to mounting/home/root/
* Unmount after copying
```
sudo mount rootfs.img mounting/
sudo cp a.out mounting/home/root
sudo umount mounting
```
By typing ls command in qemu we can see a.out file 
then type ./a.out in qemu to get output of the file 

## 2. By Network

* Now, we are transfering the file using the Network 
* In your folder where output file is generated, type the following command
```
ifconfig
```

* Previously we excuted the qemu command in which we set the ip address for qemu using name tap0
* In current directory, type the following commands
```
sudo ifconfig tap0 192.168.7.1
sudo cp a.out /srv/tftp/
```

* Now, navigate to Qemu terminal and type "ifconfig" and you can see a eth0 network with ip address set on it
* Type the following command in the qemu teminal
```
tftp -g 192.168.7.1 -r a.out
ls
```

* Now, by typing ls you can see the file a.out in the qemu terminal.
* Now type following commands to see the output in the qemu.
```
./a.out
```

* Now, you will see the output in the terminal.

INTREE and OUTTREE
=========

## OUT TREE KERNEL

* out tree kernel is nothing but modules which are developed outside the source kernel
* some commands used 
```
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
static int __init hello_init(void){
printk("Hello World..welcome\n");
return 0;
}
static void __exit hello_exit(void){
printk("Bye,Leaving the world\n");
}
module_init(hello_init);
module_exit(hello_exit);
MODULE_LICENCE("GPL")
MODULE_AUTHOR("SHARATH");
MODULE_DESCRIPTION("A simple module");
```
* Now write a Makefile to compile and run the program
* Make sure you CROSS COMPILE the program with this command ```ARCH=arm CROSS_COMPILE=arm-linux-gnueabi-```
* Now after running the program you will get ```.ko``` file which means kernel output.
* Now copy this .ko file to target kernel either by using Mount Method or Network Method.
* After this login to Qemu when you do ls you will find .ko file.
* you can run this by using following commands.

```
insmod    -> which is used to insert the module
rmmod     -> which is used to remove the module
lsmod     -> it lists the loaded modules
dmesg     -> lists the log of messages
dmesg -c  ->lists the log of messages and clears the log
```

* If you got any error while displaying the message in the qemu try these ways
* For structural error try with:-


- resizing the roofts.img
```
e2fsck -f rootfs.img
resize2fs rootfs.img 16M
```
- umount and mount again       
- delete the files and redownload

* For library errors:-
```
apt install build-essential git libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev
apt build-dep qemu-kvm
apt install libaio-dev libbluetooth-dev libbrlapi-dev libbz2-dev
apt install libsasl2-dev libsdl1.2-dev libseccomp-dev libsnappy-dev libssh2-1-dev
```
## IN TREE KERNEL

* In tree kernel is nothing but we make changes or write programs with in the kernel.
* After making changes we have to rebuid the kernel to reflect the changes.

## Dynamic Module
* Dynamic module is nothing but it can load and unload at runtime
* when we copy the kernel output to target board we can load the modules using insmod and can be unloaded with rmmod
* Create a sub dir in KSRC
```
mkdir drivers/char/dtest
```
* place hello.c in dtest
```
#include <linux/init.h>
#include<linux/module.h>
#include<linux/kernel.h>
static int __init hello_init(void)
{
printk("Hello world..Welcome\n");
return 0;
}
static void __exit hello_exit(void)
{
printk("Bye,Leaving the world\n");
}
module_init(hello_init);
module_exit(hello_exit);
MODULE_LICENSE("GPL");
MODULE_AUTHOR("Challarao");
MODULE_DESCRIPTION("A simple module");
```
* create a make file for the helo.c
```
obj-m += hello.o
```
* add the following entry to drivers/char/Makefile
* be cautious about this step, as editing 
* existingg file
```
obl-m +=dtest/
```
* Rebuild the kernel and redeploy 
* for rebuilding the kernel yse the following commands
```
make ARCH=arm CROSS_COMPILE=arm-linux-gnueabi-  modules
sudo mount -o loop,rw.sync rootfs.img/mnt/rootfs
make ARCH = arm CROSS_COMPILE=arm-linux-gnueabi- modules_install INSTALL_MOD_PATH=/mnt/rootfs
sudo umount /mnt/rootfs
```
## Static MOdule 
* These are quite opposite to dynamic modules. 
* Static modules present within the kernel if we want we can enable and disable it but we can not load unload  like dynamic modules
```
//sdemo.c ref code for static module
int svar 100;
void sayHello(void) {
printk("Greeting Hello\n");
}
static int _init sdemo_init(void) {
int i;
for(i=1;i<=4;i++)
printk("sdemo, i-%d\n", svar);
returun 0;
}
static void exit sdemo_exit(void) {
printk("Bye, Leaving the world\n");
}
EXPORT_SYMBOL_GPL (svar);
EXPORT_SYMBOL_GPL (sayHello);
```
* Create a sub dir in KSRC 
```
mkdir drivers/char/stest
```
* Place sdemo.c in stest
* Create a Makefile in stest
```
obj-y +=sdemo.o
```
* Add following entry to drivers/char/Makefile

```
obj-y +=stest/
```
* be cautious, as editing existing file
* Re-build the kernel & redeploy
* reboot with new kernel
* No need to rebuild modules (or) modules_install
* gdb-debugger
```
arm-linux-gnueabi-nm vmlinux | grep sdemo_init
arm-linux-gnueabi-objdump -t vmlinux | grep sdemo_init
```
* normal nm, objdump in case of native
* check /proc/kallsyms
```
cat /proc/kallsyms | grep sdemo_init
cat /proc/kallsyms | grep svar
cat /proc/kallsyms | grep sayHello
dmesg| grep sdemo
```
* check sdemo_init under generated
* System. map also

## GDB installation

There are two ways you can install GDB on linux.

### Install pre-built gdb binaries

**On Debian and Ubuntu:**

```
sudo apt-get update
sudo apt-get install gdb
```

### compile gdb from source, compile and install

**On Debian and Ubuntu:**

Download source code.

```
wget "http://ftp.gnu.org/gnu/gdb/gdb-7.11.tar.gz"
```

Extract the source code.

```
tar -xvzf gdb-7.11.tar.gz
```

Configure, Compile, and install it.

```
cd gdb-7.11
./configure
make
make install
sudo make install (optional)
```
By default this will install gdb binaries in /usr/local/bin and libs in /usr/local/lib.

To check version and test whether gdb installed correctly.

```
gdb --version
```

## Example Debug C Program

Compile your C program with -g option. This allows the compiler to collect the debugging information.

```
cd gdb-debugger
gcc -g -o fibonacci fibonacci_naive.c
./fibonacci
```
Example for the gdb debugging
```
# include <stdio.h>
int main()
{
int i, num, j;
printf ("Enter the number: ");
scanf ("%d", &num );
for (i=1; i<num; i++)
j=j*i;    
printf("The factorial of %d is %d\n",num,j);
}
```
Launch the C debugger (gdb).

```
gdb ./fibonacci
```

Set up a break point inside C program. The Syantx is `break line_number`

```
break 10
Breakpoint 1 at 0x400641: file fibonacci_naive.c, line 10.
```

Execute the C program in gdb debugger.

```
run
```

Once you executed the C program, it would execute until the first break point, and give you the prompt for debugging.

```
(gdb) run
Starting program: /home/arslan/github-repositories/gdb-debugger/fibonacci 

Breakpoint 1, main (argc=1, argv=0x7fffffffda48) at fibonacci_naive.c:10
10	int main(int argc, char** argv) {
```

* For all the options available for gdb are seen in the below link 
```
https://gist.github.com/rkubik/b96c23bd8ed58333de37f2b8cd052c30
```
# OOPS Crash Analysis

* An “Oops” is something the kernel would trigger when some goes wrong in execution sequence, or an exception, in the kernel code. It’s somewhat like the segfaults of user-space.
* It has three types of crash analysis

## 1.Kernel Panic

* This a situation wherein the system enters into dead state due to the severity of the crash. Technically speaking, a panic is a subset of the oops (i.e., the more     serious of the oopses). 


* After running the qemu you can see the kernel panic.

* As shown in the below screenshot.


## 2.Aiee

* A hard panic related with interrupts

## 3.Taint

* The kernel will mark itself as 'tainted' when something occurs that might be relevant later when investigating problems, Don't worry too much about this, most of the time it's not a problem to run a tainted kernel;

* To solve the oops crash we have a method, is known as ```addr2line```

## Address to Line

* The addr2line (address to line) command is a very useful tool for identifying the line of code that caused the problem!

* The man page for this command contains additional details.
* The basic use case is shown as follows.

```
addr2line -f <the offset address from the crash info> -e <path of the executable file>
```
* Use the proper compiler triplet as a prefix if you are working on an embedded target board.
* You can use the following line with ARM architecture.

```
arm-linux-gnueabi-addr2line -f <the offset address from the crash info> -e <path of the executable file>
```

## Dynamic Modules

Since the functions are not a part of vmlinux, the effort required for bug tracing with dynamic modules (which might be either In-Tree or Out-Tree) is significantly less than that required for static modules, making bug analysis simple and quicker.

```
arm-linux-gnueabi-addr2line -f 0x28 -e oops.ko
```
* This command will show the error line in the program
```
init_kernel_module
/home/u40017723/WorkSpace/EOS/EmbeddedLinux/Qemu/KernelDebugging/Modules/Oops/oops.c:11
```
## Static Code

* To locate the crash site in code that is included in the kernel image, you can also use the addr2line programme.
* In this situation, vmlinux will have to do since we need an image with debugging symbols enabled in it.

```
arm-linux-gnueabi-addr2line -f 80b014f4 -e vmlinux
```

* This command will show the error line in the program
```
kernel_init_freeable at /home/u40017723/WorkSpace/KernelDebugging/linux-5.14.7/init/main.c:1606
```

## Objdump

* If you recall from the previous chapter, the addr2line function only gives us the line number from the file that crashed, nothing more. To perform a more thorough analysis, we will either need to open the file and look for the problem in the given line or use gdb.

```
objdump -x /bin/ls
```


