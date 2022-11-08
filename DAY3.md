
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

